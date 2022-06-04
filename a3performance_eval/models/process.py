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

from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date

SEMESTERS = {'1': 'Fall', '2': 'Spring', '3': 'Summer'}

class Process(models.Model):
    _name = 'a3performance.eval.process'
    _description = 'Evaluation Process'
    _inherit = ['a3.faculty.owned', 'mail.thread']
    _inherits = {'a3performance.eval.ts.process': 'ts_process_id',
                 'a3performance.eval.rp.process': 'rp_process_id',
                 'a3performance.eval.sd.process': 'sd_process_id'}
    _sql_constraints = [('a3performance.eval.process_ukey', 'unique(from_year,to_year,from_semester,to_semester)', 'An evaluation process for the selected period already exists')]

    @api.model
    def _from_year_selection(self):
        current_year = date.today().year
        year = current_year - 5
        year_list = []
        while year <= current_year:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    @api.model
    def _to_year_selection(self):
        current_year = date.today().year
        year = current_year
        year_list = []
        while year <= current_year + 5:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    @api.model
    def _latest_evaluation_year_selection(self):
        current_year = date.today().year
        year = current_year - 3
        year_list = []
        while year <= current_year:
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    name = fields.Char('Evaluation Process', compute='_set_name')
    hiring_date = fields.Date(related='faculty_id.hiring_date')
    rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'Rank', default=lambda self: self.env['a3.faculty'].search(
            [('partner_id', '=', self.env.user.partner_id.id)]).rank, required=True)
    srank_id = fields.Many2one('a3performance.srank', string='Sub-Rank', default=lambda self: self.env['a3.faculty'].search(
            [('partner_id', '=', self.env.user.partner_id.id)]).srank_id, required=True)
    state = fields.Selection([('faculty', 'Faculty'), ('f2c', 'Submitted'),
                             ('committee', 'Committee'), ('c2d',
                              'Submitted'), ('dean', 'Dean / Director'),
                             ('d2v', 'Submitted'), ('vpaa', 'VPAA'), ('done', 'Done')],
                             'Progress', default='faculty', required=True, tracking=True)
    type = fields.Selection(
        [('srank', 'Sub-Rank'), ('rank', 'Rank')], 'Evaluation Type', default='srank', required=True,
        readonly=True, states={'faculty': [('readonly', False)]})
    from_year = fields.Selection(_from_year_selection, 'From Year', required=True,
                               readonly=True, states={'faculty': [('readonly', False)]},
                               default=lambda self: str(date.today().year))
    from_semester = fields.Selection(
        [('1', 'Spring'), ('3', 'Fall')], 'From', default='1', required=True,
        readonly=True, states={'faculty': [('readonly', False)]})
    to_year = fields.Selection(_to_year_selection, 'To Year', required=True,
                             readonly=True, states={'faculty': [('readonly', False)]})
    to_semester = fields.Selection(
        [('1', 'Spring'), ('3', 'Fall')], 'To', default='3', required=True,
        readonly=True, states={'faculty': [('readonly', False)]})
    period = fields.Char('Period under Evaluation', compute='_set_name')
    
    previous_evaluation = fields.Boolean('Evaluated before?', default=True, readonly=True, states={'faculty': [('readonly', False)]})
    previous_process_id = fields.Many2one('a3performance.eval.process', string='Previous Evaluation')

    ts_goal_ids = fields.One2many('a3performance.eval.ts.goal', 'process_id', string='Goals')
    ts_goal_progress = fields.Float('Goal Progress', compute='_ts_goal_progress')
    ts_goal_achievement = fields.Char('Goal Achievement', compute='_ts_goal_progress')

    sd_goal_ids = fields.One2many('a3performance.eval.sd.goal', 'process_id', string='Goals')
    sd_goal_progress = fields.Float('Goal Progress', compute='_sd_goal_progress')
    sd_goal_achievement = fields.Char('Goal Achievement', compute='_sd_goal_progress')

    rp_goal_ids = fields.One2many('a3performance.eval.rp.goal', 'process_id', string='Goals')
    rp_goal_progress = fields.Float('Goal Progress', compute='_rp_goal_progress')
    rp_goal_achievement = fields.Char('Goal Achievement', compute='_rp_goal_progress')

    ts_process_id = fields.Many2one(
        'a3performance.eval.ts.process', string='TS Process', required=True)
    rp_process_id = fields.Many2one(
        'a3performance.eval.rp.process', string='RP Process', required=True)
    sd_process_id = fields.Many2one(
        'a3performance.eval.sd.process', string='SD Process', required=True)

    overall_self_evaluation = fields.Html('Overall Self-Evaluation',
                                  readonly=True, states={'faculty': [('readonly', False)]})

     
    @api.constrains('from_year', 'from_semester', 'to_year', 'to_semester')
    def _check_period(self):
        for rec in self:
            if rec.from_year > rec.to_year or (rec.from_year == rec.to_year and rec.from_semester > rec.to_semester):
                raise UserError(
                    'From Year/Semester should be before To Year/Semester')

    @api.onchange('from_year', 'to_year', 'from_semester', 'to_semester')     
    def _set_name(self):
        for rec in self:
            if rec.from_year and rec.from_semester and rec.to_year and rec.to_semester:
                rec.period = SEMESTERS[rec.from_semester] + ' ' + rec.from_year + ' - ' + SEMESTERS[rec.to_semester] + ' ' + rec.to_year
                if rec.faculty_id:
                    rec.name = rec.faculty_id.name + ' / ' + rec.period
    
    @api.onchange('from_year', 'type')
    def _update_to_year(self):
        for rec in self:
            if rec.type == 'srank':
                if int(rec.from_year) + 1 >= date.today().year:
                    rec.to_year = str(int(rec.from_year) + 1)
                else:
                    rec.to_year = str(date.today().year)
            else:
                if int(rec.from_year) + 5 >= date.today().year:
                    rec.to_year = str(int(rec.from_year) + 5)
                else:
                    rec.to_year = str(date.today().year)
    
    @api.onchange('from_semester')
    def _update_to_semester(self):
        for rec in self:
            if rec.from_semester == '1':
                rec.to_semester = '3'
            elif rec.from_semester == '3':
                rec.to_semester = '1'

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

    def _sd_goal_progress(self):
        for rec in self:
            goal_count = len(rec.sd_goal_ids)
            if goal_count == 0:
                rec.sd_goal_progress = 0
                rec.sd_goal_achievement = '0 / 0'
                continue
            
            achieved_goal_count = sum(1 for goal in rec.sd_goal_ids if goal.achieved)
            rec.sd_goal_progress = round(100 * achieved_goal_count / goal_count)
            rec.sd_goal_achievement = str(achieved_goal_count) + ' / ' + str(goal_count)

    def _rp_goal_progress(self):
        for rec in self:
            goal_count = len(rec.rp_goal_ids)
            if goal_count == 0:
                rec.rp_goal_progress = 0
                rec.rp_goal_achievement = '0 / 0'
                continue
            
            achieved_goal_count = sum(1 for goal in rec.rp_goal_ids if goal.achieved)
            rec.rp_goal_progress = round(100 * achieved_goal_count / goal_count)
            rec.rp_goal_achievement = str(achieved_goal_count) + ' / ' + str(goal_count)
