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


class Course(models.Model):
    _inherit = 'ix.course'

    description = fields.Html(string='Description')
    sch = fields.Integer(compute='_compute_sch', string='SCH', store=True)    
    prerequisite_ids = fields.One2many(
        'ixcatalog.prerequisite', 'course_id', string='Prerequisites')
    corequisite_ids = fields.One2many(
        'ixcatalog.corequisite', inverse_name='course_id', string='Corequisites')
    prerequisite_for_ids = fields.One2many(
        'ix.course', compute='_prerequisite_for_ids', string='Prerequisite For')
    corequisite_for_ids = fields.One2many(
        'ix.course', compute='_corequisite_for_ids', string='Corequisite For')
    component_ids = fields.Many2many(
        'ixcatalog.component', 'ixcatalog_component_course_rel', 'course_id', 'component_id', string='Components')
    req_class = fields.Selection(string='Required Classification', selection=[
                                 ('soph', 'Sophomore'), ('jun', 'Junior'), ('sen', 'Senior')])
    remarks = fields.Text(string='Remarks')
    session_ids = fields.Many2many(comodel_name='ix.session', string='Offered in')    
    is_internship = fields.Boolean(string='Internship', default=False)
    ilo_ids = fields.One2many('ixcatalog.course.ilo', 'course_id', string='ILOs')
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


    def _corequisite_ids(self):
        for rec in self:
            corequisites = self.env['ixcatalog.corequisite'].search(
                [('course_id', '=', rec.id)])
            if not corequisites:
                rec.corequisite_ids = False
            else:
                rec.corequisite_ids = [corequisite.corequisite_id.id for corequisite in corequisites]            

    def _corequisite_for_ids(self):
        for rec in self:
            corequisites = self.env['ixcatalog.corequisite'].search(
                [('corequisite_id', '=', rec.id)])
            if not corequisites:
                rec.corequisite_for_ids = False
            else:            
                rec.corequisite_for_ids = [corequisite.course_id.id for corequisite in corequisites]            

    def _prerequisite_for_ids(self):
        for rec in self:
            prerequisites = self.env['ixcatalog.prerequisite'].search(
                [('alternative_ids', 'in', rec.id)])
            if not prerequisites:
                rec.prerequisite_for_ids = False
            else:            
                rec.prerequisite_for_ids = [prerequisite.course_id.id  for prerequisite in prerequisites]

    @api.depends('code')
    def _compute_sch(self):
        for rec in self:
            rec.sch = len(rec.code) > 5 and rec.code[5] >= '0' and rec.code[5] <= '5' and int(
                rec.code[5]) or 0
