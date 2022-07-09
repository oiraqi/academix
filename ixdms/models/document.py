from odoo import models, fields


class Document(models.Model):
	_name = 'ixdms.document'
	_description = 'Document'
	_inherit = 'mail.thread'
	_sql_constraints = [('name_folder_ukey', 'unique(name, folder_id)', 'Another document with the same name already exists in this folder!')]

	name = fields.Char('Name', required=True)
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')
	folder_id = fields.Many2one(comodel_name='ixdms.folder', string='Folder', required=True)
	favorite = fields.Boolean(string='Favorite', default=False)
		
	