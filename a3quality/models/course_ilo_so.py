from odoo import api, fields, models


class CourseIlOSO(models.Model):
    _name = 'a3quality.course.ilo.so'
    _description = 'Course ILO & SO Mapping'
    _sql_constraints = [('a3quality_ilo_so_course_program_so_ukey', 'unique(course_program_id, so_id)', 'SO mapping already exists')]

    ilo_ids = fields.Many2many(comodel_name='a3catalog.course.ilo', string='ILOs')
    so_id = fields.Many2one(comodel_name='a3quality.student.outcome', string='SO', required=True)
    course_program_id = fields.Many2one(comodel_name='a3quality.course.program', string='Course/Program', required=True)    
    level = fields.Selection(string='Level', selection=[('introduce', 'Introduce'), ('reinforce', 'Reinforce'), ('emphasize', 'Emphasize')], default='introduce', required=True)
    course_id = fields.Many2one(comodel_name='a3.course', related='course_program_id.course_id', store=True)
    program_id = fields.Many2one(comodel_name='a3catalog.program', related='course_program_id.program_id', store=True)
    
    