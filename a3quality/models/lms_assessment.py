from odoo import models, fields

class LmsAssessment(models.Model):
    _inherit = 'a3lms.assessment'

    course_ilo_ids = fields.One2many('a3catalog.course.ilo', related='course_id.ilo_ids')
    ilo_ids = fields.Many2many(comodel_name='a3catalog.course.ilo', string='ILOs')
    