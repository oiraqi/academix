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

from odoo import api, fields, models


class Component(models.Model):
    _name = 'ixcatalog.component'
    _description = 'Program Component'
    _inherit = 'ix.school.owned'

    name = fields.Char(string='Name', required=True)
    sch = fields.Integer(string='SCH', required=True)
    
    level = fields.Selection(
        [('u', 'Undergraduate'), ('g', 'Graduate')], 'Level', default='u', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    program_ids = fields.Many2many(
        'ixcatalog.program', 'ixcatalog_program_component_rel', 'component_id', 'program_id', string='Programs')
    parent_id = fields.Many2one(
        comodel_name='ixcatalog.component', string='Parent Component')
    child_ids = fields.One2many(
        comodel_name='ixcatalog.component', inverse_name='parent_id', string='Sub-components')
    course_ids = fields.Many2many(
        'ix.course', 'ixcatalog_component_course_rel', 'component_id', 'course_id', string='Courses')
    hide_children = fields.Boolean(
        compute='_compute_hide_children', string='hide_children')

    @api.depends('child_ids')
    def _compute_hide_children(self):
        for rec in self:
            rec.hide_children = not (rec.child_ids or self.env.ref('ix.group_setup') in self.sudo().env.user.groups_id or self.env.ref('ix.group_coordinator') in self.sudo().env.user.groups_id)            

    hide_courses = fields.Boolean(
        compute='_compute_hide_courses', string='hide_courses')

    @api.depends('course_ids')
    def _compute_hide_courses(self):
        for rec in self:
            if rec.course_ids or self.env.ref('ix.group_setup') in self.sudo().env.user.groups_id or self.env.ref('ix.group_coordinator') in self.sudo().env.user.groups_id:
                rec.hide_courses = False
            else:
                rec.hide_courses = True
