from odoo import models, fields


class Chapter(models.Model):
	_name = 'ixlms.chapter'
	_description = 'Chapter'
	_order = "sequence"
	_sql_constraints = [('course_sequence_ukey', 'unique(course_id, sequence)', 'Duplicate chapter sequence!')]

	name = fields.Char('Name', required=True)
	sequence = fields.Integer('Ch.', required=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', string='Module', required=True)
	course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)
	start_date = fields.Date(string='Start Date')
	nsessions = fields.Integer(string='Sessions')
	resource_ids = fields.Many2many(comodel_name='ixlms.resource', string='Resources')
	nresources = fields.Integer(string='Resources', compute='_nresources')
	module_ids = fields.One2many(comodel_name='ixlms.module', related='course_id.module_ids')

	def _nresources(self):
		for rec in self:
			rec.nresources = len(rec.resource_ids)
	
	
		