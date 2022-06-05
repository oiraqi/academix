from odoo import api, fields, models


class Prerequisite(models.Model):
    _name = 'a3catalog.prerequisite'
    _description = 'Course Prerequisite'

    course_id = fields.Many2one('a3.course', string='Course')
    alternative_ids = fields.Many2many('a3.course', string='Prerequisite')
    sequence = fields.Integer(default='1', required=True)
