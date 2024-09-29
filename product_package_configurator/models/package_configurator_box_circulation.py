from odoo import api, fields, models

from ..utils.fitter import calc_sheet_quantity
from ..utils.misc import multiply


class PackageConfiguratorBoxCirculation(models.Model):
    """Model to be able to have multiple circulation options for box."""

    _name = 'package.configurator.box.circulation'
    _inherit = 'package.configurator.circulation'
    _description = "Package Configurator Box Circulation"

    configurator_id = fields.Many2one('package.configurator.box')
    total_carton_quantity = fields.Integer(compute='_compute_sheet_quantity')
    total_inside_wrappingpaper_quantity = fields.Integer(
        compute='_compute_sheet_quantity',
        string="Total Inside Wrapping Paper Quantity",
    )
    total_outside_wrappingpaper_quantity = fields.Integer(
        compute='_compute_sheet_quantity',
        string="Total Outside Wrapping Paper Quantity",
    )
    # price/cost fields should be part of package.configurator.circulation
    # abstraction, which would need to be implemented in concrete class.
    unit_cost = fields.Float(compute='_compute_cost')
    total_cost = fields.Float(compute='_compute_cost')

    @api.depends(
        'configurator_id.base_layout_fit_qty',
        'configurator_id.base_inside_fit_qty',
        'configurator_id.base_outside_fit_qty',
        'configurator_id.lid_layout_fit_qty',
        'configurator_id.lid_inside_fit_qty',
        'configurator_id.lid_outside_fit_qty',
        'quantity',
    )
    def _compute_sheet_quantity(self):
        for rec in self:
            rec.update(rec._get_sheet_quantity_data())

    @api.depends(
        'total_carton_quantity',
        'total_inside_wrappingpaper_quantity',
        'total_outside_wrappingpaper_quantity',
        'quantity',
        'configurator_id.carton_id',
        'configurator_id.wrappingpaper_inside_id',
        'configurator_id.wrappingpaper_outside_id',
    )
    def _compute_cost(self):
        for rec in self:
            rec.update(rec._get_price_data())

    def _get_sheet_quantity_data(self):
        def add_qty_if_applicable(data, fname, fit_qty):
            if fit_qty:
                data[fname] += calc_sheet_quantity(self.quantity, fit_qty)

        self.ensure_one()
        data = self._get_init_sheet_quantity_data()
        cfg = self.configurator_id
        add_qty_if_applicable(data, 'total_carton_quantity', cfg.base_layout_fit_qty)
        add_qty_if_applicable(data, 'total_carton_quantity', cfg.lid_layout_fit_qty)
        add_qty_if_applicable(
            data, 'total_inside_wrappingpaper_quantity', cfg.base_inside_fit_qty
        )
        add_qty_if_applicable(
            data, 'total_inside_wrappingpaper_quantity', cfg.lid_inside_fit_qty
        )

        add_qty_if_applicable(
            data, 'total_outside_wrappingpaper_quantity', cfg.base_outside_fit_qty
        )
        add_qty_if_applicable(
            data, 'total_outside_wrappingpaper_quantity', cfg.lid_outside_fit_qty
        )
        return data

    def _get_init_sheet_quantity_data(self):
        return {
            'total_carton_quantity': 0,
            'total_inside_wrappingpaper_quantity': 0,
            'total_outside_wrappingpaper_quantity': 0,
        }

    def _get_price_data(self):
        self.ensure_one()
        data = {'unit_cost': 0, 'total_cost': 0}
        if self.quantity:
            cfg = self.configurator_id
            total_cost = 0
            total_cost += multiply(cfg.carton_id.unit_cost, self.total_carton_quantity)
            total_cost += multiply(
                cfg.wrappingpaper_inside_id.unit_cost,
                self.total_inside_wrappingpaper_quantity,
            )
            total_cost += multiply(
                cfg.wrappingpaper_outside_id.unit_cost,
                self.total_outside_wrappingpaper_quantity,
            )
            data.update(
                {'unit_cost': total_cost / self.quantity, 'total_cost': total_cost}
            )
        return data
