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


class Room(models.Model):
    _name = 'a3.room'
    _description = 'Room'
    _order = 'building_id,number'
    _sql_constraints = [('number_blg_ukey', 'unique(number, building_id)', 'Room already exists')]

    name = fields.Char(string='Name & Building', compute='_compute_name', store=True)
    number = fields.Char(string='Number', required=True)
    building_id = fields.Many2one(comodel_name='a3.building', string='Building', required=True)
    type = fields.Selection(string='Type', selection=[('classroom', 'Classroom'), ('office', 'Office'), ('lab', 'Lab')], default='classroom')
    

    @api.depends('number', 'building_id')
    @api.onchange('number', 'building_id')
    def _compute_name(self):
        for rec in self:
            if rec.number and rec.building_id:
                rec.name = rec.building_id.name + ' / ' + rec.number
            else:
                rec.name = False