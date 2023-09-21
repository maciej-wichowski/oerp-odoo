# Author: Andrius Laukavičius. Copyright: Andrius Laukavičius.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Product Stamp Configurator",
    'version': '16.0.1.0.0',
    'summary': 'Base stamp product configurator module',
    'license': 'LGPL-3',
    'author': "Andrius Laukavičius",
    'website': "https://timefordev.com",
    'category': 'Sales/Sales',
    'depends': [
        # odoo
        'product',
    ],
    'data': [
        'security/product_stamp_configurator_groups.xml',
        'security/ir.model.access.csv',
        'security/stamp_design_security.xml',
        'security/stamp_die_security.xml',
        'security/stamp_difficulty_security.xml',
        'security/stamp_finishing_security.xml',
        'security/stamp_material_security.xml',
        'security/stamp_pricelist_security.xml',
        'views/res_config_settings.xml',
        'views/res_partner.xml',
        'views/product_category.xml',
        'views/product_template.xml',
        'views/stamp_pricelist.xml',
        'views/stamp_design.xml',
        'views/stamp_die.xml',
        'views/stamp_difficulty.xml',
        'views/stamp_finishing.xml',
        'views/stamp_material.xml',
        'views/menus.xml',
        # TODO: remove this once it can be used from sales
        'wizards/stamp_configure_views.xml',
    ],
    'application': True,
    'installable': True,
}
