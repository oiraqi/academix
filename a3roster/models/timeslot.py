from odoo import fields, models, api


class TimeSlot(models.Model):
    _name = 'a3roster.timeslot'
    _description = 'Timeslot'
    _sql_constraints = [('timeslot_ukey', 'unique(start_time, end_time, days)', 'Time slot already defined!')]

    name = fields.Char('Name', compute='_compute_name', store=True)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    days = fields.Selection(string='Days', selection=[('MWF', 'MWF'), ('TR', 'TR')], default='MWF', required=True)

    @api.depends('start_time', 'end_time')
    @api.onchange('start_time', 'end_time')
    def _compute_name(self):
        for rec in self:
            if rec.start_time and rec.end_time and rec.days:
                start_hours = int(rec.start_time)
                start_minutes = (rec.start_time - start_hours) * 60
                start_time = str(start_hours) + ':' + str(start_minutes)
                end_hours = int(rec.end_time)
                end_minutes = (rec.end_time - end_hours) * 60
                end_time = str(end_hours) + ':' + str(end_minutes)
                rec.name = rec.days + ' ' + start_time + ' - ' + end_time
            else:
                rec.name = False
