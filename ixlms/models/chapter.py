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

from odoo import models, fields


class Chapter(models.Model):
	_name = 'ixlms.chapter'
	_description = 'Chapter'
	_order = "sequence"
	_sql_constraints = [('course_sequence_ukey', 'unique(lms_course_id, sequence)', 'Duplicate chapter sequence!')]

	name = fields.Char('Name', required=True)
	sequence = fields.Integer('Ch.', required=True)
	module_id = fields.Many2one(comodel_name='ixlms.module', string='Module', required=True)
	course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', related='course_id', store=True)
	ccourse_id = fields.Many2one(comodel_name='ix.course', related='lms_course_id.course_id')
	start_date = fields.Date(string='Start Date')
	nsessions = fields.Integer(string='Sessions')
	resource_ids = fields.Many2many(comodel_name='ixlms.resource', string='Resources')
	nresources = fields.Integer(string='Resources', compute='_nresources')
	module_ids = fields.One2many(comodel_name='ixlms.module', related='lms_course_id.module_ids')

	def _nresources(self):
		for rec in self:
			rec.nresources = len(rec.resource_ids)
	
	
		