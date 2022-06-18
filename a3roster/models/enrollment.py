from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
	_name = 'a3roster.enrollment'
	_inherit = 'mail.thread'
	_description = 'Enrollment'
	_sql_constraints = [('student_section_ukey', 'unique(student_id, section_id)', 'Student already enrolled in this section')]

	name = fields.Char('Name', compute='_set_name')
	student_id = fields.Many2one(comodel_name='a3.student', string='Student', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section', required=True)
	state = fields.Selection(string='State', selection=[('created', 'Created'), ('enrolled', 'Enrolled'),
		('dropped', 'Dropped'), ('passed', 'Passed'), ('failed', 'Failed'), ('w', 'W'), ('wf', 'WF'), ('wp', 'WP'), ('ip', 'IP')], default='created',
		required=True, tracking=True)
	wstate = fields.Selection(string='WState', selection=[('wreq', 'Request To Withdraw'), ('wadv', 'W Approved by Advisor'), ('winst', 'W Approved by Instructor'),
		('wfreq', 'WF Request'), ('wpreq', 'WP Request'), ('ipreq', 'IP Request')], tracking=True)
	wdtime = fields.Datetime()
	school_id = fields.Many2one(comodel_name='a3.school', string='School', related='section_id.school_id', store=True)
	discipline_id = fields.Many2one(comodel_name='a3.discipline', string='Discipline', related='section_id.course_id.discipline_id', store=True)
	term_id = fields.Many2one(comodel_name='a3.term', string='Term', related='section_id.term_id', store=True)
	sid = fields.Char(related="student_id.sid")
	program_id = fields.Many2one(comodel_name='a3catalog.program', related='student_id.program_id', store=True)

	@api.constrains('student_id', 'section_id')
	def _check(self):
		for rec in self:
			if rec.student_id and rec.section_id:
				# From a performance perspective, we should start with the cheap is_open check,
				# then the time conflict check, and only then, the prerequisites check.
				# However, for a more pertinent feedback to the user, we deem it's worth it to start
				# with the more expensive prerequisites check.
				self.env['a3roster.enrollment'].check_prerequisites(rec.student_id, rec.section_id.course_id)				
				if not rec.section_id.is_open:
					raise ValidationError('Section closed!')
				self.env['a3roster.enrollment'].check_time_conflict(rec.student_id, rec.section_id)

	@api.model
	def check_prerequisites(self, student, course):
		for prerequisite in course.prerequisite_ids:
			alternatives = []
			for alternative in prerequisite.alternative_ids:
				alternatives.append(alternative.name)
				fulfilled = False
				if self.search([('student_id', '=', student.id), ('section_id.course_id', '=', alternative.id), ('state', '=', 'passed')]):
					fulfilled = True
					break
				if not fulfilled:
					if len(alternatives) > 1:
						raise ValidationError('None of these alternative prerequisites is fulfilled: ' + str(alternatives))
					else:
						raise ValidationError('Unfulfilled prerequisite: ' + alternatives[0])
				
	
	@api.model
	def check_time_conflict(self, student, section):
		current_sections = self.search([('student_id', '=', student.id), ('term_id', '=', section.term_id.id), ('state', '=', 'enrolled')])
		for sec in current_sections:
			if section.start_time <= sec.end_time and section.end_time >= sec.start_time:
				raise ValidationError('Time Conflict with ' + sec.name + ': ' + sec.timeslot)
	
	@api.onchange('student_id', 'section_id')
	def _set_name(self):
		for rec in self:
			if rec.student_id and rec.section_id:
				rec.name = rec.student_id.name + ' / ' + rec.section_id.name
			else:
				rec.name = ''

	def enroll(self):
		for rec in self:
			rec.state = 'enrolled'

	def drop(self):
		for rec in self:
			rec.state = 'dropped'
			rec.wdtime = fields.Datetime.now()

	def withdraw(self):
		for rec in self:
			rec.state = 'withdrawn'
			rec.wdtime = fields.Datetime.now()

	def req_to_w(self):
		return

	def req_to_wp(self):
		return

	def req_to_wf(self):
		return

	def req_to_ip(self):
		return

	def app_w_adv(self):
		return

	def app_w_ins(self):
		return
	
	def app_wp(self):
		return

	def app_wf(self):
		return

	def app_ip(self):
		return