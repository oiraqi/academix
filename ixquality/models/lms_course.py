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

class LmsCourse(models.Model):
    _inherit = 'ixlms.course'

    @api.model
    def create(self, vals):
        course = super(LmsCourse, self).create(vals)
        for ilo in course.ilo_ids:
            for program in course.program_ids:
                self.env['ixquality.lms.course.ilo.program'].create({
                    'course_id': course.id,
                    'ilo_id': ilo.id,
                    'program_id': program.id
                })
        return course

    ilo_program_ids = fields.One2many('ixquality.lms.course.ilo.program', inverse_name='lms_course_id', groups="ix.group_faculty,ix.group_coordinator,ix.group_vpaa")
    acquisition_level = fields.Selection(string='Targetted Acquisition Level (TAL)', selection=[
		('3', '60%+'), ('4', '80%+'), ('5', 'Fully Acquired')], default='4', required=True)
    