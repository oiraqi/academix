from odoo import api, fields, models


class Corequisite(models.Model):
    _name = 'a3catalog.corequisite'
    _description = 'Course Corequisite'
    _sql_constraints = [('a3catalog_corequisite_ukey', 'unique(course_id, corequisite_id)', 'The same corequisite has been added several times!')]

    course_id = fields.Many2one('a3.course', string='Course')
    corequisite_id = fields.Many2one('a3.course', string='Corequisite')
    sequence = fields.Integer(default='1', required=True)
