from odoo import models, fields


class Node(models.Model):
	_name = 'ixdms.node'
	_description = 'Node'
	_inherit = ['mail.thread', 'ix.expandable']
	_order = 'type,name'
	_sql_constraints = [('name_type_parent_ukey', 'unique(name, type, parent_id)', 'Duplicate name!')]

	name = fields.Char('Name', required=True)
	type = fields.Selection(string='Type', selection=[('1', 'Folder'), ('2', 'Document')], default='2', required=True)
	color = fields.Integer(string='Color')	
	tag_ids = fields.Many2many(comodel_name='ixdms.tag', string='Tags')
	ntags = fields.Integer(compute='_ntags')

	def _ntags(self):
		for rec in self:
			rec.ntags = len(rec.tag_ids)
	
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')
	parent_id = fields.Many2one(comodel_name='ixdms.node', string='Parent')
	child_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', string='Content')
	nchildren = fields.Integer(string='Sub-Folders', compute='_nchildren')

	def _nchildren(self):
		for rec in self:
			rec.nchildren = len(rec.child_ids)

	folder_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', domain=[('type', '=', '1')], string='Sub-Folders')
	nfolders = fields.Integer(string='Sub-Folders', compute='_nfolders')

	def _nfolders(self):
		for rec in self:
			rec.nfolders = len(rec.folder_ids)

	document_ids = fields.One2many(comodel_name='ixdms.node', inverse_name='parent_id', domain=[('type', '=', '2')], string='Documents')
	ndocuments = fields.Integer(string='Documents', compute='_ndocuments')

	def _ndocuments(self):
		for rec in self:
			rec.ndocuments = len(rec.document_ids)

	read_user_ids = fields.Many2many(comodel_name='res.users', relation='ixdms_read_node_user_rel', string='Read Access Users')
	write_user_ids = fields.Many2many(comodel_name='res.users', relation='ixdms_write_node_user_rel', string='Write Access Users')
	read_group_ids = fields.Many2many(comodel_name='res.groups', relation='ixdms_read_node_groups_rel', string='Read Access Groups')
	write_group_ids = fields.Many2many(comodel_name='res.groups', relation='ixdms_write_node_groups_rel', string='Write Access Groups')

	shared = fields.Boolean(compute='_shared')	

	def _shared(self):
		for rec in self:
			rec.shared = rec._rec_shared()
			
	def _rec_shared(self):
		if len(self.read_user_ids) > 0 or len(self.read_group_ids) > 0:
			return True
		if not self.parent_id:
			return False
		return self.parent_id._rec_shared()
	

	def open(self):
		self.ensure_one()
		domain = [('id', '=', self.id)]
		context = {'default_parent_id': self.id}
		return self._expand_to('ixdms.action_node_open', domain, context, self.id)
