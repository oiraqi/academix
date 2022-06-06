from odoo import models, fields


class Journal(models.Model):
	_name = 'a3research.journal'
	_description = 'Journal'

	name = fields.Char('Name', required=True)
	impact = fields.Selection(
        [('if', 'Impact Factor'), ('ix', 'Indexed'), ('nix', 'Non-indexed')], 'Impact', required=True)
	