from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re

class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient Record'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    department_id = fields.Many2one('hms.department', string="Department", domain="[('is_opened','=',True)]")
    department_capacity = fields.Integer(string="Department Capacity", related="department_id.capacity", readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors")
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string="Logs")
    state = fields.Selection([
    ('undetermined', 'Undetermined'),
    ('good', 'Good'),
    ('fair', 'Fair'),
    ('serious', 'Serious')
    ], string="State", default='undetermined')
    email = fields.Char(string="Email", required=True)
    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user, readonly=True)


    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = date.today()
                record.age = today.year - record.birth_date.year
            else:
                record.age = 0

    @api.onchange('age')
    def _onchange_age(self):
        for record in self:
            if record.age < 30:
                record.pcr = True
                return {
                    'warning': {
                        'title': "PCR Checked Automatically",
                        'message': "PCR has been checked automatically because age is below 30."
                    }
                }

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is required if PCR is checked.")

    @api.onchange('state')
    def _onchange_state(self):
        for record in self:
            if record.state and record.id:
                self.env['hms.patient.log'].create({
                    'description': f"State changed to {record.state.capitalize()}",
                    'patient_id': record.id
                })

    @api.constrains('email')
    def _check_email_validity_uniqueness(self):
        for record in self:
            if record.email:
                email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                if not re.match(email_regex, record.email):
                    raise ValidationError("Please enter a valid email address.")

                existing = self.env['hms.patient'].search([('email', '=', record.email), ('id', '!=', record.id)])
                if existing:
                    raise ValidationError("Email must be unique. This email is already assigned to another patient.")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.first_name} {record.last_name}" if record.first_name and record.last_name else record.first_name or record.last_name or "Unknown"
            result.append((record.id, name))
        return result

    def print_patient_report(self):
        # Find the report action by searching for it
        report_action = self.env['ir.actions.report'].search([
            ('name', '=', 'Patient Status Report'),
            ('model', '=', 'hms.patient')
        ], limit=1)
        
        if report_action:
            return report_action.report_action(self)
        else:
            # Fallback: try to get it by external ID
            try:
                return self.env.ref('hms.patient_status_pdf').report_action(self)
            except ValueError:
                raise ValueError("Patient Status Report not found. Please check if the report is properly installed.")
