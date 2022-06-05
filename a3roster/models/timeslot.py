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


class TimeSlot(models.Model):
    _name = 'a3roster.timeslot'
    _description = 'Timeslot'
    _sql_constraints = [('timeslot_ukey', 'unique(start_time, end_time, days)', 'Time slot already defined!')]

    name = fields.Char('Name', compute='_compute_name', store=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    days = fields.Selection(string='Days', selection=[('MWF', 'MWF'), ('TR', 'TR')], default='MWF', required=True)

    @api.depends('start_time', 'end_time')
    @api.onchange('start_time', 'end_time')
    def _compute_name(self):
        for rec in self:
            if rec.start_time and rec.end_time and rec.days:
                start_hours = int(rec.start_time)
                start_minutes = (rec.start_time - start_hours) * 60
                start_time = str(start_hours) + ':' + str(start_minutes)
                end_hours = int(rec.end_time)
                end_minutes = (rec.end_time - end_hours) * 60
                end_time = str(end_hours) + ':' + str(end_minutes)
                rec.name = rec.days + ' ' + start_time + ' - ' + end_time
            else:
                rec.name = False
