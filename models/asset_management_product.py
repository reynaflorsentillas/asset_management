from odoo import models, fields

STATE_COLOR_SELECTION = [
    ('0', 'Red'),
    ('1', 'Green'),
    ('2', 'Blue'),
    ('3', 'Yellow'),
    ('4', 'Magenta'),
    ('5', 'Cyan'),
    ('6', 'Black'),
    ('7', 'White'),
    ('8', 'Orange'),
    ('9', 'SkyBlue')
]

class ProductProduct(models.Model):
    _inherit = 'product.template'
    
    is_asset = fields.Boolean(string='Is Asset', help='Check if the product is an asset')

class AssetManagementAssetProduct(models.Model):
    _inherit = 'product.template'

    # @api.multi
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = '[' + str(record.asset_number) + ']' + ' ' + record.name
    #         result.append((record.id, name))
    #     return result

    def _read_group_state_ids(self, domain, read_group_order=None, access_rights_uid=None, team='3'):
        access_rights_uid = access_rights_uid or self.uid
        stage_obj = self.env['asset_management.state']
        order = stage_obj._order
        # lame hack to allow reverting search, should just work in the trivial case
        if read_group_order == 'stage_id desc':
            order = "%s desc" % order
        # write the domain
        # - ('id', 'in', 'ids'): add columns that should be present
        # - OR ('team','=',team): add default columns that belongs team
        search_domain = []
        search_domain += ['|', ('team','=',team)]
        search_domain += [('id', 'in', ids)]
        stage_ids = stage_obj._search(search_domain, order=order, access_rights_uid=access_rights_uid)
        result = stage_obj.name_get(access_rights_uid, stage_ids)
        # restore order of the search
        result.sort(lambda x,y: cmp(stage_ids.index(x[0]), stage_ids.index(y[0])))
        return result, {}    

    def _read_group_finance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '0')

    def _read_group_warehouse_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '1')

    def _read_group_manufacture_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '2')

    def _read_group_maintenance_state_ids(self, domain, read_group_order=None, access_rights_uid=None):
        return self._read_group_state_ids(domain, read_group_order, access_rights_uid, '3')

    CRITICALITY_SELECTION = [
        ('0', 'General'),
        ('1', 'Important'),
        ('2', 'Very important'),
        ('3', 'Critical')
    ]

    # name = fields.Char('Asset Name', size=64, required=True, translate=True)
    finance_state_id = fields.Many2one('asset_management.state', 'State', domain=[('team','=','0')])
    warehouse_state_id = fields.Many2one('asset_management.state', 'State', domain=[('team','=','1')])
    manufacture_state_id = fields.Many2one('asset_management.state', 'State', domain=[('team','=','2')])
    maintenance_state_id = fields.Many2one('asset_management.state', 'State', domain=[('team','=','3')])
    maintenance_state_color = fields.Selection(related='maintenance_state_id.state_color', selection=STATE_COLOR_SELECTION, string="Color", readonly=True)
    criticality = fields.Selection(CRITICALITY_SELECTION, 'Criticality')
    # property_stock_asset = fields.Many2one('stock.location', "Asset Location", company_dependent=True, domain=[('usage', 'like', 'asset')], help="This location will be used as the destination location for installed parts during asset life.")
    user_id = fields.Many2one('res.users', 'Assigned to', track_visibility='onchange')
    active = fields.Boolean('Active', default=True)
    status = fields.Selection([
        ('in', 'IN'),
        ('out', 'OUT'),
    ], string='Asset Current Status')
    asset_number = fields.Char('Asset Number', size=64)
    model = fields.Char('Model', size=64)
    serial = fields.Char('Serial No.', size=64)

    vendor_id = fields.Many2one('res.partner', 'Vendor')
    manufacturer_id = fields.Many2one('res.partner', 'Manufacturer')
    start_date = fields.Date('Start Date')
    purchase_date = fields.Date('Purchase Date')
    warranty_start_date = fields.Date('Warranty Start')
    warranty_end_date = fields.Date('Warranty End')
    # image = fields.Binary("Image")
    # image_small = fields.Binary("Small-sized image")
    # image_medium = fields.Binary("Medium-sized image")
    category_ids = fields.Many2many('asset_management.category', id1='asset_id', id2='category_id', string='Tags')

    expiration_date = fields.Datetime(string='Date')
    maintenance_date = fields.Datetime(string='Date')
    maintenance_duration = fields.Float(string='Duration')
    calibration_date = fields.Datetime(string='Date')
    calibration_duration = fields.Datetime(string='Duration')

    _group_by_full = {
        'finance_state_id': _read_group_finance_state_ids,
        'warehouse_state_id': _read_group_warehouse_state_ids,
        'manufacture_state_id': _read_group_manufacture_state_ids,
        'maintenance_state_id': _read_group_maintenance_state_ids,
    }

    # @api.model
    # def create(self, vals):
    #     tools.image_resize_images(vals)
    #     return super(AssetManagementAsset, self).create(vals)

    # @api.multi
    # def write(self, vals):
    #     tools.image_resize_images(vals)
    #     return super(AssetManagementAsset, self).write(vals)