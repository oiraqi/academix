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

import urllib
import json
import base64
from odoo import models, fields, api


class Textbook(models.Model):
    _name = 'ixlms.textbook'
    _sql_constraints = [('isbn_ukey', 'unique(isbn)',
                         ('A book with the same ISBN exists already!'))]    
    
    name = fields.Char('Title', size=128, required=True)
    isbn = fields.Char('ISBN (10 or 13)', size=13, required=True)
    thumbnail = fields.Binary('Cover')
    authors = fields.Text(string='Author(s)', required=True)
    edition = fields.Char('Edition', required=True)
    description = fields.Text('Description')
    publisher = fields.Char('Publisher', required=True)
    course_id = fields.Many2one('ix.course', 'Course', required=True)
    
    @api.onchange('isbn')
    def onchange_isbn(self):
        for rec in self:
            if rec.isbn and (len(rec.isbn) == 10 or len(rec.isbn) == 13):
                response = urllib.request.urlopen(
                    'https://www.googleapis.com/books/v1/volumes?q=isbn:' + rec.isbn)
                book = json.loads(response.read())
                if book.get('totalItems') and book["totalItems"] == 1:
                    book_info = book["items"][0]["volumeInfo"]
                    rec.name = book_info.get('title')
                    rec.description = book_info.get('description')
                    rec.edition = book_info.get('publishedDate')

                    if book_info.get('authors'):
                        rec.authors = ', '.join(book_info['authors'])

                    if book_info.get('publisher'):                   
                        rec.publisher = book_info["publisher"]

                    if book_info.get('imageLinks') and book_info["imageLinks"].get('smallThumbnail'):
                        response = urllib.request.urlopen(
                            book_info["imageLinks"]["smallThumbnail"])
                        rec.thumbnail = base64.encodebytes(response.read())
    