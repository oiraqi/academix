from odoo import api, fields, models


class StandardEvent(models.Model):
    _name = 'a3calendar.standard.event'
    _description = 'Standard Event'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
    standard_considerations = fields.Html(string='Standard Considerations')    
