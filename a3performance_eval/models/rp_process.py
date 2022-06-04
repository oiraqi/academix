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
    _name = 'a3performance.eval.rp.process'
    _description = 'Process Projection on RP'

    research_activity_ids = fields.One2many(
        'a3performance.rp.activity', string='Activities', compute='_research_activity_ids')
    article_impact_ids = fields.One2many(
        'a3performance.rp.article', string='Impact Factor', compute='_article_impact_ids')
    article_indexed_ids = fields.One2many(
        'a3performance.rp.article', string='Indexed', compute='_article_indexed_ids')
    article_non_indexed_ids = fields.One2many(
        'a3performance.rp.article', string='Non Indexed', compute='_article_non_indexed_ids')
    book_ids = fields.One2many(
        'a3performance.rp.book', string='Books / Monographs', compute='_book_ids')
    paper_ids = fields.One2many(
        'a3performance.rp.paper', string='Papers', compute='_paper_ids')
    presentation_ids = fields.One2many(
        'a3performance.rp.presentation', string='Presentations', compute='_presentation_ids')
    
    rp_narrative = fields.Html('Narrative',
        readonly=True, states={'faculty': [('readonly', False)]})
