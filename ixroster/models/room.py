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


WEEK_DAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday')
class Room(models.Model):
    _inherit = 'ix.room'

    section_ids = fields.One2many('ixroster.section', 'room_id', 'Sections', order_by='term_id desc')
    reservation_ids = fields.One2many(comodel_name='ixroster.reservation', inverse_name='room_id', string='Reservations')

    @api.model
    def available_rooms(self, start_time, end_time):
        busy_rooms = self.env['ixroster.reservation'].search([('start_time', '<=', end_time), ('end_time', '>=', end_time)])
        busy_rooms = [room.id for room in busy_rooms]
        start_datetime = fields.Datetime.to_datetime(start_time)
        end_datetime = fields.Datetime.to_datetime(end_time)
        start_day = start_datetime.weekday()
        end_day = end_datetime.weekday()
        start_timeslot = start_datetime.hour + start_datetime.minute / 60
        end_timeslot = end_datetime.hour + end_datetime.minute / 60
        if start_day == end_day:
            day = WEEK_DAYS[start_day]
            sections = self.env['ixroster.section'].search([('room_id', 'not in', busy_rooms), (day, '=', True),
                ('start_timeslot', '<=', end_timeslot),
                ('end_timeslot', '>=', start_timeslot)])
            for section in sections:
                busy_rooms.append(section.room_id.id)
        elif end_day >= start_day + 1:
            first_day = WEEK_DAYS[start_day]
            last_day = WEEK_DAYS[end_day]
            sections = self.env['ixroster.section'].search(['&', ('room_id', 'not in', busy_rooms), '|', '&', (first_day, '=', True),
                ('end_timeslot', '>=', start_timeslot), '&', (last_day, '=', True),
                ('start_timeslot', '<=', end_timeslot)])
            busy_rooms = [section.room_id.id for section in sections]
            day = start_day + 1
            while day < last_day:
                sections = self.env['ixroster.section'].search([(WEEK_DAYS[day], '=', True)])
                for section in sections:
                    busy_rooms.append(section.room_id.id)
                day += 1
        
        available_rooms = self.search([('id', 'not in', busy_rooms)])
        return [room.id for room in available_rooms]
        

    