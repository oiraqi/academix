from odoo import models, fields, api

class LmsAssessmentLine(models.Model):
    _inherit = 'ixlms.assessment.line'

    assessed_ilo_ids = fields.One2many(comodel_name='ixquality.assessed.ilo', inverse_name='assessment_line_id', string='Assessed ILOs')

    def create_assessed_ilos(self):
        self.ensure_one()
        assessed_ilo_ids = [assessed_ilo_id.ilo_id for assessed_ilo_id in self.assessed_ilo_ids]
        for ilo in self.assessment_id.ilo_ids:
            if ilo.id not in assessed_ilo_ids:
                self.env['ixquality.assessed.ilo'].create({            
                    'assessment_line_id': self.id,
                    'ilo_id': ilo.id,
                })

    