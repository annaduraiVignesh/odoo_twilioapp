
##################################    TWILIO PYTHON   ###########################################

from twilio import *
from odoo import models, fields, api
from twilio.rest import TwilioRestClient
from odoo.exceptions import Warning
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
from twilio import TwilioRestException

# Provide account value and token on below line
client = TwilioRestClient(account='YOUR ACCOUNT', token='YOUR TOKEN HERE')


class contact_contact_base(models.Model):
    _name = 'contact.twiliocontact_base'
    _rec_name = 'contact_name_contactclass'


    contact_name_contactclass = fields.Char(string="Contact Name")
    to = fields.Char(string="To", size=13)
    image = fields.Binary(string="Contact Avatar")

class TwilioBase(models.Model):
    _name = 'twiliosms.base'
    _inherits = {'contact.twiliocontact_base':'contact_name'}

    _defaults = {
              'date_time': lambda *a:datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
              }
    from_ = fields.Char(string="Your Number", default='YOUR TWILIO NUMBER here',required=True,help="Pls, provide your twilio number")
    contact_name = fields.Many2one('contact.twiliocontact_base', string="Contact Name", required=True,help="Your contact number here")
    body = fields.Char(string="Message", size=160)
    display_all = fields.Text(string="Sender,Receiver,Message", readonly=True)
    date_time = fields.Datetime(string="Date & Time",  readonly=True)
    msg_status = fields.Char(string="Status")

    @api.onchange('msg_status')
    def onchangedate(self):
        self.date_time = str(datetime.now())

    @api.multi
    @api.depends('from_', 'to', 'body')
    @api.model
    def sendsms(self):
        if not self.body:
            raise Warning("Message part is empty")
        else:
            try:
                client.messages.create(from_=self.from_, to=self.to, body=self.body)
                self.display_all = "Sender Number  " + str(self.from_) + "  Receiver Number " + str(self.to) \
                + "Message Content -> " + str(self.body) + "  at " + str(self.date_time)
                msg_status = str("Message Sent")
                self.msg_status = msg_status

            except TwilioRestException as e:
                print(e)
                domain=[('contact_name_contactclass', '=', self.contact_name_contactclass)]
                res = self.env['contact.twiliocontact_base'].search(domain)
                count_domain = [('contact_name_contactclass', '=', self.contact_name_contactclass)]
                rec = self.env['contact.twiliocontact_base'].search_count(count_domain)
                raise Warning("This is not a registered Number, plz verify (OR) register")
        return

    @api.multi
    @api.depends('from_', 'to')
    @api.model
    def callnumber(self):
        if not self.to:
            raise Warning("contact number is empty")
        else:
            try:
                client.calls.create(url="http://demo.twilio.com/docs/voice.xml", to=self.to, from_=self.from_)
            except TwilioRestException as e:
                print(e)
                raise Warning("This is not a registered Number, plz verify OR register")
        return


