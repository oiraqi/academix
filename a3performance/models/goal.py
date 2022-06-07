# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.a3ma>).
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


class Goal(models.AbstractModel):
    _name='a3performance.goal'
    _description = 'An abstract goal to set and achieve in a given evaluation process'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', required=True, default=1)
    process_id = fields.Many2one('a3performance.process', string='RP Process', required=True)
    target = fields.Integer('Target', required=True)
    value = fields.Integer('Value', compute='_value')
    cvalue = fields.Char('Value', compute='_value')
    achieved = fields.Boolean('Achieved', compute='_value')

    def _value(self):
        self.write({'value': 0, 'cvalue': '0', 'achieved': False})
