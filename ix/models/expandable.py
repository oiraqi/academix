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

from odoo import models


class Expandable(models.AbstractModel):
    _name = 'ix.expandable'
    _description = 'Expandable Mixin'

    def _expand_to(self, action_id, domain=False, context=False, res_id=False):
        action = self.env['ir.actions.act_window']._for_xml_id(action_id)
        if domain:
            action['domain'] = domain
        if context:
            action['context'] = context
        if res_id:
            action['res_id'] = res_id
        return action
    