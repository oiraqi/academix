from odoo import models, fields


class Node(models.Model):
	_name = 'ixdms.node'
	_description = 'Node'
	_inherit = ['mail.thread', 'ix.expandable']
	_order = 'type,name'

	name = fields.Char('Name', required=True)
	type = fields.Selection(string='Type', selection=[('1', 'Folder'), ('2', 'Document')], default='2', required=True)
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

	folder_ids = fields.One2many(comodel_name='ixdms.folder', inverse_name='parent_id', domain=[('type', '=', '1')], string='Sub-Folders')
	nfolders = fields.Integer(string='Sub-Folders', compute='_nfolders')

	def _nfolders(self):
		for rec in self:
			rec.nfolders = len(rec.folder_ids)

	document_ids = fields.One2many(comodel_name='ixdms.document', inverse_name='folder_id', domain=[('type', '=', '2')], string='Documents')
	ndocuments = fields.Integer(string='Documents', compute='_ndocuments')

	def _ndocuments(self):
		for rec in self:
			rec.ndocuments = len(rec.document_ids)

	read_user_ids = fields.Many2many(comodel_name='res.users', string='Read Access Users')
	write_user_ids = fields.Many2many(comodel_name='res.users', string='Write Access Users')
	read_group_ids = fields.Many2many(comodel_name='res.group', string='Read Access Groups')
	write_group_ids = fields.Many2many(comodel_name='res.group', string='Write Access Groups')

	rshared = fields.Boolean(compute='_rshared')
	wshared = fields.Boolean(compute='_wshared')

	def _rshared(self):
		for rec in self:
			rec.rshared = len(rec.read_user_ids) > 0 or len(rec.read_group_ids) > 0
	
	def _wshared(self):
		for rec in self:
			rec.wshared = len(rec.write_user_ids) > 0 or len(rec.write_group_ids) > 0

	def open(self):
		self.ensure_one()
		domain = [('id', '=', self.id)]
		return self._expand_to('ixdms.action_node_open', domain, False, self.id)
