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

SEMESTERS = {'1': 'Spring', '2': 'Summer', '3': 'Fall'}

class Term(models.Model):
    _name = 'a3.term'
    _description = 'Academic Term'
    _order = 'year,semester'
    _sql_constraints = [('term_ukey', 'unique(year, semester)', 'Term already exists')]

    @api.model
    def get_or_create(self, year, semester):
        records = self.search([('year', '=', year), ('semester', '=', semester)])
        if records:
            return records[0]
        return self.create({'year': year, 'semester': semester})

    name = fields.Char(string='Term', compute='_compute_name', store=True)
    year = fields.Integer(string='Year', required=True)
    semester = fields.Selection(
        [('1', 'Spring'), ('2', 'Summer'), ('3', 'Fall')], 'Semester', required=True)

    @api.depends('year', 'semester')
    def _compute_name(self):
        for rec in self:
            if rec.year and rec.semester:
                rec.name = SEMESTERS[rec.semester] + ' ' + str(rec.year)
    
