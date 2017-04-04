from odoo import models, fields 

class AssetManagementReader(models.Model):
    _name = 'asset_management.reader'
    _description = 'Asset Management Readers'

    name = fields.Char(required=True)
    type = fields.Selection([
        ('fixed','Fixed'),
        ('handheld', 'Handheld'),
    ])