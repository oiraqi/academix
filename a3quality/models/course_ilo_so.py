from odoo import api, fields, models


class CourseIlOSO(models.Model):
    _name = 'a3quality.course.ilo.so'
    _description = 'Course ILO & SO Mapping'

    course_ilo_id = fields.Many2one(comodel_name='a3catalog.course.ilo', string='ILO', required=True)
    so_id = fields.Many2one(comodel_name='a3quality.student.outcome', string='SO', required=True)
    course_program_id = fields.Many2one(comodel_name='a3quality.course.program', string='Course/Program', required=True)    
    level = fields.Selection(string='Level', selection=[('introduce', 'Introduce'), ('reinforce', 'Reinforce'), ('emphasize', 'Emphasize')], default='introduce', required=True)
    