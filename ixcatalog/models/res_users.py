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


class ResUsers(models.Model):
    _inherit = 'res.users'

    managed_program_ids = fields.One2many(comodel_name='ixcatalog.program', compute='_managed_program_ids')

    def _managed_program_ids(self):
        if self.env.ref('ix.group_faculty') not in self.env.user.groups_id:
            for rec in self:
                rec.managed_program_ids = False
        else:
            for rec in self:
                if self.env.user.faculty_id:
                    managed_program_ids = [program.id for program in self.env.user.faculty_id.managed_program_ids]
                    if len(managed_program_ids) > 0:
                        rec.managed_program_ids = managed_program_ids
                    else:
                        rec.managed_program_ids = False
                else:
                    rec.managed_program_ids = False