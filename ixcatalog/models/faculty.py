from odoo import models, fields


class Faculty(models.Model):
	_inherit = 'ix.faculty'

	managed_program_ids = fields.Many2many('ixcatalog.program', 'ixcatalog_program_ix_faculty', 'manager_id', 'program_id', string='Managed Programs')	
	