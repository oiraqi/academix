from odoo import models, fields, api


class Attendance(models.Model):
	_name = 'a3lms.attendance'
	_description = 'Attendance'

	name = fields.Char('Name', compute='_set_name')
	course_id = fields.Many2one(comodel_name='a3lms.course', string='Course', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='course_id.section_id', store=True)
	term_id = fields.Many2one(comodel_name='a3.term', related='course_id.section_id.term_id', store=True)
	school_id = fields.Many2one(comodel_name='a3.school', related='course_id.section_id.school_id', store=True)
	instructor_id = fields.Many2one(comodel_name='a3.faculty', related='course_id.section_id.instructor_id')
	day = fields.Date(string='Date', required=True, default= lambda self: fields.Date.today())
	attendance_line_ids = fields.One2many(comodel_name='a3lms.attendance.line', inverse_name='attendance_id', string='Attendance Lines')
	npresent = fields.Integer(string='Present Students', compute='_stats')
	nabsent = fields.Integer(string='Absent Students', compute='_stats')
	nlate = fields.Integer(string='Late Students', compute='_stats')
	
	@api.onchange('attendance_line_ids')
	def _stats(self):
		for rec in self:
			if rec.attendance_line_ids:
				npresent = nabsent = nlate = 0
				for line in rec.attendance_line_ids:
					if line.state == 'present':
						npresent += 1
					elif line.state == 'absent':
						nabsent += 1
					elif line.state == 'late':
						nlate += 1
				rec.npresent = npresent
				rec.nabsent = nabsent
				rec.nlate = nlate
			else:
				rec.npresent = 0
				rec.nabsent = 0
				rec.nlate = 0
	
	
	def _set_name(self):
		for rec in self:
			if rec.course_id and rec.day:
				rec.name = 'Attendance / ' + rec.course_id.name + ' / ' + rec.day
			else:
				rec.name = ''

	@api.onchange('course_id')
	def _onchange_course_id(self):
		for rec in self:
			if rec.course_id and rec.course_id.student_ids:
				attendance_lines = []
				for student in rec.course_id.student_ids:
					attendance_line = self.env['a3lms.attendance.line'].new({
						'student_id': student.id,
						'attendance_id': rec.id,
						'state': 'present',
					})
					attendance_lines.append(attendance_line.id)
				rec.attendance_line_ids = attendance_lines