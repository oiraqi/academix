# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.aui.ma>).
#
#    Author: Omar Iraqi Houssaini | https://github.com/oiraqi
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api


class Team(models.Model):
	_name = 'ixlms.team'
	_description = 'Team'

	name = fields.Char('Name', compute='_set_name')
	teamset_id = fields.Many2one(comodel_name='ixlms.teamset', string='Team Set', required=True)	
	member_ids = fields.One2many(comodel_name='ixlms.team.membership', inverse_name='team_id', string='Members')
	course_id = fields.Many2one(comodel_name='ixlms.course', related='teamset_id.lms_course_id', store=True)
	student_ids = fields.One2many(comodel_name='ix.student', related='course_id.student_ids')

	@api.onchange('member_ids')
	def _set_name(self):
		for rec in self:
			if not rec.member_ids:
				rec.name = ''
				continue
			names = [member.member_id.name for member in rec.member_ids]
			rec.name = '{ ' + ', '.join(names) + ' }'
	
	