from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
	assess_by = fields.Selection(string='Group Assessment Grading By', selection=[('module', 'Module'), ('technique', 'Technique'),], default='module', required=True)
	attendance_weight = fields.Float(string='Attendance Weight (%)', compute='_attendance_weight')

	@api.onchange('assess_by', 'module_ids', 'weighted_technique_ids')
	def _attendance_weight(self):
		for rec in self:
			sum_weights = 0
			if rec.assess_by == 'module' and rec.module_ids:
				sum_weights = sum([module.weight for module in rec.module_ids])
				if sum_weights > 100:						
					raise ValidationError('The sum of module weights must be <= 100%')
			elif rec.assess_by == 'technique' and rec.weighted_technique_ids:
				sum_weights = sum([weighted_technique.weight for weighted_technique in rec.weighted_technique_ids])
				if sum_weights > 100:						
					raise ValidationError('The sum of technique weights must be <= 100%')
			rec.attendance_weight = 100 - sum_weights


	attendance_grading = fields.Selection(string='Attendance Grading', selection=[('rate', 'Attendance Rate'),
		('ratez', 'Attendance Rate but Zero after'), ('penalty', 'Penalty(%) / Absence')], default='rate')
	absence_limit = fields.Integer(string='Max Absences', default=5)
	penalty_per_absence = fields.Float(string='Penalty(%) / Absence', default=5.0)
	module_ids = fields.One2many(comodel_name='a3lms.module', inverse_name='course_id', string='Modules')
	weighted_technique_ids = fields.One2many(comodel_name='a3lms.weighted.technique', inverse_name='course_id', string='Techniques')
	assessment_technique_ids = fields.One2many(comodel_name='a3lms.assessment.technique', compute='_assessment_techniques')
	
	@api.onchange('assess_by', 'weighted_technique_ids')
	def _assessment_techniques(self):
		for rec in self:
			if rec.assess_by == 'technique' and rec.weighted_technique_ids:
				rec.assessment_technique_ids = [weighted_technique.technique_id.id for weighted_technique in rec.weighted_technique_ids]
			else:
				rec.assessment_technique_ids = self.env['a3lms.assessment.technique'].search([])
	
	assessment_ids = fields.One2many(comodel_name='a3lms.assessment', inverse_name='course_id', string='Assessments')
	used_technique_ids = fields.One2many(comodel_name='a3lms.assessment.technique', compute='_used_techniques')
	
	@api.onchange('assessment_ids')
	def _used_technique_ids(self):
		for rec in self:
			if rec.assessment_ids:
				rec.used_technique_ids = [assessment.technique_id.id for assessment in rec.assessment_ids]
			else:
				rec.used_technique_ids = False
	
	details = fields.Html(string='More Details')
	
	
	