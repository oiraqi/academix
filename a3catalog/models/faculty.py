from odoo import models, fields


class Faculty(models.Model):
	_inherit = 'a3.faculty'

	managed_program_ids = fields.Many2many('a3catalog.program', 'a3catalog_program_a3_faculty', 'manager_id', 'program_id', string='Managed Programs')	
	