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
    def create(self, vals):
        if 'year' in vals and 'semester' in vals:
            year = int(vals['year'].split('/')[0]) + 2000
            if vals['semester'] == '1':
                semester = '3'
            elif vals['semester'] == '2':
                semester = '1'
                year += 1
            else:
                semester = '2'
                year += 1
            vals['term_id'] = self.env['a3.term'].sudo().get_or_create(year, semester).id
        return super(Activity, self).create(vals)
        
    def write(self, vals):
        if 'term_id' in vals:
            records = self.env['a3.term'].browse([vals['term_id']])
            year = records[0].year
            semester = records[0].semester - 2000
            if records:                 
                if semester == '1':
                    vals['year'] = str(year - 1) + '/' + str(year)
                    vals['semester'] = '2'
                elif semester == '2':
                    vals['year'] = str(year - 1) + '/' + str(year)
                    vals['semester'] = '3'
                else:
                    vals['year'] = str(year) + '/' + str(year + 1)
                    vals['semester'] = '1'
            return super(Activity, self).write(vals)
        
        if 'semester' in vals and 'year' in vals:
            year = int(vals['year'].split('/')[0]) + 2000
            if vals['semester'] == '1':
                semester = '3'
            elif vals['semester'] == '2':
                semester = '1'
                year += 1
            else:
                semester = '2'
                year += 1
            vals['term_id'] = self.env['a3.term'].sudo().get_or_create(year, semester).id
            return super(Activity, self).write(vals)
        
        result = super(Activity, self).write(vals)
        for rec in self:
            year = int(rec.year.split('/')[0]) + 2000
            if rec.semester == '1':
                semester = '3'
            elif rec.semester == '2':
                semester = '1'
                year += 1
            else:
                semester = '2'
                year += 1
            rec.term_id = self.env['a3.term'].sudo().get_or_create(year, semester)
        
        return result



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
    term_id = fields.Many2one('a3.term', string='Term')
    suffix = fields.Char(compute='_onchange_semester_or_year')
    prefix = fields.Char(compute='_onchange_semester_or_year')

    document_ids = fields.One2many(
        'ir.attachment', string='Documents', compute='_document_ids')
    document_count = fields.Integer(compute='_document_ids')

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

    @api.depends('semester', 'year')
    @api.onchange('semester', 'year')
    def _onchange_semester_or_year(self):
        for rec in self:
            year = int(rec.year.split('/')[0]) + 2000
            if rec.semester == '1':
                rec.term_id = self.env['a3.term'].sudo().get_or_create(year, '3')
                rec.suffix = '-FA' + str(year - 2000)
                rec.prefix = 'FA' + str(year - 2000) + '-'                
            elif rec.semester == '2':
                rec.term_id = self.env['a3.term'].sudo().get_or_create(year + 1, '1')
                rec.suffix = '-SP' + str(year - 1999)
                rec.prefix = 'SP' + str(year - 1999) + '-'
            else:
                rec.term_id = self.env['a3.term'].sudo().get_or_create(year + 1, '2')
                rec.suffix = '-SU' + str(year - 1999)
                rec.prefix = 'SU' + str(year - 1999) + '-'
