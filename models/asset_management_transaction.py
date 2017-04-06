from odoo import api, fields, models, _ 

class AssetManagementTransaction(models.Model):
    _name = 'asset_management.transaction'
    _description = 'Asset Transactions'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    # asset_id = fields.Many2one(comodel_name='asset_management.asset', index=True, string='Asset')
    asset_id = fields.Many2one(comodel_name='product.template', index=True, string='Asset', domain="[('is_asset', '=', 'true')]")
    # asset_id = fields.Many2one(comodel_name='product.template', index=True, string='Asset')
    security_gate_id = fields.Many2one(comodel_name='asset_management.security.gate', index=True, string='Security Gate')
    status = fields.Selection([
        ('in', 'IN'),
        ('out', 'OUT')
    ])

    reader_name = fields.Char(string='Reader Name')
    mac_address = fields.Char(string='Mac Address')
    tid = fields.Char(string='Tag Serial number')
    epc = fields.Char(string='Scanned Tag Asset Number')

    transaction_date = fields.Datetime(string='Date and Time', default=fields.Datetime.now, readonly=True)

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('asset_management.transaction') or 'New'
        
        asset_number = values['epc']
        if asset_number:
            # asset_id = self.env['product.template'].search([('default_code', '=', asset_number)])
            # if asset_id:
            #     asset = self.env['product.template'].browse(asset_id.id)
            #     values['asset_id'] = asset.id
            serial_id = self.env['stock.production.lot'].search([('name', '=', asset_number)])
            if serial_id:
                serial = self.env['stock.production.lot'].browse(serial_id.id)
                values['asset_id'] = serial.product_id.id

        reader_name = values['reader_name']
        if reader_name:
            reader_id = self.env['asset_management.reader'].search([('name', '=', reader_name)])
            gate_id = self.env['asset_management.security.gate'].search([('reader_id', '=', reader_id.id)])
            gate = self.env['asset_management.security.gate'].browse(gate_id.id)
            values['security_gate_id'] = gate.id
            if gate.type == 'entry':
                values['status'] = 'in'
            if gate.type == 'exit':
                values['status'] = 'out'
    
        result = super(AssetManagementTransaction, self).create(values)
    
        return result
    
    @api.multi
    def write(self, vals):
        if 'epc' in vals:
            asset_number = vals['epc']
            if asset_number:
                asset_id = self.env['product.template'].search([('default_code', '=', asset_number)])
                if asset_id:
                    asset = self.env['product.template'].browse(asset_id.id)
                    vals['asset_id'] = asset.id
            # new_uom = self.env['product.uom'].browse(vals['uom_id'])
            # updated = self.filtered(lambda template: template.uom_id != new_uom)
            # done_moves = self.env['stock.move'].search([('product_id', 'in', updated.mapped('product_variant_ids').ids)], limit=1)
            # if done_moves:
                # raise UserError(_("You can not change the unit of measure of a product that has already been used in a done stock move. If you need to change the unit of measure, you may deactivate this product."))
        return super(AssetManagementTransaction, self).write(vals)