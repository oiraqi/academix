from odoo import models, fields


class Chapter(models.Model):
	_name = 'a3lms.chapter'
	_description = 'Chapter'
	_order = "sequence"

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence')	
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	course_id = fields.Many2one(comodel_name='a3lms.course', related='module_id.course_id', store=True)
	start_date = fields.Date(string='Start Date')
	nsessions = fields.Integer(string='Sessions')	
		