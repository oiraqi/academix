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
	
	student_share_ids = fields.One2many(comodel_name='ixdms.student.share', inverse_name='node_id', string='Student Shares')
	faculty_share_ids = fields.One2many(comodel_name='ixdms.faculty.share', inverse_name='node_id', string='Faculty Shares')

	implied_read_user_ids = fields.Many2many(comodel_name='res.users', compute='_implied', string='Implied Read Access Users')
	implied_write_user_ids = fields.Many2many(comodel_name='res.users', compute='_implied', string='Implied Write Access Users')
	
	implied_student_share_ids = fields.Many2many(comodel_name='ixdms.student.share', compute='_implied', string='Implied Student Shares')
	implied_faculty_share_ids = fields.Many2many(comodel_name='ixdms.faculty.share', compute='_implied', string='Implied Faculty Shares')
	
	shared = fields.Boolean(compute='_implied')
	write_allowed = fields.Boolean(compute='_implied')
	is_implied = fields.Boolean(compute='_implied')
	

	def _implied(self):
		for rec in self:
			implied_read_user_ids = []
			implied_write_user_ids = []
			implied_student_share_ids = []
			implied_faculty_share_ids = []
			shared = False
			
			rec._rec_implied(implied_read_user_ids, implied_write_user_ids, implied_student_share_ids, implied_faculty_share_ids)

			if len(implied_read_user_ids) > 0:
				rec.implied_read_user_ids = implied_read_user_ids
				shared = True
			else:
				rec.implied_read_user_ids = False
			if len(implied_write_user_ids) > 0:
				rec.implied_write_user_ids = implied_write_user_ids
				shared = True
			else:
				rec.implied_write_user_ids = False
			if len(implied_student_share_ids) > 0:
				rec.implied_student_share_ids = implied_student_share_ids
				shared = True
			else:
				rec.implied_student_share_ids = False
			if len(implied_faculty_share_ids) > 0:
				rec.implied_faculty_share_ids = implied_faculty_share_ids
				shared = True
			else:
				rec.implied_faculty_share_ids = False

			rec.shared = shared or len(rec.read_user_ids) > 0 or len(rec.write_user_ids) > 0 or len(rec.student_share_ids) > 0 or len(rec.faculty_share_ids) > 0
			rec.write_allowed = self.env.user == rec.create_uid or self.env.user in rec.write_user_ids or self.env.user in rec.implied_write_user_ids
			user_id = self.env.user.id
			is_implied = user_id in implied_read_user_ids or user_id in implied_write_user_ids
			if is_implied:
				rec.is_implied = True
				continue
			
			if self.env.ref('ix.group_student') in self.env.user.groups_id:
				student = self.env.user.student_id
				for student_share in rec.implied_student_share_ids:
					if student.school_id == student_share.school_id:
						if student_share.program_id:
							if student_share.program_id == student.program_id:
								is_implied = True
								break
						else:
							is_implied = True
							break
			elif self.env.ref('ix.group_faculty') in self.env.user.groups_id:
				faculty = self.env.user.faculty_id
				for faculty_share in rec.implied_faculty_share_ids:
					if faculty.school_id == faculty_share.school_id:
						if faculty_share.discipline_id:
							if faculty_share.discipline_id == faculty.discipline_id:
								is_implied = True
								break
						else:
							is_implied = True
							break
			
			rec.is_implied = is_implied
			
	def _rec_implied(self, implied_read_user_ids, implied_write_user_ids, implied_student_share_ids, implied_faculty_share_ids):
		if not self.parent_id:
			return

		for read_user in self.parent_id.read_user_ids:
			if read_user.id not in implied_read_user_ids:
				implied_read_user_ids.append(read_user.id)
		
		for write_user in self.parent_id.write_user_ids:
			if write_user.id not in implied_write_user_ids:
				implied_write_user_ids.append(write_user.id)

		for student_share in self.parent_id.implied_student_share_ids:
			if student_share.id not in implied_student_share_ids:
				implied_student_share_ids.append(student_share.id)
		
		for faculty_share in self.parent_id.implied_faculty_share_ids:
			if faculty_share.id not in implied_faculty_share_ids:
				implied_faculty_share_ids.append(faculty_share.id)
		
		return self.parent_id._rec_implied(implied_read_user_ids, implied_write_user_ids, implied_student_share_ids, implied_faculty_share_ids)

	def open(self):
		self.ensure_one()
		domain = [('id', '=', self.id)]
		context = {'default_parent_id': self.id}
		return self._expand_to('ixdms.action_node_open', domain, context, self.id)
