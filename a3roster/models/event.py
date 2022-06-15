from odoo import models, fields, api


class Event(models.Model):
    _inherit = 'calendar.event'
	
    
    reservation_id = fields.Many2one(comodel_name='a3roster.reservation', string='Reservation')
    
    @api.depends('start', 'stop', 'location')
    def update_reservation(self):
        for rec in self:
            if rec.reservation_id:
                if rec.start != rec.reservation_id.start_time:
                    rec.reservation_id.start_time = rec.start
                if rec.stop != rec.reservation_id.end_time:
                    rec.reservation_id.end_time = rec.stop
                if rec.location != rec.reservation_id.room_id.name:
                    rec.reservation_id.room_id = self.env['a3.room'].get_from_name(rec.location)