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


class Process(models.Model):
    _inherit = 'a3performance.process'
    _description = 'Process Projection on TS'

    ts_goal_ids = fields.One2many('a3performance.ts.goal', 'process_id', string='Goals')
    ts_goal_progress = fields.Float('Goal Progress', compute='_ts_goal_progress')
    ts_goal_achievement = fields.Char('Goal Achievement', compute='_ts_goal_progress')

    def _ts_goal_progress(self):
        for rec in self:
            goal_count = len(rec.ts_goal_ids)
            if goal_count == 0:
                rec.ts_goal_progress = 0
                rec.ts_goal_achievement = '0 / 0'
                continue
            
            achieved_goal_count = sum(1 for goal in rec.ts_goal_ids if goal.achieved)
            rec.ts_goal_progress = round(100 * achieved_goal_count / goal_count)
            rec.ts_goal_achievement = str(achieved_goal_count) + ' / ' + str(goal_count)

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

    ts_committee_review = fields.Html('Committee Review',
        readonly=True, states={'committee': [('readonly', False)]},
        groups='a3.group_committee_member,a3.group_dean,a3.group_vpaa')
    ts_dean_review = fields.Html('Dean Review',
        readonly=True, states={'dean': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
    ts_vpaa_review = fields.Html('VPAA Review',
        readonly=True, states={'vpaa': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
