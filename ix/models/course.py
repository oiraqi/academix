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
from odoo.exceptions import UserError
import re


class Course(models.Model):
    _name = 'ix.course'
    _sql_constraints = [
        ('code_ukey', 'unique(code)', 'Course already exists')]
    _order = 'code'

    name = fields.Char('Code and Name', required=True)
    name_only = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    number = fields.Integer('Number', required=True)
    school_id = fields.Many2one(
        'ix.school', compute='_compute_discipline_school', string='School', store=True)
    discipline_id = fields.Many2one(
        'ix.discipline', compute='_compute_discipline_school', string='Discipline', store=True)

    @api.model
    def create(self, vals):
        if 'code' in vals:
            if 'name_only' in vals:
                vals['name'] = vals['code'] + ' ' + vals['name_only']
            if len(vals['code'].split()) == 2:
                vals['number'] = int(vals['code'].split()[1])
        return super(Course, self).create(vals)

    def write(self, vals):        
        if 'code' not in vals and 'name_only' not in vals:
            return super(Course, self).write(vals)
        
        result = super(Course, self).write(vals)
        for rec in self:
            rec.name = rec.code + ' ' + rec.name_only
            if 'code' in vals:
                rec.number = int(rec.code.split()[1])
        return result
        
    
    
    
    @api.onchange('code')
    @api.depends('code')
    def _compute_discipline_school(self):
        for rec in self:
            if rec.code and len(rec.code) >= 3:
                discipline_id = self.env['ix.discipline'].search(
                    [('code', '=', rec.code.upper()[0:3])])
                if discipline_id:
                    rec.discipline_id = discipline_id
                    rec.school_id = discipline_id.school_id
                    code = rec.code.replace(" ", "").upper()
                    if len(code) > 3:
                        rec.code = code[0:3] + ' ' + code[3:]
                else:
                    raise UserError(
                        'Invalid course code. No match found for discipline!')
            else:
                rec.discipline_id = False
                rec.school_id = False

    level = fields.Selection(
        [('u', 'Undergraduate'), ('g', 'Graduate')], 'Level', default='u', required=True)

    @api.constrains('code')
    def _check_code(self):
        for rec in self:
            code = rec.code.replace(" ", "").upper()
            if len(code) != 7:
                raise UserError('Erroneous Course Code!')
            
            if rec.level == 'u' and not re.match(r'[0-4][0-4]\d\d', code[3:7]):
                raise UserError(
                    'Undergraduate course codes must match [0-4][0-4][0-9][0-9]')

            if rec.level == 'g' and not re.match(r'[5-6][0-4]\d\d', code[3:7]):
                raise UserError(
                    'Graduate course codes must match [5-6][0-4][0-9][0-9]')
            
