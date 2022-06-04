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

from odoo import models, fields, api
from odoo.exceptions import UserError

class Experience(models.Model):
    _name = 'a3performance.sd.experience'
    _inherit = 'a3.faculty.owned'

    company = fields.Char('Company', required=True)
    position = fields.Char('Position', required=True)
    duties = fields.Html('Duties', required=True)
    from_date = fields.Date('From', required=True)
    to_date = fields.Date('To', required=True)

    @api.constrains('from_date', 'to_date')
    def _check(self):
        for rec in self:
            if rec.to_date <= rec.from_date:
                raise UserError('From date should be before To date')
