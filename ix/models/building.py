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

from odoo import fields, models, api


class BuildingGroup(models.Model):
	_name = 'ix.building.group'
	_description = 'BuildingGroup'

	name = fields.Char('Name', required=True)
	building_ids = fields.One2many(comodel_name='ix.building', inverse_name='group_id', string='Buildings')
    

class Building(models.Model):
    _name = 'ix.building'
    _description = 'Building'
    _sql_constraints = [('b=name_ukey', 'unique(name)', 'Building already exists')]

    name = fields.Char(string='Name', required=True)
    group_id = fields.Many2one(comodel_name='ix.building.group', string='Group', required=True)
    room_ids = fields.One2many(comodel_name='ix.room', inverse_name='building_id', string='Rooms')
    classrooms = fields.Integer(compute='_rooms', string='Classrooms', store=True)
    labs = fields.Integer(compute='_rooms', string='Labs', store=True)
    offices = fields.Integer(compute='_rooms', string='Offices', store=True)
    general_rooms = fields.Integer(compute='_rooms', string='General Purpose Rooms', store=True)
    capacity = fields.Integer(compute='_rooms', string='Total Capacity', store=True)

    @api.depends('room_ids')
    def _rooms(self):
        for rec in self:
            classrooms = 0
            labs = 0
            offices = 0
            general_rooms = 0
            capacity = 0
            for room in rec.room_ids:
                if room.type == 'classroom':
                    classrooms += 1
                elif room.type == 'lab':
                    labs += 1
                elif room.type == 'office':
                    offices += 1
                elif room.type == 'general':
                    general_rooms += 1
                capacity += int(room.capacity)
            rec.classrooms = classrooms
            rec.labs = labs
            rec.offices = offices
            rec.general_rooms = general_rooms
            rec.capacity = capacity
    