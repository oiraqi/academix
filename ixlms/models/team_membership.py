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


class TeamMembership(models.Model):
	_name = 'ixlms.team.membership'
	_description = 'Team Membership'
	_sql_constraints = [('student_teamset_ukey', 'unique(student_id, teamset_id)', 'A member cannot belong to different teams in the same Team Set!')]

	name = fields.Char('Name', related='member_id.name')
	member_id = fields.Many2one(comodel_name='ix.student', string='Member', required=True)
	team_id = fields.Many2one(comodel_name='ixlms.team', string='Team', required=True)
	teamset_id = fields.Many2one(comodel_name='ixlms.teamset', related='team_id.teamset_id', store=True)
	