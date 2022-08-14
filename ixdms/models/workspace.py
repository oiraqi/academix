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


class Workspace(models.Model):
    _inherit = 'ixdms.node'

    workspace_id = fields.Many2one(comodel_name='ixdms.node', string='Workspace', compute='_workspace_id')
    admin_ids = fields.Many2many(
        comodel_name='res.users', relation='ixdms_admin_workspace_user_rel', string='Admins')

    def _workspace_id(self):
        for rec in self:
            if rec.scope != 'workspace':
                rec.workspace_id = False
            elif not rec.parent_id:
                rec.workspace_id = rec
            else:
                rec.workspace_id = rec.parent_id.workspace_id
    