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

from odoo import api, fields, models, api


class Event(models.Model):
    _name = 'a3calendar.term'
    _description = 'Important Date'
    _inherit = 'a3.activity'
    _sql_constraints = [('a3calendar_idate_ukey', 'unique(year, semester, type)', 'IDate already exists!')]

    name = fields.Char(string='Title', compute='_set_name')
    start = fields.Date(string='Start Date')
    type = fields.Selection(string='Type', selection=[('std', 'Standard'), ('cstm', 'Custom')], default='std')
    standard_event_id = fields.Many2one(comodel_name='a3calendar.standard.event', string='Standard Event')
    custom_event = fields.Char(string='Custom Event')
    standard_considerations = fields.Html(related='standard_event_id.standard_considerations')
    specific_considerations = fields.Html(string='Specific Considerations')

    @api.onchange('type', 'standard_event_id', 'custom_event')
    def _set_name_(self):
        for rec in self:
            if rec.type == 'std' and rec.standard_event_id:
                rec.name = rec.standard_event_id.name
            elif rec.type == 'cstm' and rec.custom_event:
                rec.name = rec.custom_event
            else:
                rec.name = ''
    