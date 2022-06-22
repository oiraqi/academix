from odoo import models, fields, api


class Attendance(models.Model):
	_name = 'a3lms.attendance'
	_description = 'Attendance'

	name = fields.Char('Name', compute='_set_name')
	course_id = fields.Many2one(comodel_name='a3lms.course', string='Course', required=True)
	day = fields.Date(string='Date', required=True, default= lambda self: fields.Date.today())
	attendance_line_ids = fields.One2many(comodel_name='a3lms.attendance.line', inverse_name='attendance_id', string='Attendance Lines')
	
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
