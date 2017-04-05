from odoo import api, fields, models, _ 

class AssetManagementTransaction(models.Model):
    _name = 'asset_management.transaction'
    _description = 'Asset Transactions'

    name = fields.Char(string='Code', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    
    asset_id = fields.Many2one(comodel_name='asset_management.asset', index=True, string='Asset')
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
            asset_id = self.env['asset_management.asset'].search([('asset_number', '=', asset_number)])
            asset = self.env['asset_management.asset'].browse(asset_id.id)
            values['asset_id'] = asset.id

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
