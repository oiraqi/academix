from odoo import models, fields, api


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
	student_ids = fields.One2many('a3.student', related='section_id.student_ids')
	nstudents = fields.Integer(related='section_id.nstudents')
	description = fields.Html(related='course_id.description')
	ilo_ids = fields.One2many('a3catalog.course.ilo', related='course_id.ilo_ids')
	textbook_ids = fields.One2many(comodel_name='a3lms.textbook', related='course_id.textbook_ids')
	office_hour_ids = fields.One2many(comodel_name='a3roster.office.hour', related='instructor_id.office_hour_ids')
	grade_grouping = fields.Selection(string='Assessment Grouping', selection=[('module', 'Course Module'), ('technique', 'Assessment Technique'),], default='module', required=True)
	grade_weighting = fields.Selection(string='Assessment Weighting', selection=[('percentage', '%'), ('points', 'Points'),], default='percentage', required=True)	
	attendance_points = fields.Integer(string='Attendance Points', default=0)
	attendance_percentage = fields.Float(string='Attendance %', compute='_attendance_percentage')
	attendance_weight = fields.Float(compute='_attendance_weight')

	@api.onchange('grade_grouping', 'module_ids', 'technique_ids')
	def _attendance_percentage(self):
		for rec in self:
			if rec.grade_grouping == 'module' and rec.module_ids:
				module_percentages = sum([module.percentage for module in rec.module_ids])
				if module_percentages <= 100:
					rec.attendance_percentage = 100 - module_percentages
					return
			elif rec.grade_grouping == 'technique' and rec.technique_ids:
				technique_percentages = sum([technique.percentage for technique in rec.technique_ids])
				if technique_percentages <= 100:
					rec.attendance_percentage = 100 - technique_percentages
					return
			rec.attendance_percentage = 0.0
	
	@api.onchange('grade_weighting', 'attendance_percentage', 'attendance_points')
	def _attendance_weight(self):
		for rec in self:
			if rec.grade_weighting == 'percentage':
				rec.attendance_weight = rec.attendance_percentage
			elif rec.grade_weighting == 'points':
				rec.attendance_weight = float(rec.attendance_points)
			else:
				rec.attendance_weight = 0.0

	attendance_grading = fields.Selection(string='Attendance Grading', selection=[('rate', 'Attendance Rate'),
		('penalty', 'Penalty / Absence')], default='rate')	
	penalty_per_absence = fields.Float(string='Penalty(%) / Absence', default=5.0)
	zero_after_max_abs = fields.Boolean(string='Zero after Max Absences', default=False)	
	max_absences = fields.Integer(string='Max Absences', default=5)
	module_ids = fields.One2many(comodel_name='a3lms.module', inverse_name='course_id', string='Modules')
	technique_ids = fields.One2many(comodel_name='a3lms.weighted.technique', inverse_name='course_id', string='Techniques')	
	assessment_ids = fields.One2many(comodel_name='a3lms.assessment', inverse_name='course_id', string='Assessments')
	nassessments = fields.Integer(string='Number of Assessments', compute='_assessment_ids')	
	used_technique_ids = fields.One2many(comodel_name='a3lms.assessment.technique', compute='_assessment_ids')
	
	@api.onchange('assessment_ids')
	def _assessment_ids(self):
		for rec in self:
			if rec.assessment_ids:
				rec.used_technique_ids = [assessment.technique_id.id for assessment in rec.assessment_ids]
				rec.nassessments = len(rec.assessment_ids)
			else:
				rec.used_technique_ids = False
				rec.nassessments = 0
	
	details = fields.Html(string='More Details')
	
	
	