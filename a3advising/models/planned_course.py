from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PlannedCourse(models.Model):
    _name = 'a3advising.planned.course'
    _description = 'Planned Course'
    _inherit = ['a3.student.owned', 'a3.activity']
    _sql_constraints = [('a3advising_planned_course_ukey', 'unique(course_id, student_id)', 'Course already planned!')]

    course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)
    name = fields.Char(string='Name', compute='_set_name')
    description = fields.Html(related='course_id.description')
    grade = fields.Selection(string='Grade', selection=[('p', 'P'), ('f', 'F')], default='p')


    @api.constrains('semester_year')
    def _check_max_courses(self):
        for rec in self:
            if self.env['a3advising.planned.course'].search_count(
                [('semester_year', '=', rec.semester_year)]) > 6:
                raise ValidationError('Max allowed number of courses exceeded!')

    
    @api.onchange('course_id')
    def _set_name(self):
        for rec in self:
            if rec.course_id:
                rec.name = rec.course_id.name

