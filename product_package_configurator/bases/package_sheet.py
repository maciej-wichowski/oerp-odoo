from odoo import fields, models

from .. import const


class PackageSheet(models.AbstractModel):

    _name = 'package.sheet'
    _description = "Package Sheet"

    price_unit = fields.Float(required=True, digits=const.DecimalPrecision.PRICE)
    sheet_length = fields.Float(
        "Length, mm", required=True, digits=const.DecimalPrecision.SIZE
    )
    sheet_width = fields.Float(
        "Width, mm", required=True, digits=const.DecimalPrecision.SIZE
    )
    company_id = fields.Many2one(
        'res.company', required=True, default=lambda s: s.env.company
    )
    currency_id = fields.Many2one(related='company_id.currency_id')
