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
from odoo.exceptions import ValidationError


class LmsCourse(models.Model):
	_name = 'ixlms.course'
	_description = 'LMS Course'
	_inherit = ['ix.activity', 'ix.expandable', 'ix.institution.owned']
	_sql_constraints = [('section_ukey', 'unique(section_id)', 'LMS course already created!')]

	section_id = fields.Many2one(comodel_name='ixroster.section', string='Section', required=True)	
	name = fields.Char(related='section_id.name')
	color = fields.Integer(string='Color Index')	
	course_id = fields.Many2one(comodel_name='ix.course', related='section_id.course_id')
	school_id = fields.Many2one(comodel_name='ix.school', related='section_id.school_id', store=True)	
	prerequisite_ids = fields.One2many('ixcatalog.prerequisite', related='course_id.prerequisite_ids')
	corequisite_ids = fields.One2many('ixcatalog.corequisite', related='course_id.corequisite_ids')
	prerequisites = fields.Char(compute='_requisites')
	corequisites = fields.Char(compute='_requisites')

	def _requisites(self):
		for rec in self:
			prerequisites = 'None'
			if rec.prerequisite_ids:
				if len(rec.prerequisite_ids) == 1:
					prerequisites = rec.prerequisite_ids[0].name
				else:
					prerequisites = ', '.join([prerequisite.name for prerequisite in rec.prerequisite_ids])
			rec.prerequisites = prerequisites
			
			corequisites = 'None'
			if rec.corequisite_ids:
				if len(rec.corequisite_ids) == 1:
					corequisites = rec.corequisite_ids[0].name
				else:
					corequisites = ', '.join([corequisite.name for corequisite in rec.corequisite_ids])
			rec.corequisites = corequisites

	instructor_id = fields.Many2one(comodel_name='ix.faculty', related='section_id.instructor_id', store=True)
	discipline_id = fields.Many2one(comodel_name='ix.discipline', related='section_id.discipline_id')
	timeslot = fields.Char(related='section_id.timeslot')	
	room_id = fields.Many2one(comodel_name='ix.room', related='section_id.room_id')
	student_ids = fields.One2many('ix.student', related='section_id.student_ids')
	enrollment_ids = fields.One2many('ixroster.enrollment', related='section_id.enrollment_ids')
	nstudents = fields.Integer(related='section_id.nstudents')
	description = fields.Html(related='course_id.description')
	ilo_ids = fields.One2many('ixcatalog.course.ilo', related='course_id.ilo_ids')
	textbook_ids = fields.One2many(comodel_name='ixlms.textbook', related='course_id.textbook_ids')
	office_hour_ids = fields.One2many(comodel_name='ixroster.office.hour', related='instructor_id.office_hour_ids')
	office_hours = fields.Char(compute='_office_hours')

	def _office_hours(self):
		for rec in self:
			office_hours = ''
			if rec.office_hour_ids:
				if len(rec.office_hour_ids) == 1:
					office_hours = rec.office_hour_ids[0].name
				else:
					office_hours = ', '.join([office_hour.name for office_hour in rec.office_hour_ids])
			rec.office_hours = office_hours
	

	module_ids = fields.One2many(comodel_name='ixlms.module', inverse_name='lms_course_id', string='Modules')
	nmodules = fields.Integer(string='Modules', compute='_nmodules')
	assessed_module_ids = fields.One2many(comodel_name='ixlms.module', compute='_assessed_module_ids', string='Modules')

	@api.onchange('module_ids')
	def _nmodules(self):
		for rec in self:
			if rec.module_ids:
				rec.nmodules = len(rec.module_ids)
			else:
				rec.nmodules = 0

	@api.onchange('assessment_ids')
	def _assessed_module_ids(self):
		for rec in self:
			assessed_module_ids = [assessment.module_id.id for assessment in rec.assessment_ids]
			rec.assessed_module_ids = self.env['ixlms.module'].search([('id', 'in', assessed_module_ids)])

	technique_ids = fields.One2many(comodel_name='ixlms.weighted.technique', inverse_name='lms_course_id', string='Techniques')
	ntechniques = fields.Integer(string='Techniques', compute='_ntechniques')

	@api.onchange('technique_ids')
	def _ntechniques(self):
		for rec in self:
			if rec.technique_ids:
				rec.ntechniques = len(rec.technique_ids)
			else:
				rec.ntechniques = 0

	grade_grouping = fields.Selection(string='Assessment Grouping', selection=[('module', 'Course Module'), ('technique', 'Assessment Technique'),], default='module', required=True)
	grade_weighting = fields.Selection(string='Assessment Weighting', selection=[('percentage', 'Percentage'), ('points', 'Points'),], default='percentage', required=True)	
	attendance_points = fields.Integer(string='Attendance Points', default=0)
	assessment_percentage = fields.Float(string='Assessment %', compute='_ass_att_percentage')
	attendance_percentage = fields.Float(string='Attendance %', compute='_ass_att_percentage')
	attendance_weight = fields.Float(compute='_attendance_weight')

	@api.onchange('assessment_ids')
	def _ass_att_percentage(self):
		for rec in self:			
			assessment_percentage = sum([assessment.percentage for assessment in rec.assessment_ids])
			if assessment_percentage <= 100:
				rec.assessment_percentage = assessment_percentage
				rec.attendance_percentage = 100 - assessment_percentage
			else:
				rec.attendance_percentage = 0.0
				raise ValidationError('The sum of assessment percentages cannot exceed 100%')
				
	
	@api.onchange('grade_weighting', 'attendance_percentage', 'attendance_points')
	def _attendance_weight(self):
		for rec in self:
			if rec.grade_weighting == 'percentage':
				rec.attendance_weight = rec.attendance_percentage
			elif rec.grade_weighting == 'points':
				rec.attendance_weight = float(rec.attendance_points)
			else:
				rec.attendance_weight = 0.0

	attendance_grading = fields.Selection(string='Attendance Grading', selection=[('rate', 'Attendance Rate'),
		('penalty', 'Penalty / Unexcused Absence')], default='rate')	
	penalty_per_absence = fields.Float(string='Penalty(%) / Absence', default=5.0)
	zero_after_max_abs = fields.Boolean(string='Zero after Max Absences', default=False)	
	max_absences = fields.Integer(string='Max Absences', default=5)
	
	assessment_ids = fields.One2many(comodel_name='ixlms.assessment', inverse_name='lms_course_id', string='Assessments')
	nassessments = fields.Integer(string='Assessments', compute='_assessment_ids')
	nassessment_lines = fields.Integer(string='Number of Assessment Lines', compute='_assessment_ids')
	used_technique_ids = fields.One2many(comodel_name='ixlms.assessment.technique', compute='_assessment_ids')
	attendance_ids = fields.One2many(comodel_name='ixlms.attendance', inverse_name='lms_course_id', string='Attendance Sheets', groups="ix.group_faculty,ix.group_coordinator,ix.group_vpaa")
	nattendance_sheets = fields.Integer(string='Number of Attendance Sheets', compute='_attendance_ids', groups="ix.group_faculty,ix.group_coordinator,ix.group_vpaa")
	teamset_ids = fields.One2many(comodel_name='ixlms.teamset', inverse_name='lms_course_id', string='Team Sets')
	nteamsets = fields.Integer(string='Team Sets', compute='_nteamsets')

	@api.onchange('teamset_ids')
	def _nteamsets(self):
		for rec in self:
			if rec.teamset_ids:
				rec.nteamsets = len(rec.teamset_ids)
			else:
				rec.nteamsets = 0
	
	chapter_ids = fields.One2many(comodel_name='ixlms.chapter', inverse_name='lms_course_id', string="Chapters & Timeline")
	nchapters = fields.Integer(string='Chapters', compute='_nchapters')

	def _nchapters(self):
		for rec in self:
			rec.nchapters = len(rec.chapter_ids)
	

	def _attendance_ids(self):
		for rec in self:
			rec.nattendance_sheets = len(rec.attendance_ids)
	
	@api.onchange('assessment_ids')
	def _assessment_ids(self):
		for rec in self:
			if rec.assessment_ids:
				rec.used_technique_ids = [assessment.technique_id.id for assessment in rec.assessment_ids]
				rec.nassessments = len(rec.assessment_ids)
				rec.nassessment_lines = self.env['ixlms.assessment.line'].search_count([('lms_course_id', '=', rec.id), ('student_id', 'in', rec.student_ids.ids)])
			else:
				rec.used_technique_ids = False
				rec.nassessments = 0
				rec.nassessment_lines = 0
	
	details = fields.Html(string='More Details')

	channel_ids = fields.One2many(comodel_name='mail.channel', inverse_name='lms_course_id', string='Channels')
	nchannels = fields.Integer(string='Channels', compute='_nchannels')

	def _nchannels(self):
		for rec in self:
			rec.nchannels = len(rec.channel_ids)

	program_ids = fields.One2many(comodel_name='ixcatalog.program', compute='_program_ids')

	def _program_ids(self):
		for rec in self:
			program_ids = []
			for student in rec.student_ids:
				if student.program_id.id not in program_ids:
					program_ids.append(student.program_id.id)
			if len(program_ids) > 0:
				rec.program_ids = program_ids
			else:
				rec.program_ids = False
	

	@api.constrains('grade_weighting', 'assessment_ids')
	def check_sum_percentages(self):
		for rec in self:
			if rec.grade_weighting != 'percentage' or not rec.assessment_ids:
				continue
			
			if sum([assessment.percentage for assessment in rec.assessment_ids]) > 100:
				raise ValidationError('The sum of assessment percentages cannot exceed 100%')
		
	def get_students(self):
		self.ensure_one()
		domain = [('section_id', '=', self.section_id.id), ('state', 'in', ['enrolled', 'withdrawn', 'completed'])]		
		return self._expand_to('ixlms.action_enrollment', domain)

	def get_my(self):
		self.ensure_one()
		domain = [('section_id', '=', self.section_id.id), ('student_id', '=', self.env.user.student_id.id), ('state', 'in', ['enrolled', 'withdrawn', 'completed'])]
		enrollment_id = self.env['ixroster.enrollment'].search(domain)
		return self._expand_to('ixlms.action_enrollment_my', domain, False, enrollment_id.id)

	def get_assessments(self):
		self.ensure_one()
		domain = [('lms_course_id', '=', self.id)]
		context = {'default_lms_course_id': self.id}
		if self.grade_grouping == 'module' and self.grade_weighting == 'percentage':
			context.update({'group_by': 'module_id'})
			return self._expand_to('ixlms.action_assessment_module_percentage', domain, context)

		if self.grade_grouping == 'module' and self.grade_weighting == 'points':
			context.update({'group_by': 'module_id'})
			return self._expand_to('ixlms.action_assessment_module_points', domain, context)
		
		if self.grade_grouping == 'technique' and self.grade_weighting == 'percentage':
			context.update({'group_by': 'technique_id'})
			return self._expand_to('ixlms.action_assessment_technique_percentage', domain, context)

		if self.grade_grouping == 'technique' and self.grade_weighting == 'points':
			context.update({'group_by': 'technique_id'})
			return self._expand_to('ixlms.action_assessment_technique_points', domain, context)
		

	def get_grade_matrix(self):
		self.ensure_one()
		domain = [('course_id', '=', self.id), ('student_id', 'in', self.student_ids.ids)]
		if self.grade_grouping == 'module' and self.grade_weighting == 'percentage':
			return self._expand_to('ixlms.action_assessment_line_module_percentage', domain)

		if self.grade_grouping == 'module' and self.grade_weighting == 'points':
			return self._expand_to('ixlms.action_assessment_line_module_points', domain)
		
		if self.grade_grouping == 'technique' and self.grade_weighting == 'percentage':
			return self._expand_to('ixlms.action_assessment_line_technique_percentage', domain)

		if self.grade_grouping == 'technique' and self.grade_weighting == 'points':
			return self._expand_to('ixlms.action_assessment_line_technique_points', domain)

	def get_attendance(self):
		self.ensure_one()
		domain = [('lms_course_id', '=', self.id)]
		context = {'default_lms_course_id': self.id}
		return self._expand_to('ixlms.action_attendance', domain, context)

	def get_teamsets(self):
		self.ensure_one()
		domain = [('lms_course_id', '=', self.id)]
		context = {'default_lms_course_id': self.id}
		return self._expand_to('ixlms.action_teamset', domain, context)

	def get_modules(self):
		self.ensure_one()
		domain = [('lms_course_id', '=', self.id)]
		context = {'default_lms_course_id': self.id}
		return self._expand_to('ixlms.action_module', domain, context)

	def get_techniques(self):
		self.ensure_one()
		domain = [('course_id', '=', self.id)]
		context = {'default_course_id': self.id}
		return self._expand_to('ixlms.action_weighted_technique', domain, context)

	def get_channels(self):
		self.ensure_one()
		domain = [('lms_course_id', '=', self.id)]
		context = {'default_lms_course_id': self.id, 'default_public': 'private'}
		return self._expand_to('ixlms.action_mail_channel', domain, context)

	def get_chapters(self):
		self.ensure_one()
		domain = [('lms_course_id', '=', self.id)]
		context = {'default_lms_course_id': self.id, 'group_by': 'module_id'}
		return self._expand_to('ixlms.action_chapter', domain, context)


