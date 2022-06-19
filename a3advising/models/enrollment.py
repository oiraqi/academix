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

from odoo import fields, models


class Enrollment(models.Model):
    _inherit = 'a3roster.enrollment'

    advisor_id = fields.Many2one(related='student_id.advisor_id')

    def app_w_adv(self):
        # Don't trust the interface, perform the server-side check!
        # If someone is playing with us, drop silently
        if self.env.ref('a3.group_faculty') in self.env.user.groups_id and self.student_id.advisor_id.user_id == self.env.user:
            self.wstate = 'wadv'
