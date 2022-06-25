from odoo import models, fields, api


class Team(models.Model):
	_name = 'a3lms.team'
	_description = 'Team'

	name = fields.Char('Name', compute='_set_name')
	member_ids = fields.Many2many(comodel_name='a3.student', string='Members', required=True)
	course_id = fields.Many2one(comodel_name='a3lms.course', string='LMS Course', required=True)
	

	@api.onchange(member_ids)
	def _set_name(self):
		for rec in self:
			if not rec.member_ids:
				rec.name = ''
				continue
			names = [member.name for member in rec.member_ids]
			rec.name = '{' + ', '.join(names) + '}'
	
	