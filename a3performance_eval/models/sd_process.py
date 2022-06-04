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

class SDProcess(models.Model):
    _name = 'a3performance.eval.sd.process'
    _description = 'Process Projection on SD'

    committee_school_activity_ids = fields.One2many(
        'a3performance.sd.activity', string='School Committees', compute='_committee_school_activity_ids')
    committee_university_activity_ids = fields.One2many(
        'a3performance.sd.activity', string='University Committees', compute='_committee_university_activity_ids')
    development_ids = fields.One2many(
        'a3performance.sd.development', string='Development', compute='_development_ids')
    experience_ids = fields.One2many(
        'a3performance.sd.experience', string='Experiences', compute='_experience_ids')
    service_ids = fields.One2many(
        'a3performance.sd.service', string='Services', compute='_service_ids')
    
    sd_narrative = fields.Html('Narrative',
        readonly=True, states={'faculty': [('readonly', False)]})
