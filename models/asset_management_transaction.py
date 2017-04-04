from odoo import api, fields, models, _ 

class AssetManagementTransaction(models.Model):
    _name = 'asset_management.transaction'
    _description = 'Asset Transactions'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    reader_name = fields.Char(string='Reader Name')
    mac_address = fields.Char(string='Mac Address')
    tid = fields.Char(string='Tag Serial number')
    epc = fields.Char(string='Scanned Tag Asset Number')

    asset_id = fields.Many2one(comodel_name='asset_management.asset', index=True, string='Asset')
    security_gate_id = fields.Many2one(comodel_name='asset_management.security.gate', index=True, string='Security Gate')
    status = fields.Selection([
        ('in', 'IN'),
        ('out', 'OUT')
    ])

    @api.model
    def create(self, values):
        """
            Create a new record for a model ModelName
            @param values: provides a data for new record
    
            @return: returns a id of new record
        """
        if values.get('name', 'New') == 'New':
            values['name'] = self.env['ir.sequence'].next_by_code('asset_management.transaction') or 'New'
            # values['asset_id'] = self.env['asset_management.asset'].browse(self.asset_id.asset_number)
    
        result = super(AssetManagementTransaction, self).create(values)
    
        return result
