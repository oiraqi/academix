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

class CommitteeActivity(models.Model):
    _name = 'a3performance.sd.committee.activity'
    _inherit = 'a3performance.sd.activity'
    _description = 'Committee Activities'

    committee_id = fields.Many2one('a3performance.sd.committee', string='Committee', required=True)
    role = fields.Selection([('chair', 'Chair'), ('member',
                            'Member')], 'Role', default='member', required=True)
    scope = fields.Selection(related='committee_id.scope', store=True)
