from odoo import models, fields


class Folder(models.Model):
	_name = 'ixdms.folder'
	_description = 'Folder'

	name = fields.Char('Name', required=True)
	parent_id = fields.Many2one(comodel_name='ixdms.folder', string='Parent')
	folder_ids = fields.One2many(comodel_name='ixdms.folder', inverse_name='parent_id', string='Sub-Folders')
	nfolders = fields.Integer(string='Number of Subfolders', compute='_nfolders')

	def _folders(self):
		for rec in self:
			rec.nfolders = len(rec.folder_ids)

	document_ids = fields.One2many(comodel_name='ixdms.document', inverse_name='folder_id', string='Documents')
	ndocuments = fields.Integer(string='Number of Documents', compute='_ndocuments')

	def _ndocuments(self):
		for rec in self:
			rec.ndocuments = len(rec.document_ids)
	
	
	