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
import re


class Resource(models.Model):
	_name = 'ixlms.resource'
	_description = 'Resource'

	name = fields.Char('Name', required=True)	
	file = fields.Binary(string='File')
	url = fields.Char(string='URL')
	text = fields.Html(string='Text')
	has_text = fields.Boolean(string='Text', compute='_has_text')
	has_url = fields.Boolean(string='URL', compute='_has_url')
	
	def _has_text(self):
		stripper = re.compile('<.*?>')
		for rec in self:			
			rec.has_text = rec.text and len(re.sub(stripper, '', rec.text).strip()) > 0

	def _has_url(self):
		for rec in self:			
			rec.has_url = rec.url and len(rec.url) > 0
	
	course_id = fields.Many2one(comodel_name='ix.course', string='Course', required=True)
	