# Author: Andrius Laukavičius. Copyright: Andrius Laukavičius.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Product Stamp Configurator - Sale CRM",
    'version': '15.0.1.0.0',
    'summary': 'Stamp product configurator integration with sales and CRM',
    'license': 'LGPL-3',
    'author': "Andrius Laukavičius",
    'website': "https://timefordev.com",
    'category': 'Sales/CRM',
    'depends': [
        # odoo
        'sale_crm',
        # oerp-odoo
        'product_stamp_configurator_sale',
    ],
    'installable': True,
    'auto_install': True,
}
