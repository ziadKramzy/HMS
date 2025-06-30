from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(string="Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_opened = fields.Boolean(string="Is Opened")
    patient_ids = fields.One2many('hms.patient', 'department_id', string="Patients")

    @api.constrains('is_opened')
    def _check_is_opened(self):
        for record in self:
            if not record.is_opened and record.patient_ids:
                raise ValidationError("You cannot have patients in a closed department.")
