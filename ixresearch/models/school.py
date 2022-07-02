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

from odoo import api, fields, models


class School(models.Model):
    _inherit = 'ix.school'

    article_ids = fields.One2many(comodel_name='ixresearch.article', inverse_name='school_id', string='Articles')
    book_ids = fields.One2many(comodel_name='ixresearch.book', inverse_name='school_id', string='Books')
    paper_ids = fields.One2many(comodel_name='ixresearch.paper', inverse_name='school_id', string='Papers')
    presentation_ids = fields.One2many(comodel_name='ixresearch.presentation', inverse_name='school_id', string='Presentaions')
    
