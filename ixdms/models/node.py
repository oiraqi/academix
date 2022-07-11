from odoo import models, fields


class Node(models.Model):
	_name = 'ixdms.node'
	_description = 'Node'

	name = fields.Char('Name', required=True)
	type = fields.Selection(string='Type', selection=[('document', 'Document'), ('folder', 'Folder')], default='document', required=True)
	color = fields.Integer(string='Color')	
	tag_ids = fields.Many2many(comodel_name='ixdms.tag', string='Tags')
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')
	parent_id = fields.Many2one(comodel_name='ixdms.node', string='Parent')
	child_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', string='Content')
	nchildren = fields.Integer(string='Sub-Folders', compute='_nchildren')

	def _nchildren(self):
		for rec in self:
			rec.nchildren = len(rec.child_ids)

	def open(self):
		self.ensure_one()
		domain = [('id', '=', self.id)]
		return self._expand_to('ixdms.action_node_open', domain, False, self.id)
