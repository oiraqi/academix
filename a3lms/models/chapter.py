from odoo import models, fields


class Chapter(models.Model):
	_name = 'a3lms.chapter'
	_description = 'Chapter'

	name = fields.Char('Name', required=True)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	start_date = fields.Date(string='Start Date')
	nsessions = fields.Integer(string='Sessions')	
		