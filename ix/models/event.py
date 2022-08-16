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


META_EVENTS = [('add_drop', 'Add/Drop'), ('w', 'Last day to drop a course with W'), ('grade_submission', 'Grade Submission')]

class Event(models.Model):
	_name = 'calendar.event'
	_inherit = ['calendar.event', 'ix.activity']
	_description = 'Event'

	allday = fields.Boolean('All Day', default=True)
	meta = fields.Selection(string='Type', selection=META_EVENTS)

	@api.onchange('meta')
	def _meta(self):
		for rec in self:
			if rec.meta:
				for meta_event in META_EVENTS:
					if meta_event[0] == rec.meta:
						rec.name = meta_event[1]
						return
			
	
	