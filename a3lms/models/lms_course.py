from multiprocessing import context
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LmsCourse(models.Model):
	_name = 'a3lms.course'
	_description = 'LMS Course'
	_inherit = ['a3.activity', 'a3.expandable']
	_sql_constraints = [('section_ukey', 'unique(section_id)', 'LMS course already created!')]

	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section', required=True)	
	name = fields.Char(related='section_id.name')	
	course_id = fields.Many2one(comodel_name='a3.course', related='section_id.course_id')
	instructor_id = fields.Many2one(comodel_name='a3.faculty', related='section_id.instructor_id')
	discipline_id = fields.Many2one(comodel_name='a3.discipline', related='section_id.discipline_id')
	timeslot = fields.Char(related='section_id.timeslot')	
	room_id = fields.Many2one(comodel_name='a3.room', related='section_id.room_id')
	student_ids = fields.One2many('a3.student', related='section_id.student_ids')
	enrollment_ids = fields.One2many('a3roster.enrollment', related='section_id.enrollment_ids')
	nstudents = fields.Integer(related='section_id.nstudents')
	description = fields.Html(related='course_id.description')
	ilo_ids = fields.One2many('a3catalog.course.ilo', related='course_id.ilo_ids')
	textbook_ids = fields.One2many(comodel_name='a3lms.textbook', related='course_id.textbook_ids')
	office_hour_ids = fields.One2many(comodel_name='a3roster.office.hour', related='instructor_id.office_hour_ids')
	grade_grouping = fields.Selection(string='Assessment Grouping', selection=[('module', 'Course Module'), ('technique', 'Assessment Technique'),], default='module', required=True)
	grade_weighting = fields.Selection(string='Assessment Weighting', selection=[('percentage', 'Percentage'), ('points', 'Points'),], default='percentage', required=True)	
	attendance_points = fields.Integer(string='Attendance Points', default=0)
	attendance_percentage = fields.Float(string='Attendance %', compute='_attendance_percentage')
	attendance_weight = fields.Float(compute='_attendance_weight')

	@api.onchange('assessment_ids')
	def _attendance_percentage(self):
		for rec in self:			
			assessment_percentages = sum([assessment.percentage for assessment in rec.assessment_ids])
			if assessment_percentages <= 100:
				rec.attendance_percentage = 100 - assessment_percentages
			else:
				rec.attendance_percentage = 0.0
				raise ValidationError('The sum of assessment percentages cannot exceed 100%')
				
	
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
	assessed_module_ids = fields.One2many(comodel_name='a3lms.module', compute='_assessed_module_ids', string='Modules')	

	@api.onchange('assessment_ids')
	def _assessed_module_ids(self):
		for rec in self:
			assessed_module_ids = [assessment.module_id.id for assessment in rec.assessment_ids]
			rec.assessed_module_ids = self.env['a3lms.module'].search([('id', 'in', assessed_module_ids)])

	technique_ids = fields.One2many(comodel_name='a3lms.weighted.technique', inverse_name='course_id', string='Techniques')	
	assessment_ids = fields.One2many(comodel_name='a3lms.assessment', inverse_name='course_id', string='Assessments')
	nassessments = fields.Integer(string='Number of Assessments', compute='_assessment_ids')
	nassessment_lines = fields.Integer(string='Number of Assessment Lines', compute='_assessment_ids')
	used_technique_ids = fields.One2many(comodel_name='a3lms.assessment.technique', compute='_assessment_ids')
	attendance_ids = fields.One2many(comodel_name='a3lms.attendance', inverse_name='course_id', string='Attendance Sheets')
	nattendance_sheets = fields.Integer(string='Number of Attendance Sheets', compute='_attendance_ids')
	team_ids = fields.One2many(comodel_name='a3lms.team', inverse_name='course_id', string='Teams')
	chapter_ids = fields.One2many(comodel_name='a3lms.chapter', inverse_name='course_id', string="Chapters & Timeline")

	def _chapter_ids

	def _attendance_ids(self):
		for rec in self:
			rec.nattendance_sheets = len(rec.attendance_ids)
	
	@api.onchange('assessment_ids')
	def _assessment_ids(self):
		for rec in self:
			if rec.assessment_ids:
				rec.used_technique_ids = [assessment.technique_id.id for assessment in rec.assessment_ids]
				rec.nassessments = len(rec.assessment_ids)
				rec.nassessment_lines = self.env['a3lms.assessment.line'].search_count([('course_id', '=', rec.id), ('student_id', 'in', rec.student_ids.ids)])
			else:
				rec.used_technique_ids = False
				rec.nassessments = 0
				rec.nassessment_lines = 0
	
	details = fields.Html(string='More Details')

	@api.constrains('grade_weighting', 'assessment_ids')
	def _check_sum_percentages(self):
		for rec in self:
			if rec.grade_weighting != 'percentage' or not rec.assessment_ids:
				continue
			
			if sum([assessment.percentage for assessment in rec.assessment_ids]) > 100:
				raise ValidationError('The sum of assessment percentages cannot exceed 100%')
		
	def get_students(self):
		self.ensure_one()
		domain = [('section_id', '=', self.section_id.id), ('state', 'in', ['enrolled', 'withdrawn'])]
		return self._resolve_action('a3lms.action_enrollment', domain)

	def get_assessments(self):
		self.ensure_one()
		domain = [('course_id', '=', self.id)]
		if self.grade_grouping == 'module' and self.grade_weighting == 'percentage':
			return self._resolve_action('a3lms.action_assessment_module_percentage', domain)

		if self.grade_grouping == 'module' and self.grade_weighting == 'points':
			return self._resolve_action('a3lms.action_assessment_module_points', domain)
		
		if self.grade_grouping == 'technique' and self.grade_weighting == 'percentage':
			return self._resolve_action('a3lms.action_assessment_technique_percentage', domain)

		if self.grade_grouping == 'technique' and self.grade_weighting == 'points':
			return self._resolve_action('a3lms.action_assessment_technique_points', domain)
		

	def get_grade_matrix(self):
		self.ensure_one()
		domain = [('course_id', '=', self.id), ('student_id', 'in', self.student_ids.ids)]
		group_fields = ['program_id', 'student_id']
		if self.grade_grouping == 'module':
			group_fields.append('module_id')
		elif self.grade_grouping == 'technique':
			group_fields.append('technique_id')
		context = {'group_by': group_fields}
		return self._resolve_action('a3lms.action_assessment_line', domain, context)

	def get_attendance(self):
		self.ensure_one()
		domain = [('course_id', '=', self.id)]
		context = {'default_course_id': self.id}
		return self._resolve_action('a3lms.action_attendance', domain, context)

