from odoo import models, fields


class AttendanceLine(models.Model):
	_name = 'ixlms.attendance.line'
	_description = 'AttendanceLine'

	name = fields.Char(related='student_id.name')	
	student_id = fields.Many2one(comodel_name='ix.student', string='Student', required=True)	
	attendance_id = fields.Many2one(comodel_name='ixlms.attendance', string='Attendance', required=True)
	section_id = fields.Many2one(comodel_name='ixroster.section', related='attendance_id.section_id', store=True)	
	state = fields.Selection(string='State', selection=[('present', 'Present'), ('absent', 'Absent - Unexcused'), ('late', 'Late'), ('absentx', 'Absent - Excused')], default='present', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', related='student_id.program_id', store=True)
	school_id = fields.Many2one(comodel_name='ix.school', string='School', related='attendance_id.course_id.section_id.school_id', store=True)
	day = fields.Date(related='attendance_id.day', store=True)
		