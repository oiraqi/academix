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


class FacultyStudentShared(models.AbstractModel):
    _name = 'ix.faculty.student.shared'
    _description = 'A resource accessible by both a student and a faculty'

    faculty_id = fields.Many2one(
        'ix.faculty', string='Faculty', default=lambda self: self.env['ix.faculty'].search(
            [('user_id', '=', self.env.user.id)]))

    student_id = fields.Many2one(
        'ix.student', string='Student', default=lambda self: self.env['ix.student'].search(
            [('user_id', '=', self.env.user.id)]))

    school_id = fields.Many2one('ix.school', string='School', default=lambda self: self.env['ix.faculty'].search(
            [('user_id', '=', self.env.user.id)]).school_id or self.env['ix.student'].search(
            [('user_id', '=', self.env.user.id)]).school_id, required=True)
    
    locked = fields.Boolean('Locked', readonly=True, default=False)
