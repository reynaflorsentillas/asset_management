from odoo import fields, models

class AssetManagementSecurityGate(models.Model):
    _name = 'asset_management.security.gate'
    _description = 'Asset Management Security Gate'

    name = fields.Char(required=True)
    type = fields.Selection([
        ('entry','Entry'),
        ('exit', 'Exit'),
    ], required=True)
    reader_id = fields.Many2one(comodel_name='asset_management.reader', string='Assigned Reader')
    warehouse_id = fields.Many2one('stock.warehouse', 'Served Warehouse', help='The warehouse this rule is for')
    more_info = fields.Text(string='More Info')
    