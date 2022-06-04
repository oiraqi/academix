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

from odoo import models, fields


class TSProcess(models.Model):
    _inherit = 'a3performance.eval.ts.process'
    
    ts_committee_review = fields.Html('Committee Review',
        readonly=True, states={'committee': [('readonly', False)]},
        groups='a3.group_committee_member,a3.group_dean,a3.group_vpaa')
    ts_dean_review = fields.Html('Dean Review',
        readonly=True, states={'dean': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
    ts_vpaa_review = fields.Html('VPAA Review',
        readonly=True, states={'vpaa': [('readonly', False)]},
        groups='a3.group_dean,a3.group_vpaa')
