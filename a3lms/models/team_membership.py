from odoo import models, fields


class TeamMembership(models.Model):
	_name = 'ixlms.team.membership'
	_description = 'Team Membership'
	_sql_constraints = [('student_teamset_ukey', 'unique(student_id, teamset_id)', 'A member cannot belong to different teams in the same Team Set!')]

	name = fields.Char('Name', related='member_id.name')
	member_id = fields.Many2one(comodel_name='ix.student', string='Member', required=True)
	team_id = fields.Many2one(comodel_name='ixlms.team', string='Team', required=True)
	teamset_id = fields.Many2one(comodel_name='ixlms.teamset', related='team_id.teamset_id', store=True)
	