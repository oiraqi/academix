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


class Portfolio(models.Model):
	_name = 'ixquality.portfolio'
	_description = 'Portfolio'
	_inherit = 'ix.faculty.activity'
	_sql_constraints = [('section_ukey', 'unique(section_id)', 'A portfolio already exists for this section')]

	name = fields.Char('Name', compute='_compute_name', store=True)
	lms_course_id = fields.Many2one(comodel_name='ixlms.course', string='LMS Course', required=True)	
	section_id = fields.Many2one('ixroster.section', related='lms_course_id.section_id', store=True)
	course_id = fields.Many2one(comodel_name='ix.course', related='section_id.course_id', store=True)
	school_id = fields.Many2one(comodel_name='ix.school', related='section_id.school_id', store=True)
	technique_ids = fields.One2many(comodel_name='ixlms.weighted.technique', related='lms_course_id.technique_ids')

	@api.onchange('section_id', 'faculty_id')
	@api.depends('section_id', 'faculty_id')
	def _compute_name(self):
		for rec in self:
			if rec.section_id:
				rec.name = rec.section_id.name + '-Portfolio'
				if rec.faculty_id:
					rec.name += ' - ' + rec.faculty_id.name
			else:
				rec.name = ''

	
	@api.onchange('term_id')
	def _onchange_term_id(self):
		for rec in self:
			if rec.term_id:
				lms_courses = self.env['ixlms.course'].search(
                    [('instructor_id.user_id', '=', self.env.user.id), ('term_id', '=', rec.term_id.id)])
				if lms_courses:
					rec.lms_course_id = lms_courses[0]
				else:
					rec.lms_course_id = False

	useful_assessment_technique_ids = fields.Many2many('ixlms.weighted.technique', 'ixquality_portfolio_assessment_technique_useful', 'portfolio_id', 'assessment_technique_id', 'Useful', required=True)
	not_recommended_assessment_technique_ids = fields.Many2many('ixlms.weighted.technique', 'ixquality_portfolio_assessment_technique_nr', 'portfolio_id', 'assessment_technique_id', 'Not Recommended')
	assessment_ids = fields.One2many(comodel_name='ixquality.assessment', inverse_name='portfolio_id', string='Assessment / Program')
	action_ids = fields.One2many(comodel_name='ixquality.action', inverse_name='portfolio_id', string='Recommended Remedial Actions')	
	ilo_changes = fields.Html('Recommended Changes To Course ILOs')
	ass_tech_modifications = fields.Html('Recommended Modifications To Assessment Techniques')
	deviations = fields.Html('Significant Deviations in Course Content from Syllabus')	
	grade_matrix = fields.Binary(string='Grade Matrix')
	good_performance = fields.Binary(string='Good Performance Samples (1 zip)')
	avg_performance = fields.Binary(string='Avg. Performance Samples (1 zip)')
	poor_performance = fields.Binary(string='Poor Performance Samples (1 zip)')
	