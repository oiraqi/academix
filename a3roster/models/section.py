from odoo import api, fields, models


class Section(models.Model):
    _name = 'a3roster.section'
    _description = 'Course Section'
    _inherit = 'a3.activity'
    _order = 'course_id,number'
    _sql_constraints = [('a3roster_section_ukey', 'unique(year, semester, course_id, number)', 'Section already exists')]

    name = fields.Char(compute='_compute_name', string='Name', store=True)
    
    @api.depends('course_id', 'number', 'year', 'semester')
    @api.onchange('course_id', 'number', 'year', 'semester')
    def _compute_name(self):
        for rec in self:
            if rec.course_id and rec.number and rec.year and rec.semester:
                rec.name = rec.course_id.code + rec.number + rec.suffix
            else:
                rec.name = ''
    
    course_id = fields.Many2one(comodel_name='a3.course', string='Course', required=True)    
    number = fields.Selection(string='Section', selection=[('01', '01'), ('02', '02'),
                                                          ('03', '03'), ('04', '04'),
                                                          ('05', '05'), ('06', '06'),
                                                          ('07', '07'), ('08', '08'),
                                                          ('09', '09'), ('10', '10')], default='01', required=True)
    school_id = fields.Many2one(comodel_name='a3.school',
                    related='course_id.school_id', readonly=True, store=True)
    discipline_id = fields.Many2one(comodel_name='a3.discipline',
                    related='course_id.discipline_id', readonly=True, store=True)
    instructor_id = fields.Many2one(comodel_name='a3.faculty', string='Instructor')
    classroom_id = fields.Many2one(comodel_name='a3roster.classroom', string='Classroom')
    timeslot_id = fields.Many2one(comodel_name='a3roster.timeslot', string='Timeslot')    
    syllabus = fields.Binary(string='Syllabus')    
    student_ids = fields.Many2many('a3.student', 'a3roster_section_student_rel', 'section_id', 'student_id', 'Students')        
