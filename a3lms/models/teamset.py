from odoo import models, fields


class Teamset(models.Model):
	_name = 'a3lms.teamset'
	_description = 'Teamset'
	_inherit = 'a3.expandable'

	name = fields.Char('Name', required=True)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	nmembers_per_team = fields.Integer(string='Initial Number of Members per Team', default=2, required=True)	
	team_ids = fields.One2many(comodel_name='a3lms.team', inverse_name='teamset_id', string='Teams')		

	def get_teams(self):
		self.ensure_one()
		domain = [('teamset_id', '=', self.id)]
		context = {'default_teamset_id': self.id}
		return self._resolve_action('a3lms.action_team_membership', domain, context)
	