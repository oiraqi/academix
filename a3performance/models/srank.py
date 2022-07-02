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


class Srank(models.Model):
    _name = 'ixperformance.srank'
    _order = 'rank,name'
    _sql_constraints = [('name_ukey', 'unique(name)', 'Sub rank already exists')]

    name = fields.Char('Code', required=True)
    rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'Rank', required=True)

    def write(self, vals):
        if 'name' in vals:
            vals['name'] = vals['name'].replace(' ', '').upper()

        return super(Srank, self).write(vals)
