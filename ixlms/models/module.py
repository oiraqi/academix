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


class Module(models.Model):
	_name = 'ixlms.module'
	_description = 'Module'
	_order = 'sequence'

	name = fields.Char('Name', required=True)
	sequence = fields.Integer(string='Sequence')
	points = fields.Integer(string='Points', compute='_points')
	percentage = fields.Float(string='%', compute='_percentage')
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)	
	assessment_ids = fields.One2many(comodel_name='ixlms.assessment', inverse_name='module_id', string='Assessments')
	nassessments = fields.Integer(string='# of Assessments', compute='_nassessments')
	chapter_ids = fields.One2many(comodel_name='ixlms.chapter', inverse_name='module_id', string='Chapters & Timeline')
	nchapters = fields.Integer(string='# of Chapters', compute='_nchapters')

	@api.onchange('assessment_ids')
	def _points(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.points = sum([assessment.points for assessment in rec.assessment_ids])
			else:
				rec.points = 0

	@api.onchange('assessment_ids')
	def _percentage(self):
		for rec in self:			
			if rec.assessment_ids:
				rec.percentage = sum([assessment.percentage for assessment in rec.assessment_ids])
			else:
				rec.percentage = 0

	@api.onchange('assessment_ids')
	def _nassessments(self):
		for rec in self:
			rec.nassessments = len(rec.assessment_ids)

	@api.onchange('chapter_ids')
	def _nchapters(self):
		for rec in self:
			rec.nchapters = len(rec.chapter_ids)