# Author: Andrius Laukavičius. Copyright: Andrius Laukavičius.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Product Stamp Configurator - Sale",
    'version': '15.0.1.0.0',
    'summary': 'Stamp product configurator integration with sales',
    'license': 'LGPL-3',
    'author': "Andrius Laukavičius",
    'website': "https://timefordev.com",
    'category': 'Sales/Sales',
    'depends': [
        # odoo
        'sale',
        # oerp-odoo
        'product_stamp_configurator',
    ],
    'data': [
        'views/sale_order.xml',
        'wizards/stamp_configure_views.xml',
    ],
    'installable': True,
    'auto_install': True,
}