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


class RPProcess(models.Model):
    _inherit = 'a3performance.process'
    _description = 'Process Projection on RP'

    rp_goal_ids = fields.One2many('a3performance.rp.goal', 'process_id', string='Goals')
    rp_goal_progress = fields.Float('Goal Progress', compute='_rp_goal_progress')
    rp_goal_achievement = fields.Char('Goal Achievement', compute='_rp_goal_progress')
    
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

    research_activity_ids = fields.One2many(
        'a3research.activity', string='Activities', compute='_research_activity_ids')
    article_impact_ids = fields.One2many(
        'a3research.article', string='Impact Factor', compute='_article_impact_ids')
    article_indexed_ids = fields.One2many(
        'a3research.article', string='Indexed', compute='_article_indexed_ids')
    article_non_indexed_ids = fields.One2many(
        'a3research.article', string='Non Indexed', compute='_article_non_indexed_ids')
    book_ids = fields.One2many(
        'a3research.book', string='Books / Monographs', compute='_book_ids')
    paper_ids = fields.One2many(
        'a3research.paper', string='Papers', compute='_paper_ids')
    presentation_ids = fields.One2many(
        'a3research.presentation', string='Presentations', compute='_presentation_ids')
    
    rp_narrative = fields.Html('Narrative',
        readonly=True, states={'faculty': [('readonly', False)]})

    rp_committee_review = fields.Html('Committee Review',
        readonly=True, states={'committee': [('readonly', False)]},
        groups='a3.group_committee_member,a3.group_dean,a3.group_vpaa')
    rp_dean_review = fields.Html('Dean Review',
        readonly=True, states={'dean': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
    rp_vpaa_review = fields.Html('VPAA Review',
        readonly=True, states={'vpaa': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
