from odoo import models, fields


class Enrollment(models.Model):
	_name = 'a3roster.enrollment'
	_inherit = 'mail.thread'
	_description = 'Enrollment'
	_sql_constraints = [('student_section_ukey', 'unique(student_id, section_id)', 'Student already enrolled in this section')]

	name = fields.Char('Name', compute='_set_name')
	student_id = fields.Many2one(comodel_name='a3.student', string='Student', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section', required=True)
	state = fields.Selection(string='State', selection=[('created', 'Created'), ('enrolled', 'Enrolled'),
		('dropped', 'Dropped'), ('w', 'Withdrawn - W'), ('wf', 'WF'), ('wp', 'WP'), ('ip', 'IP')], default='created',
		required=True, tracking=True)
	wstate = fields.Selection(string='WState', selection=[('wreq', 'Request To Withdraw'), ('wadv', 'W Approved by Advisor'), ('winst', 'W Approved by Instructor'),
		('wfreq', 'WF Request'), ('wpreq', 'WP Request'), ('ipreq', 'IP Request')], tracking=True)
	school_id = fields.Many2one(comodel_name='a3.school', string='School', related='section_id.school_id', store=True)
	discipline_id = fields.Many2one(comodel_name='a3.discipline', string='Discipline', related='section_id.course_id.discipline_id', store=True)
	term_id = fields.Many2one(comodel_name='a3.term', string='Term', related='section_id.term_id', store=True)
	
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

	def withdraw(self):
		for rec in self:
			rec.state = 'withdrawn'

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