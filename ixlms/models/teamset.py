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

from odoo import models, fields


class Teamset(models.Model):
	_name = 'ixlms.teamset'
	_description = 'Teamset'
	_inherit = 'ix.expandable'

	name = fields.Char('Name', required=True)
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)	
	nmembers_per_team = fields.Integer(string='Initial Number of Members per Team', default=2, required=True)	
	team_ids = fields.One2many(comodel_name='ixlms.team', inverse_name='teamset_id', string='Teams')		

	def get_teams(self):
		self.ensure_one()
		domain = [('teamset_id', '=', self.id)]
		context = {'default_teamset_id': self.id}
		return self._expand_to('ixlms.action_team_membership', domain, context)
	