{
    'name': "Twilio SMS",
    'summary': """ This App has the ability to send SMS using twilio """,
    'version': '10.0.1.0.0',
    'category': 'SMS app',
    'website': "viki2.odoo.com",
    'author': "Vignesh",
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'images': ['images/main_screenshot.png'],
    'depends': ['base'],
    'data': [
         'views/twiliosms_send_view.xml',
    ],
}
