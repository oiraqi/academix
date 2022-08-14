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


class StudentOutcome(models.Model):
    _name = 'ixquality.student.outcome'
    _description = 'Student Outcome'
    _order = 'sequence'
    _sql_constraints = [
        ('sequence_program_ukey', 'unique(sequence, program_id)', 'Sequence must be unique')]

    name = fields.Char(compute='_compute_name', string='Reference')

    @api.depends('sequence')
    @api.onchange('sequence')
    def _compute_name(self):
        for rec in self:
            rec.name = 'SO' + str(rec.sequence)

    description = fields.Text(string='SO', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    program_id = fields.Many2one(
        comodel_name='ixcatalog.program', string='Program', required=True)
    introducing_course_ids = fields.One2many(
        comodel_name='ix.course', compute='_introducing_cours_ids', string='Introduced')
    reinforcing_course_ids = fields.One2many(
        comodel_name='ix.course', compute='_reinforcing_course_ids', string='Reinforced')
    emphasizing_course_ids = fields.One2many(
        comodel_name='ix.course', compute='_emphasizing_course_ids', string='Emphasized')

    @api.onchange('program_id')
    def _introducing_cours_ids(self):
        for rec in self:
            records = self.env['ixquality.course.ilo.so'].search([('so_id', '=', rec.id), (
                'level', '=', 'introduce'), ('course_program_id.program_id', '=', rec.program_id.id)])
            if records:
                rec.introducing_course_ids = [record.course_program_id.course_id.id for record in records]
            else:
                rec.introducing_course_ids = False

    @api.onchange('program_id')
    def _reinforcing_course_ids(self):
        for rec in self:
            records = self.env['ixquality.course.ilo.so'].search([('so_id', '=', rec.id), (
                'level', '=', 'reinforce'), ('course_program_id.program_id', '=', rec.program_id.id)])
            if records:
                rec.reinforcing_course_ids = [record.course_program_id.course_id.id for record in records]
            else:
                rec.reinforcing_course_ids = False

    @api.onchange('program_id')
    def _emphasizing_course_ids(self):
        for rec in self:
            records = self.env['ixquality.course.ilo.so'].search([('so_id', '=', rec.id), (
                'level', '=', 'emphasize'), ('course_program_id.program_id', '=', rec.program_id.id)])
            if records:
                rec.emphasizing_course_ids = [record.course_program_id.course_id.id for record in records]
            else:
                rec.emphasizing_course_ids = False