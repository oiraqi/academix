# -*- coding: utf-8 -*-
###############################################################################
#
#    Al Akhawayn University in Ifrane -- AUI
#    Copyright (C) 2022-TODAY AUI(<http://www.a3ma>).
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


class TSProcess(models.Model):
    _name = 'a3performance.eval.ts.process'
    _description = 'Process Projection on TS'

    student_evaluation_ids = fields.One2many(
        'a3performance.ts.student.evaluation', string='Student Evaluation', compute='_student_evaluation_ids')
    class_observation_ids = fields.One2many(
        'a3performance.ts.class.observation', string='Class Observation', compute='_class_observation_ids')
    action_ids = fields.One2many(
        'a3performance.ts.action', string='Actions', compute='_action_ids')
    supervision_ids = fields.One2many(
        'a3performance.ts.supervision', string='Supervised Projects', compute='_supervision_ids')
    
    ts_narrative = fields.Html('Narrative',
        readonly=True, states={'faculty': [('readonly', False)]})
