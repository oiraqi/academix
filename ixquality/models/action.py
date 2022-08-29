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

from odoo import api, models, fields


class Action(models.Model):
	_name = 'ixquality.action'
	_inherit = 'mail.thread'
	_description = 'Action'

	name = fields.Char('Title', required=True)
	description = fields.Html(string='Description', required=True)	
	portfolio_id = fields.Many2one(comodel_name='ixquality.portfolio', string='Portfolio')
	assessment_line_id = fields.Many2one(comodel_name='ixquality.assessment.line', string='Assessment Line')
	lms_course_ilo_id = fields.Many2one(comodel_name='ixlms.course.ilo', string='ILO')
	assessment_criteria = fields.Text(string='Assessment Criteria')
	assessment_methodology = fields.Text(string='Assessment Methodology')
	assessment_results = fields.Text(string='Assessment Results')

	@api.depends('assessment_line_id')
	@api.onchange('assessment_line_id')
	def _assessment_line(self):
		for rec in self:
			if rec.assessment_line_id:
				rec.portfolio_id = rec.assessment_line_id.assessment_id.portfolio_id				
				rec.lms_course_ilo_id = rec.assessment_line_id.lms_course_ilo_id

	state = fields.Selection([
        ('planned', 'Planned'), ('implemented', 'Implemented'),
        ('assessed', 'Assessed')], string='State', default='planned', required=True, tracking=True)

	
	def mark_implemented(self):
		self.ensure_one()
		self.state = 'implemented'

	def mark_assessed(self):
		self.ensure_one()
		self.state = 'assessed'
