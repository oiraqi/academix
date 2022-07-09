from odoo import models, fields


class Resource(models.Model):
	_name = 'ixlms.resource'
	_description = 'Resource'

	name = fields.Char(related='document_id.name')
	chapter_id = fields.Many2one(comodel_name='ixlms.chapter', string='Chapter', required=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', string='Module', required=True)
	course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)
	document_id = fields.Many2one(comodel_name='ixdms.document', string='Document')
	file = fields.Binary(related='document_id.file')
	url = fields.Char(related='document_id.url')	
	