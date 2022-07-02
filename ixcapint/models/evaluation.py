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


class Evaluation(models.Model):
    _name = 'ixcapint.evaluation'
    _inherit = 'ix.faculty.owned'
    _description = 'Project Evaluation'

    project_id = fields.Many2one('ixcapint.project', string='Project', required=True)
    student_id = fields.Many2one('ix.student', related='project_id.student_id', store=True, readonly=True)
    
    supervisor = fields.Char(compute='_compute_supervisor', string='Supervisor?')
    
    @api.depends('project_id')
    def _compute_supervisor(self):
        for rec in self:
            rec.supervisor = rec.project_id.supervisor_id.user_id == rec.create_uid