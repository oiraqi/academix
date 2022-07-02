from odoo import models, fields

class LmsChapter(models.Model):
    _inherit = 'ixlms.chapter'

    course_ilo_ids = fields.One2many('ixcatalog.course.ilo', related='course_id.course_id.ilo_ids')
    ilo_ids = fields.Many2many(comodel_name='ixcatalog.course.ilo', string='Covered ILOs')
    