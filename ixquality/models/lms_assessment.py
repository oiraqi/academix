from odoo import models, fields

class LmsAssessment(models.Model):
    _inherit = 'ixlms.assessment'

    course_ilo_ids = fields.One2many('ixcatalog.course.ilo', related='course_id.ilo_ids')
    ilo_ids = fields.Many2many(comodel_name='ixcatalog.course.ilo', string='Assessed ILOs')

    good_performance = fields.Binary(string='Good Performance')
    avg_performance = fields.Binary(string='Avg. Performance')
    poor_performance = fields.Binary(string='Poor Performance')

    def get_ilo_achievement(self):
        self.ensure_one()
        domain = [('assessment_id', '=', self.id)]        
        return self._expand_to('ixquality.action_assessed_ilo', domain)