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
from odoo.exceptions import ValidationError

class Term(models.Model):
    _name = 'ix.term'
    _description = 'Academic Term'
    _order = 'year,sequence'
    _sql_constraints = [('term_ukey', 'unique(year, session_id)', 'Term already exists')]

    @api.model
    def get_or_create(self, year, session_id):
        records = self.search([('year', '=', year), ('session_id', '=', session_id)])
        if records:
            return records[0]
        return self.sudo().create({'year': year, 'session_id': session_id})

    def get_or_create_next(self):
        self.ensure_one()
        next_session = self.session_id.get_next()
        if next_session:
            return self.env['ix.term'].get_or_create(self.year, next_session.id)
        
        first_session = self.env['ix.session'].get_first_session()
        return self.env['ix.term'].get_or_create(self.year + 1, first_session.id)

    @api.model
    def get_from_date(self, day):
        term = self.search([('start_date', '<=', day), ('end_date', '>=', day)])
        return term and term[0] or False

    @api.model
    def get_current(self):
        return self.get_from_date(fields.Date.today())

    @api.constrains('start_date', 'end_date')
    def _check_overlapping(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                if self.env[self._name].search_count([('end_date', '>=', rec.start_date), ('start_date', '<=', rec.end_date)]) > 1:
                    raise ValidationError('Terms are not allowed to overlap!')

    @api.constrains('year')
    def _check_year(self):
        for rec in self:
            if rec.year < 2000:
                raise ValidationError('Year must be >= 2000')

    name = fields.Char(string='Term', compute='_compute_name_code', store=True)
    code = fields.Char(string='Term', compute='_compute_name_code', store=True)
    year = fields.Integer(string='Year', required=True, default=lambda self: fields.Date.today().year)
    session_id = fields.Many2one(comodel_name='ix.session', string='Session', required=True)
    sequence = fields.Integer(related='session_id.sequence', store=True)    
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    event_ids = fields.One2many(comodel_name='calendar.event', inverse_name='term_id', string='Events & Important Dates', order='start_date')
    

    @api.depends('year', 'session_id')
    def _compute_name_code(self):
        for rec in self:
            if rec.year and rec.session_id:
                rec.name = rec.session_id.name + ' ' + str(rec.year)
                rec.code = rec.session_id.code + str(rec.year - 2000)
    
