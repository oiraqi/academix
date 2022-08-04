from odoo import models, fields


class Resource(models.Model):
	_name = 'ixlms.resource'
	_description = 'Resource'

	name = fields.Char('Name', required=True)
	chapter_id = fields.Many2one(comodel_name='ixlms.chapter', string='Chapter', required=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', related='chapter_id.module_id', store=True)
	course_id = fields.Many2one(comodel_name='ixlms.course', related='chapter_id.module_id.course_id', required=True)
	content = fields.Html(string='Content', required=True)
	
	