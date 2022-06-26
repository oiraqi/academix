from odoo import models, fields


class Chapter(models.Model):
	_name = 'a3lms.chapter'
	_description = 'Chapter'
	_order = "sequence"

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence')	
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	module_id = fields.Many2one(comodel_name='a3lms.module', string='Module', required=True)
	start_date = fields.Date(string='Start Date')
	nsessions = fields.Integer(string='Sessions')
	module_ids = fields.One2many(comodel_name='a3lms.module', related='course_id.module_ids')
		