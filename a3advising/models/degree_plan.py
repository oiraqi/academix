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
from odoo.exceptions import UserError


class DegreePlan(models.Model):
    _name = 'a3advising.degree.plan'
    _description = 'Student Degree Plan'
    _inherit = ['a3.faculty.student.shared', 'a3.activity']
    _sql_constraints = [('student_ukey',
                         'unique(student_id)', 'A student can only have one degree plan')]
    
    name = fields.Char(related='student_id.name')
    program_id = fields.Many2one('a3catalog.program', related='student_id.program_id')
    pace = fields.Selection(
        [('4', '4'), ('5', '5'), ('6', '6')], string='Pace', default='5', required=True)
    take_summer = fields.Selection(string='Take Summer', selection=[(
        'never', 'Never'), ('half', '1 / 2'), ('always', 'Always')], default='half')

    def generate(self):
        self.ensure_one()
        planned_course_ids = []
        program_course_ids = []
        for component in self.program_id.component_ids:
            for course in component.course_ids:
                program_course_ids.append(course.id)

        semester = self.semester
        iyear = self.term_id.year

        while self._plan_for_semester(planned_course_ids, program_course_ids, semester, iyear):
            if semester == '1':
                iyear = iyear + 1
                semester = '2'
            elif semester == '2':
                semester = '3'
            else:
                semester = '1'

    def _plan_for_semester(self, planned_course_ids, program_course_ids, semester, iyear):
        offered_in_condition = ()
        if semester == '1':
            offered_in_condition = ('offered_in_fall', '=', True)
        elif semester == '2':
            offered_in_condition = ('offered_in_spring', '=', True)
        elif semester == '3':
            offered_in_condition = ('offered_in_summer', '=', True)
        
        candidate_course_ids = self.env['a3.course'].search([
            ('id', 'not in', planned_course_ids),
            ('id', 'in', program_course_ids),
            offered_in_condition], order='number')

        if not candidate_course_ids:
            # Was it due to non offerings in this semester?
            # Let's check, and it is the case, let's move on
            # to the next one
            return self.env['a3.course'].search_count([('id', 'not in', planned_course_ids),
            ('id', 'in', program_course_ids)]) > 0

        pace = ord(self.pace) - 48 if semester != '3' else 2
        
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
                    self._plan_courses(temp_planned_co_course_ids, semester, iyear, planned_course_ids)
                    self._plan_courses(temp_planned_course_ids, semester, iyear, planned_course_ids)
                    return True
            
            # Go back to corequisites, missed earlier in
            # inverted corequisite anticipation
            unsatisfied_prerequisite_of_corequisite = False
            for corequisite in course.corequisite_ids:
                if corequisite is None:
                    raise UserError(course.corequisite_ids)
                if corequisite.id in temp_planned_co_course_ids or corequisite.id in planned_course_ids:
                    # Corequisite already added. Skip.
                    continue
                
                if not self._prerequisites_fulfilled(corequisite, planned_course_ids):
                    unsatisfied_prerequisite_of_corequisite = True
                    break

                while len(temp_planned_course_ids) > 0 and len(temp_planned_course_ids) + len(temp_planned_co_course_ids) > pace - 2:
                    # Free room for co-courses, for optimization
                    temp_planned_course_ids.pop()
                
                if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) <= pace - 2:
                    # Plan them together
                    temp_planned_co_course_ids.append(course)
                    temp_planned_co_course_ids.append(corequisite)
                elif len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace - 1:
                    # Room for one course only
                    temp_planned_course_ids.append(course)
                if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace: # Don't mislead for else
                    # Pace reached, we're done for this semester
                    # Plan retained courses and leave
                    self._plan_courses(temp_planned_co_course_ids, semester, iyear, planned_course_ids)
                    self._plan_courses(temp_planned_course_ids, semester, iyear, planned_course_ids)
                    return True
                
            if unsatisfied_prerequisite_of_corequisite:
                # Skip this course as at least a prerequisite of its 
                continue            
            temp_planned_course_ids.append(course)
            if len(temp_planned_course_ids) + len(temp_planned_co_course_ids) == pace:                
                # Pace reached, we're done for this semester
                # Plan retained courses and leave
                self._plan_courses(temp_planned_co_course_ids, semester, iyear, planned_course_ids)
                self._plan_courses(temp_planned_course_ids, semester, iyear, planned_course_ids)
                return True
        
        self._plan_courses(temp_planned_co_course_ids, semester, iyear, planned_course_ids)
        self._plan_courses(temp_planned_course_ids, semester, iyear, planned_course_ids)
        return True

    def _plan_courses(self, courses, semester, iyear, planned_course_ids):
        if semester == '1':
            year = str(iyear - 2000) + '/' + str(iyear - 1999)
        else:
            year = str(iyear - 2001) + '/' + str(iyear - 2000)
        for course in courses:
            self.env['a3advising.planned.course'].create({
                'course_id': course.id,
                'student_id': self.student_id.id,
                'school_id': self.student_id.school_id.id,
                'semester': semester,
                'year': year,                
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
