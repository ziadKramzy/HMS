from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string="Related Patient")
    vat = fields.Char(string="Tax ID" ,required=True)

    @api.constrains('related_patient_id')
    def _check_patient_link_unique(self):
        for record in self:
            if record.related_patient_id:
                existing_partner = self.search([
                    ('id', '!=', record.id),
                    ('related_patient_id', '=', record.related_patient_id.id)
                ])
                if existing_partner:
                    raise ValidationError("This patient is already linked to another customer.")

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise UserError("You cannot delete a customer linked to a patient.")
        return super().unlink()
