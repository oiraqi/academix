from odoo import models, fields, api


class Team(models.Model):
	_name = 'a3lms.team'
	_description = 'Team'

	name = fields.Char('Name', compute='_set_name')
	teamset_id = fields.Many2one(comodel_name='a3lms.teamset', string='Team Set', required=True)	
	member_ids = fields.One2many(comodel_name='a3lms.team.membership', inverse_name='team_id', string='Members')
	course_id = fields.Many2one(comodel_name='a3lms.course', related='teamset_id.course_id', store=True)
	student_ids = fields.One2many(comodel_name='a3.student', related='course_id.student_ids')

	@api.onchange('member_ids')
	def _set_name(self):
		for rec in self:
			if not rec.member_ids:
				rec.name = ''
				continue
			names = [member.member_id.name for member in rec.member_ids]
			rec.name = '{ ' + ', '.join(names) + ' }'
	
	