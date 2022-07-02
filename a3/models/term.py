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

SEMESTERS = {'1': 'Spring', '2': 'Summer', '3': 'Fall'}

class Term(models.Model):
    _name = 'ix.term'
    _description = 'Academic Term'
    _order = 'year,semester'
    _sql_constraints = [('term_ukey', 'unique(year, semester)', 'Term already exists')]

    @api.model
    def get_or_create(self, year, semester):
        records = self.search([('year', '=', year), ('semester', '=', semester)])
        if records:
            return records[0]
        return self.create({'year': year, 'semester': semester})

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

    name = fields.Char(string='Term', compute='_compute_name', store=True)
    year = fields.Integer(string='Year', required=True)
    semester = fields.Selection(
        [('1', 'Spring'), ('2', 'Summer'), ('3', 'Fall')], 'Semester', required=True)
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')    

    @api.depends('year', 'semester')
    def _compute_name(self):
        for rec in self:
            if rec.year and rec.semester:
                rec.name = SEMESTERS[rec.semester] + ' ' + str(rec.year)
    
