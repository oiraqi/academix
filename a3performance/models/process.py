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

SEMESTERS = {'1': 'FA', '2': 'SP'}

class Process(models.Model):
    _name = 'a3performance.process'
    _description = 'Evaluation Process'
    _inherit = ['a3.faculty.owned', 'mail.thread']
    _sql_constraints = [('from_to_ukey', 'unique(from_year, to_year, from_semester, to_semester)', 'An evaluation process for the selected period already exists')]

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

    name = fields.Char('Evaluation Process', compute='_set_name', store=True)
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
        [('1', 'Spring'), ('3', 'Fall')], 'From', default='2', required=True,
        readonly=True, states={'faculty': [('readonly', False)]})
    to_year = fields.Selection(_to_year_selection, 'To Year', required=True,
                             readonly=True, states={'faculty': [('readonly', False)]})
    to_semester = fields.Selection(
        [('1', 'Spring'), ('3', 'Fall')], 'To', default='1', required=True,
        readonly=True, states={'faculty': [('readonly', False)]})
    period = fields.Char('Period under Evaluation', compute='_set_name')
    
    previous_evaluation = fields.Boolean('Evaluated before?', default=True, readonly=True, states={'faculty': [('readonly', False)]})
    previous_process_id = fields.Many2one('a3performance.process', string='Previous Evaluation')

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
                rec.name = rec.period + '-' + 'Eval'
                if rec.faculty_id:
                    rec.name += ' - ' + rec.faculty_id.name
    
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

    # Committee section
    committee_state_datetime = fields.Datetime()    
    committee_recommendation = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Recommendation',
        readonly=True, states={'committee': [('readonly', False)]},
        groups='a3performance.group_committee_member,a3.group_dean,a3.group_vpaa')
    committee_feedback = fields.Html("Feedback",
                                     readonly=True, states={'committee': [('readonly', False)]},
                                     groups='a3performance.group_committee_member,a3.group_dean,a3.group_vpaa')

    # Dean section
    dean_recommendation = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Recommendation',
        readonly=True, states={'dean': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
    dean_new_rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'New Rank',
        readonly=True, states={'dean': [('readonly', False)]},
        attrs="{'invisible': [('dean_recommendation', '=', 'not_promote')], 'required': [('dean_recommendation', '=', 'promote')]}",
        groups='a3.group_dean,a3.group_vpaa')
    dean_new_srank_id = fields.Many2one('a3performance.srank', string='New Sub-Rank',
                                        readonly=True, states={'dean': [('readonly', False)]},
                                        attrs="{'invisible': [('dean_recommendation', '=', 'not_promote')], 'required': [('dean_recommendation', '=', 'promote')]}",
                                        groups='a3.group_dean,a3.group_vpaa')
    dean_feedback = fields.Html("Feedback",
                                readonly=True, states={'dean': [('readonly', False)]},
                                groups='a3.group_dean,a3.group_vpaa')

    # VPAA section
    vpaa_decision = fields.Selection(
        [('promote', 'Promote'), ('not_promote', "Don't promote")], 'Decision',
        readonly=True, states={'vpaa': [('readonly', False)]})
    vpaa_new_rank = fields.Selection([('D', 'Lecturer'), ('C', 'Assistant Professor'), (
        'B', 'Associate Professor'), ('A', 'Full Professor')], 'New Rank',
        readonly=True, states={'vpaa': [('readonly', False)]},
        attrs="{'invisible': [('vpaa_decision', '=', 'not_promote')], 'required': [('vpaa_decision', '=', 'promote')]}")
    vpaa_new_srank_id = fields.Many2one('a3performance.srank', string='New Sub-Rank',
                                        readonly=True, states={'vpaa': [('readonly', False)]},
                                        attrs="{'invisible': [('vpaa_decision', '=', 'not_promote')], 'required': [('vpaa_decision', '=', 'promote')]}")
    vpaa_feedback = fields.Html("Feedback",
                                readonly=True, states={'vpaa': [('readonly', False)]})

    
    # Workflow section
    def faculty_to_f2c(self):
        self.write({'state': 'f2c'})

    def f2c_to_faculty(self):
        self.write({'state': 'faculty'})

    def f2c_to_committee(self):
        self.ensure_one()
        self.write(
            {'state': 'committee', 'committee_state_date': fields.Datetime.now()})

    def committee_to_f2c(self):
        self.ensure_one()
        self.write({'state': 'f2c'})

    def committee_to_c2d(self):
        self.write({'state': 'c2d'})

    def c2d_to_committee(self):
        self.write({'state': 'committee'})

    def c2d_to_dean(self):
        # verify all required fields, e.g., committee feedback, have been filled
        self.write({'state': 'dean'})

    def dean_to_c2d(self):
        self.write({'state': 'c2d'})

    def dean_to_d2v(self):
        # verify all required fields, e.g., dean_new_srank_id or dean_new_rank, have been filled
        self.write({'state': 'd2v'})

    def d2v_to_dean(self):
        self.write({'state': 'dean'})

    def d2v_to_vpaa(self):
        self.write({'state': 'vpaa'})

    def vpaa_to_d2v(self):
        self.write({'state': 'd2v'})

    def vpaa_to_done(self):
        # verify all required fields, e.g., dean_new_srank_id or dean_new_rank, have been filled
        self.ensure_one()
        self.write({'state': 'done'})
    