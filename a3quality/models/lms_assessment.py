from odoo import models, fields

class LmsAssessment(models.Model):
    _inherit = 'a3lms.assessment'

    ilo_ids = fields.Many2many(comodel_name='a3catalog.course.ilo', string='ILOs')
    