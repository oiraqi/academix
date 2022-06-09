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
	_name = 'a3quality.action'
	_inherit = 'mail.thread'
	_description = 'Action'

	name = fields.Char('Title', required=True)
	description = fields.Html(string='Description', required=True)	
	portfolio_id = fields.Many2one(comodel_name='a3quality.portfolio', string='Portfolio')
	assessment_line_id = fields.Many2one(comodel_name='a3quality.assessment.line', string='Assessment Line')
	ilo_id = fields.Many2one(comodel_name='a3catalog.course.ilo', string='ILO')
	assessment_criteria = fields.Text(string='Assessment Criteria')
	assessment_methodology = fields.Text(string='Assessment Methodology')
	assessment_results = fields.Text(string='Assessment Results')

	@api.depends('assessment_line_id')
	@api.onchange('assessment_line_id')
	def _assessment_line(self):
		for rec in self:
			if rec.assessment_line_id:
				rec.portfolio_id = rec.assessment_line_id.assessment_id.portfolio_id
				rec.ilo_id = rec.assessment_line_id.ilo_id

	state = fields.Selection([
        ('planned', 'Planned'), ('implemented', 'Implemented'),
        ('assessed', 'Assessed')], string='State', default='planned', required=True, tracking=True)
