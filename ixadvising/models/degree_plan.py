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

from odoo import fields, models


class DegreePlan(models.Model):
    _name = 'ixadvising.degree.plan'
    _description = 'Student Degree Plan'
    _inherit = ['ix.student.owned', 'ix.activity', 'ix.expandable']
    _sql_constraints = [('student_ukey',
                         'unique(student_id)', 'A student can only have one degree plan')]
    
    name = fields.Char(related='student_id.name')
    pace = fields.Selection(
        [('4', '4'), ('5', '5'), ('6', '6')], string='Pace', default='5', required=True)
    session_ids = fields.Many2many(comodel_name='ix.session', string='Sessions', required=True)
    progress = fields.Float(related='student_id.progress')    
    

    def get_degree_plan(self):
        self.ensure_one()
        self._generate()
        domain = [('student_id', '=', self.student_id.id)]
        context = {'default_student_id': self.student_id.id}
        return self._expand_to('ixadvising.action_planned_course', domain, context)

    def _generate(self):
        if self.env['ixadvising.planned.course'].search([('student_id', '=', self.student_id.id)]):
            return
        
        planned_course_ids = []
        program_course_ids = []
        for component in self.student_id.curriculum_id.component_ids:
            for course in component.course_ids:
                program_course_ids.append(course.id)

        term_id = self.term_id        

        while self._plan_for_semester(planned_course_ids, program_course_ids, term_id):
            term_id = term_id.get_or_create_next()

    def _plan_for_semester(self, planned_course_ids, program_course_ids, term_id):       
        candidate_course_ids = self.env['ix.course'].search([
            ('id', 'not in', planned_course_ids),
            ('id', 'in', program_course_ids),
            ('session_ids', 'in', term_id.session_id.id)], order='number')

        if not candidate_course_ids:
            # Was it due to non offerings in this semester?
            # Let's check, and it is the case, let's move on
            # to the next one
            return self.env['ix.course'].search_count([('id', 'not in', planned_course_ids),
            ('id', 'in', program_course_ids)]) > 0

        pace = ord(self.pace) - 48
        if pace > term_id.session_id.max_ncourses:
            pace = term_id.session_id.max_ncourses
        
        temp_planned_course_ids = []
        temp_planned_co_course_ids = []
        for course in candidate_course_ids:
            if not self._prerequisites_fulfilled(course, planned_course_ids):
                # To soon for this course
                continue            

            # Give priority to co-courses for optimization
            # Anticipate for inverted corequisites
            for co_course in course.corequisite_for_ids:
                if not self._prerequisites_fulfilled(co_course, planned_course_ids):
                    #To soon for this inverted corequisite
                    continue
                
                while len(temp_planned_course_ids) > 0 and len(temp_planned_course_ids) + len(temp_planned_co_course_ids) > pace - 2:
                    # Free room for higher-priority co-courses
                    temp_planned_course_ids.pop()
                
                if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) <= pace - 2:
                    # Plan them together
                    temp_planned_co_course_ids.append(course)
                    temp_planned_co_course_ids.append(co_course)
                elif len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace - 1:
                    # Room for one course only
                    temp_planned_course_ids.append(course)
                if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace: # Don't mislead for else
                    # Pace reached, we're done for this semester
                    # Plan retained courses and leave
                    self._plan_courses(temp_planned_co_course_ids, term_id, planned_course_ids)
                    self._plan_courses(temp_planned_course_ids, term_id, planned_course_ids)
                    return True
            
            # Go back to corequisites, missed earlier in
            # inverted corequisite anticipation
            unsatisfied_prerequisite_of_corequisite = False
            for corequisite in course.corequisite_ids:                
                if corequisite.corequisite_id.id in temp_planned_co_course_ids or corequisite.corequisite_id.id in planned_course_ids:
                    # Corequisite already added. Skip.
                    continue
                
                if not self._prerequisites_fulfilled(corequisite.corequisite_id, planned_course_ids):
                    unsatisfied_prerequisite_of_corequisite = True
                    break

                while len(temp_planned_course_ids) > 0 and len(temp_planned_course_ids) + len(temp_planned_co_course_ids) > pace - 2:
                    # Free room for co-courses, for optimization
                    temp_planned_course_ids.pop()
                
                if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) <= pace - 2:
                    # Plan them together
                    temp_planned_co_course_ids.append(course)
                    temp_planned_co_course_ids.append(corequisite.corequisite_id)
                elif len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace - 1:
                    # Room for one course only
                    temp_planned_course_ids.append(course)
                if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace: # Don't mislead for else
                    # Pace reached, we're done for this semester
                    # Plan retained courses and leave
                    self._plan_courses(temp_planned_co_course_ids, term_id, planned_course_ids)
                    self._plan_courses(temp_planned_course_ids, term_id, planned_course_ids)
                    return True
                
            if unsatisfied_prerequisite_of_corequisite:
                # Skip this course as at least a prerequisite of its 
                continue            
            temp_planned_course_ids.append(course)
            if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace:                
                # Pace reached, we're done for this semester
                # Plan retained courses and leave
                self._plan_courses(temp_planned_co_course_ids, term_id, planned_course_ids)
                self._plan_courses(temp_planned_course_ids, term_id, planned_course_ids)
                return True
        
        self._plan_courses(temp_planned_co_course_ids, term_id, planned_course_ids)
        self._plan_courses(temp_planned_course_ids, term_id, planned_course_ids)
        return True

    def _plan_courses(self, courses, term_id, planned_course_ids):        
        for course in courses:
            if not self.env['ixadvising.planned.course'].search([('course_id', '=', course.id), ('student_id', '=', self.student_id.id)]):
                self.env['ixadvising.planned.course'].create({
                'course_id': course.id,
                'student_id': self.student_id.id,
                'school_id': self.student_id.school_id.id,
                'term_id': term_id.id,       
                })
                planned_course_ids.append(course.id)

    def _prerequisites_fulfilled(self, course, planned_course_ids):
        for prerequisite in course.prerequisite_ids:
            fulfilled = False
            for alternative in prerequisite.alternative_ids:
                if alternative.id in planned_course_ids:
                    fulfilled = True
                    break
            if not fulfilled:
                return False
        return True
