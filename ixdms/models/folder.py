from odoo import models, fields


class Folder(models.Model):
	_name = 'ixdms.folder'
	_description = 'Folder'

	name = fields.Char('Name', required=True)
	