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


class StudentShare(models.Model):
	_name = 'ixdms.student.share'
	_description = 'Student Share'
	_inherit = 'ix.school.owned'
	_sql_constraints = [('share_ukey', 'unique(share_id, school_id, program_id)', 'Duplicate shares!')]

	share_id = fields.Many2one(comodel_name='ixdms.node', string='Share', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program')
		