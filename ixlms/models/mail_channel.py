from odoo import models, fields

class MailChannel(models.Model):
    _inherit = 'mail.channel'

    course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course')
    