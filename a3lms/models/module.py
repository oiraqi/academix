from odoo import models, fields


class Module(models.Model):
	_name = 'a3lms.module'
	_description = 'Module'

	name = fields.Char('Name', required=True)
	weight = fields.Float(string='Weight (%)', required=True, default=0.0)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
		
	