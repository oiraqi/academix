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


class Publication(models.AbstractModel):
    _name = 'ixresearch.publication'
    _inherit = 'ix.faculty.activity'

    name = fields.Text('Title', required=True)
    authors = fields.Text('Authors', required=True)
    authorship = fields.Selection(string='Authorship', selection=[('single', 'Single Author'), ('first', 'First Author'), ('author', 'Author')])    
    publisher_id = fields.Many2one('ixresearch.publisher', 'Publisher', required=True)
    date = fields.Date('Date of Publication', required=True)
    isn = fields.Char('ISBN/ISSN', required=True)
    doi = fields.Char('DOI')
