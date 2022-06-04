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

from odoo import models, fields, api
from datetime import date


SEMESTERS = {'1': 'Fall', '2': 'Spring', '3': 'Summer'}

class Activity(models.AbstractModel):
    _name = 'a3.activity'
    _order = 'year desc,semester'

    @api.model
    def _year_selection(self):
        current_year = date.today().year
        year = current_year - 5
        year_list = []
        while year <= current_year + 2:
            year_list.append((str(year - 2000) + '/' + str(year - 1999),
                             str(year) + '/' + str(year - 1999)))
            year += 1
        return year_list

    year = fields.Selection(_year_selection, 'Year', required=True, default=lambda self: str(date.today().year - 2001) + '/' + str(date.today().year - 2000) if date.today().month < 8 else str(date.today().year - 2000) + '/' + str(date.today().year - 1999))
    semester = fields.Selection(
        [('1', 'Fall'), ('2', 'Spring'), ('3', 'Summer')], 'Semester', default=lambda self: '1' if date.today().month >= 8 and date.today().month <= 12 else '2' if date.today().month >= 1 and date.today().month <= 5 else '3', required=True)
    semester_year = fields.Char(string='Term', required=True)
    suffix = fields.Char(compute='_onchange_semester_or_year')
    prefix = fields.Char(compute='_onchange_semester_or_year')
    iyear = fields.Integer(compute='_onchange_semester_or_year')

    document_ids = fields.One2many(
        'ir.attachment', string='Documents', compute='_document_ids')
    document_count = fields.Integer(compute='_document_ids')

    @api.model
    def create(self, vals):
        if 'semester' in vals and 'year' in vals:
            if vals['semester'] == '1':
                vals['semester_year'] = str(int(vals['year'].split('/')[0]) + 2000) + ' - Fall'
            elif vals['semester'] == '2':
                vals['semester_year'] = str(int(vals['year'].split('/')[1]) + 2000) + ' - Spring'
            else:
                vals['semester_year'] = str(int(vals['year'].split('/')[1]) + 2000) + ' - Summer'
        return super(Activity, self).create(vals)
    

    def _document_ids(self):
        for rec in self:
            document_ids = self.sudo().env['ir.attachment'].search(
                [('res_model', '=', self._name), ('res_id', '=', rec.id)])
            if document_ids:
                rec.document_ids = document_ids
                rec.document_count = len(document_ids)
            else:
                rec.document_ids = False
                rec.document_count = 0

    @api.onchange('semester_year')
    def _onchange_semester_year(self):
        for rec in self:
            year = int(rec.semester_year.split(' - ')[0]) - 2000
            semester = rec.semester_year.split(' - ')[1]    
            rec.iyear = int(rec.semester_year.split(' - ')[0])

            if semester == 'Fall':
                rec.year = str(year) + '/' + str(year + 1)
                rec.semester = '1'
                rec.suffix = '-FA-' + str(year)
                rec.prefix = 'FA-' + str(year) + '-'
            elif semester == 'Spring':
                rec.year = str(year - 1) + '/' + str(year)
                rec.semester = '2'
                rec.suffix = '-SP-' + str(year)
                rec.prefix = 'SP-' + str(year) + '-'
            else:
                rec.year = str(year - 1) + '/' + str(year)
                rec.semester = '3'
                rec.suffix = '-SU-' + str(year)
                rec.prefix = 'SU-' + str(year) + '-'

    @api.onchange('semester', 'year')
    def _onchange_semester_or_year(self):
        for rec in self:
            year = int(rec.year.split('/')[0]) + 2000
            if rec.semester == '1':
                rec.semester_year = str(year) + ' - Fall'
                rec.suffix = '-FA-' + str(year - 2000)
                rec.prefix = 'FA-' + str(year - 2000) + '-'
                rec.iyear = year
            elif rec.semester == '2':
                rec.semester_year = str(year + 1) + ' - Spring'
                rec.suffix = '-SP-' + str(year - 1999)
                rec.prefix = 'SP-' + str(year - 1999) + '-'
                rec.iyear = year + 1
            else:
                rec.semester_year = str(year + 1) + ' - Summer'
                rec.suffix = '-SU-' + str(year - 1999)
                rec.prefix = 'SU-' + str(year - 1999) + '-'
                rec.iyear = year + 1
