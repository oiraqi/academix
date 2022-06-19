import urllib
import json
import base64
from odoo import models, fields, api


class Textbook(models.Model):
    _name = 'a3lms.textbook'
    _sql_constraints = [('isbn_ukey', 'unique(isbn)',
                         ('A book with the same ISBN exists already!'))]    
    
    name = fields.Char('Title', size=128, required=True)
    isbn = fields.Char('ISBN Code', size=13, required=True)
    thumbnail = fields.Binary('Cover')
    authors = fields.Text(string='Author(s)', required=True)
    edition = fields.Char('Edition', required=True)
    description = fields.Text('Description')
    publisher = fields.Char('Publisher', required=True)
    course_id = fields.Many2one('a3.course', 'Course', required=True)
    
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
    