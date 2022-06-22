from odoo import models, fields


class AttendanceLine(models.Model):
	_name = 'a3lms.attendance.line'
	_description = 'AttendanceLine'

	student_id = fields.Many2one(comodel_name='a3.student', string='Student', required=True)
	attendance_id = fields.Many2one(comodel_name='a3lms.attendance', string='Attendance', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', related='attendance_id.section_id', store=True)	
	state = fields.Selection(string='State', selection=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], default='Present', required=True)
	excused = fields.Boolean(string='Excused', default='False')	
	program_id = fields.Many2one(comodel_name='a3catalog.program', string='Program', related='student_id.program_id', store=True)
	school_id = fields.Many2one(comodel_name='a3.school', string='School', related='attendance_id.course_id.section_id.school_id', store=True)	
		