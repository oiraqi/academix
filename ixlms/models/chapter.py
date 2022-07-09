from odoo import models, fields


class Chapter(models.Model):
	_name = 'ixlms.chapter'
	_description = 'Chapter'
	_order = "sequence"

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence')	
	module_id = fields.Many2one(comodel_name='ixlms.module', string='Module', required=True)
	course_id = fields.Many2one(comodel_name='ixlms.course', related='module_id.course_id', store=True)
	start_date = fields.Date(string='Start Date')
	nsessions = fields.Integer(string='Sessions')
	resource_ids = fields.One2many(comodel_name='ixlms.resource', inverse_name='chapter_id', string='Resources')
	nresources = fields.Integer(string='Resources', compute='_nresources')

	def _nresources(self):
		for rec in self:
			rec.nresources = len(rec.resource_ids)
	
	
		