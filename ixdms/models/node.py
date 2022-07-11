from odoo import models, fields


class Node(models.Model):
	_name = 'ixmds.node'
	_description = 'Node'

	name = fields.Char('Name', required=True)
	type = fields.Selection(string='Type', selection=[('document', 'Document'), ('folder', 'Folder')], default='folder')	
	tag_ids = fields.Many2many(comodel_name='ixdms.tag', string='Tags')
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')
	parent_id = fields.Many2one(comodel_name='ixdms.node', string='Parent')
	folder_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', domain=[('type', '=', 'folder')], string='Sub-Folders')
	nfolders = fields.Integer(string='Sub-Folders', compute='_nfolders')

	def _nfolders(self):
		for rec in self:
			rec.nfolders = len(rec.folder_ids)

	document_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', domain=[('type', '=', 'document')], string='Documents')
	ndocuments = fields.Integer(string='Documents', compute='_ndocuments')

	def _ndocuments(self):
		for rec in self:
			rec.ndocuments = len(rec.document_ids)

	def open(self):
		self.ensure_one()
		domain = [('id', '=', self.id)]
		return self._expand_to('ixdms.action_node_open', domain, False, self.id)
