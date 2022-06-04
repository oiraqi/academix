from odoo import api, fields, models


class CourseProgram(models.Model):
    _name = 'a3quality.course.program'
    _description = 'Course Program Mapping'
    _sql_constraints = [('a3quality_course_program_ukey', 'unique(course_id, program_id)', 'Course/Program mapping already exists')]

    course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)
    program_id = fields.Many2one(comodel_name='a3catalog.program', string='Program', required=True)
    ilo_so_ids = fields.One2many(comodel_name='a3quality.course.ilo.so', inverse_name='course_program_id', string='Outcome Mapping')
    discipline_id = fields.Many2one(comodel_name='a3.discipline', related='course_id.discipline_id', store=True)
    school_id = fields.Many2one(comodel_name='a3.school', related='course_id.school_id', store=True)
    ilo_ids = fields.One2many('a3catalog.course.ilo', related='course_id.ilo_ids', string="Course ILOs")
    so_ids = fields.One2many('a3quality.student.outcome', related='program_id.so_ids', string="Program SOs")
