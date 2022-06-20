from odoo import models, fields


class LmsCourse(models.Model):
	_name = 'a3lms.course'
	_description = 'LMS Course'
	_inherit = ['a3.activity']
	_sql_constraints = [('section_ukey', 'unique(section_id)', 'LMS course already created!')]

	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section', required=True)	
	name = fields.Char(related='section_id.name')	
	course_id = fields.Many2one(comodel_name='a3.course', related='section_id.course_id')
	instructor_id = fields.Many2one(comodel_name='a3.faculty', related='section_id.instructor_id')
	discipline_id = fields.Many2one(comodel_name='a3.discipline', related='section_id.discipline_id')
	timeslot = fields.Char(related='section_id.timeslot')	
	room_id = fields.Many2one(comodel_name='a3.room', related='section_id.room_id')
	description = fields.Html(related='course_id.description')
	ilo_ids = fields.One2many('a3catalog.course.ilo', related='course_id.ilo_ids')
	textbook_ids = fields.One2many(comodel_name='a3lms.textbook', related='course_id.textbook_ids')
	office_hour_ids = fields.One2many(comodel_name='a3roster.office.hour', related='instructor_id.office_hour_ids')
	assessment_technique_ids = fields.Many2many(comodel_name='a3lms.assessment.technique', string='Assessment Techniques', required=True)
	assess_by = fields.Selection(string='Group Assessment Grading By', selection=[('technique', 'Technique'), ('module', 'Module'),], required=True)
	attendance_weight = fields.Float(string='Attendance Weight (%)', default=0.0)
	attendance_grading = fields.Selection(string='Attendance Grading', selection=[('rate', 'Attendance Rate'),
		('ratez', 'Attendance Rate but Zero after'), ('penalty', 'Penalty/Absence')], default='rate')
	absence_limit = fields.Integer(string='Max Absences', default=5)
	penalty_per_absence = fields.Float(string='Penalty/Absence', default=5.0)
	module_ids = fields.One2many(comodel_name='a3lms.module', inverse_name='course_id', string='Modules')
	weighted_technique_ids = fields.One2many(comodel_name='a3lms.weighted.technique', inverse_name='course_id', string='Techniques')
	
	
	details = fields.Html(string='More Details')
	
	
	