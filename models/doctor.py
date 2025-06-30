from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _rec_name = 'first_name'
    _description = 'Doctors'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    image = fields.Binary(string="Image")
