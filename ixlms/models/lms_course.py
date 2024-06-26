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
import re


class LmsCourse(models.Model):
	_name = 'ixlms.course'
	_description = 'LMS Course'
	_inherit = ['ix.activity', 'ix.expandable', 'ix.institution.owned']
	_order = 'term_id, course_id'

	@api.model
	def create(self, vals):
		lms_course = super(LmsCourse, self).create(vals)
		lms_course.description = lms_course.course_id.description
		
		for ilo in lms_course.course_id.ilo_ids:
			self.env['ixlms.course.ilo'].create({
				'description': ilo.description,
				'course_id': ilo.course_id.id,
				'sequence': ilo.sequence,
				'lms_course_id': lms_course.id
			})
		
		previous_lms_courses = self.env['ixlms.course'].search([('instructor_id', '=', lms_course.instructor_id.id), ('course_id', '=', lms_course.course_id.id), ('id', '!=', lms_course.id)], order='term_id desc')
		if len(previous_lms_courses) > 0:
			latest_lms_course = previous_lms_courses[0]

			lms_course.write({
				'details': latest_lms_course.details,
				'grade_grouping': latest_lms_course.grade_grouping,
				'grade_weighting': latest_lms_course.grade_weighting,
				'attendance_points': latest_lms_course.attendance_points,
				'attendance_grading': latest_lms_course.attendance_grading,
				'penalty_per_absence': latest_lms_course.penalty_per_absence,
				'zero_after_max_abs': latest_lms_course.zero_after_max_abs,
				'max_absences': latest_lms_course.max_absences,
				'assessment_remarks': latest_lms_course.assessment_remarks,
			})
			
			techniques = {}
			for technique in latest_lms_course.technique_ids:
				techniques[technique.id] = self.env['ixlms.weighted.technique'].create({
					'technique_id': technique.technique_id.id,
					'sequence': technique.sequence,
					'lms_course_id': lms_course.id
				})
			for module in latest_lms_course.module_ids:
				new_module = self.env['ixlms.module'].create({
					'name':module.name,
					'sequence':module.sequence,
					'lms_course_id': lms_course.id,
				})
				for chapter in module.chapter_ids:
					self.env['ixlms.chapter'].create({
						'name': chapter.name,
						'sequence': chapter.sequence,
						'module_id': new_module.id,
						'lms_course_id': lms_course.id,
						'nsessions': chapter.nsessions,
						'resource_ids': [(6, 0, [resource.id for resource in chapter.resource_ids])]
					})
				for assessment in module.assessment_ids:
					self.env['ixlms.assessment'].create({
						'name': assessment.name,
						'description': assessment.description,
						'lms_course_id': lms_course.id,
						'module_id': new_module.id,
						'technique_id': techniques[assessment.technique_id.id].id,
						'graded': assessment.graded,
						'points': assessment.points,
						'percentage': assessment.percentage,
						'grade_scale': assessment.grade_scale,
						'submission_type': assessment.submission_type,
						'is_file_req': assessment.is_file_req,
						'is_url_req': assessment.is_url_req,
						'is_text_req': assessment.is_text_req,
						'teamwork': assessment.teamwork,
					})
		return lms_course

	section_ids = fields.One2many(comodel_name='ixroster.section', inverse_name='lms_course_id', string='Sections', required=True)
	@api.constrains('section_ids')
	def _check_same_course_for_sections(self):
		for rec in self:
			if not rec.section_ids:
				continue
			course_id = rec.section_ids[0].course_id
			for section in rec.section_ids:
				if section.course_id != course_id:
					raise ValidationError('All sections should be of the same course!')
	
	timeslot_room_ids = fields.One2many(comodel_name='ixroster.section', inverse_name='lms_course_id', string='Time and Location', readonly=True)
	
	name = fields.Char(compute='_set_name')
	def _set_name(self):
		for rec in self:
			if rec.section_ids:
				name = rec.section_ids[0].name
				first = True
				for section in rec.section_ids:
					if first:
						first = False
						continue
					name += '/' + section.number
				rec.name = name
	
	color = fields.Integer(string='Color Index')	
	course_id = fields.Many2one(comodel_name='ix.course', compute='_course_id', store=True)
	@api.depends('section_ids')
	@api.onchange('section_ids')
	def _course_id(self):
		for rec in self:
			if rec.section_ids:
				rec.course_id = rec.section_ids[0].course_id

	school_id = fields.Many2one(comodel_name='ix.school', related='course_id.school_id', store=True)	
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

	instructor_id = fields.Many2one(comodel_name='ix.faculty', compute='_instructor_id', store=True)
	@api.depends('section_ids')
	def _instructor_id(self):
		for rec in self:
			if rec.section_ids:
				rec.instructor_id = rec.section_ids[0].instructor_id
	
	discipline_id = fields.Many2one(comodel_name='ix.discipline', compute='_discipline_id')
	def _discipline_id(self):
		for rec in self:
			if rec.section_ids:
				rec.discipline_id = rec.section_ids[0].discipline_id
	
	timeslot_room = fields.Char(compute='_timeslot_room')
	def _timeslot_room(self):
		for rec in self:
			timeslot_room = rec.section_ids[0].timeslot
			if len(rec.section_ids) > 1:
				timeslot_room = rec.section_ids[0].number + ': ' + timeslot_room
				first = True
				for section in rec.section_ids:
					if first:
						first = False
						continue
					timeslot_room += ' | ' + section.number + ': ' + section.timeslot
					if section.room_id:
						timeslot_room += ' / ' + section.room_id.name
			elif rec.section_ids[0].room_id:
				timeslot_room += ' / ' + rec.section_ids[0].room_id.name
			rec.timeslot_room = timeslot_room
	
	student_ids = fields.One2many('ix.student', compute='_student_ids')
	def _student_ids(self):		
		for rec in self:
			student_ids = []
			for section in rec.section_ids:
				for student in section.student_ids:
					student_ids.append(student.id)
			
			if len(student_ids) > 0:
				rec.student_ids = student_ids
			else:
				rec.student_ids = False
	
	enrollment_ids = fields.One2many('ixroster.enrollment', compute='_enrollment_ids')
	def _enrollment_ids(self):
		for rec in self:
			rec.enrollment_ids = self.env['ixroster.enrollment'].search([('section_id', 'in', rec.section_ids.ids), ('state', 'in', ['enrolled', 'withdrawn', 'completed'])])
	
	nstudents = fields.Integer(compute='_nstudents')
	def _nstudents(self):
		for rec in self:
			nstudents = 0
			for section in rec.section_ids:
				nstudents += section.nstudents
			rec.nstudents = nstudents
	description = fields.Html('description')
	lms_course_ilo_ids = fields.One2many(comodel_name='ixlms.course.ilo', inverse_name='lms_course_id', string='ILOs')	
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

	assessment_remarks = fields.Html(string='Remarks')
	
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
	has_details = fields.Boolean(compute='_has_details')
	
	def _has_details(self):
		stripper = re.compile('<.*?>')
		for rec in self:			
			rec.has_details = rec.details and len(re.sub(stripper, '', rec.details).strip()) > 0

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
		domain = [('section_id', 'in', self.section_ids.ids), ('state', 'in', ['enrolled', 'withdrawn', 'completed'])]
		if len (self.section_ids) == 1:
			return self._expand_to('ixlms.action_enrollment', domain)
		
		return self._expand_to('ixlms.action_enrollment_by_section', domain)

	def get_my(self):
		self.ensure_one()
		domain = [('section_id', 'in', self.section_ids.ids), ('student_id', '=', self.env.user.student_id.id), ('state', 'in', ['enrolled', 'withdrawn', 'completed'])]
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
		if len (self.section_ids) > 1:
			context['group_by'] = 'section_id'
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

