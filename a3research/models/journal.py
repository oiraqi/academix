from odoo import models, fields


class Journal(models.Model):
	_name = 'a3research.journal'
	_inherit = 'mail.thread'
	_description = 'Journal'

	name = fields.Char('Name', required=True)
	publisher_id = fields.Many2one(comodel_name='a3research.publisher', string='Publisher', required=True)
	editor = fields.Char('Editor(s)')	
	impact = fields.Selection(
        [('if', 'Impact Factor'), ('ix', 'Indexed'), ('nix', 'Non-indexed')], 'Impact', required=True)
	tier = fields.Selection(string='Tier', selection=[('1', 'Tier 1'), ('2', 'Tier 2'), ('3', 'Tier 3')], required=True, tracking=True)
	state = fields.Selection(string='State', selection=[('proposed', 'Proposed'),
		('approved', 'Approved'), ('rejected', 'Rejected')], default='proposed', required=True, tracking=True)
	
	def approve(self):
		self.ensure_one()
		self.state = 'approved'

	def reject(self):
		self.ensure_one()
		self.state = 'rejected'
	