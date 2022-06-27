from odoo import models, fields


class TeamMembership(models.Model):
	_name = 'a3lms.team.membership'
	_description = 'Team Membership'
	_sql_constraints = [('student_teamset_ukey', 'unique(student_id, teamset_id)', 'A member cannot belong to different teams in the same Team Set!')]

	name = fields.Char('Name', related='member_id.name')
	member_id = fields.Many2one(comodel_name='a3.student', string='Member', required=True)
	team_id = fields.Many2one(comodel_name='a3lms.team', string='Team', required=True)
	teamset_id = fields.Many2one(comodel_name='a3lms.teamset', related='team_id.teamset_id', store=True)
	