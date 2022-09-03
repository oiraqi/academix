from odoo import models, fields


class StudentInfo(models.Model):
	_name = 'ixadmission.student.info'
	_description = 'StudentInfo'

	name = fields.Char('Name', required=True)
	