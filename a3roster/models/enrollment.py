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
		('dropped', 'Dropped'), ('withdrawn', 'Withdrawn')], default='created',
		required=True, tracking=True)
	
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