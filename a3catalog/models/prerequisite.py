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

from odoo import api, fields, models


class Prerequisite(models.Model):
    _name = 'ixcatalog.prerequisite'
    _description = 'Course Prerequisite'

    name = fields.Char(string='Name', compute='_set_name')

    @api.onchange('alternative_ids')
    def _set_name(self):
        for rec in self:
            name = ''
            if rec.alternative_ids:
                if len(rec.alternative_ids) == 1:
                    name = rec.alternative_ids[0].name
                else:
                    name = '{ ' + ' or '.join([alternative.name for alternative in rec.alternative_ids]) + ' }'
            rec.name = name
    
    course_id = fields.Many2one('ix.course', string='Course')
    alternative_ids = fields.Many2many('ix.course', string='Prerequisite')
    sequence = fields.Integer(default='1', required=True)
