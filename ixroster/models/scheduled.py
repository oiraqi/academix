from odoo import models, fields, api
from odoo.exceptions import UserError

class Scheduled(models.AbstractModel):
    _name = 'ixroster.scheduled'
    _description = 'Scheduled with recurrence'
    
    start_timeslot = fields.Float(string='Start Time', required=True)
    end_timeslot = fields.Float(string='End Time', required=True)
    monday = fields.Boolean(string='M', default=False)
    tuesday = fields.Boolean(string='T', default=False)
    wednesday = fields.Boolean(string='W', default=False)
    thursday = fields.Boolean(string='R', default=False)
    friday = fields.Boolean(string='F', default=False)
    days = fields.Char(compute='_timeslot')    
    timeslot = fields.Char('Timeslot', compute='_timeslot')

    @api.depends('start_timeslot', 'end_timeslot', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    @api.onchange('start_timeslot', 'end_timeslot', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday')
    def _timeslot(self):
        for rec in self:
            days = ''
            if rec.monday:
                days = 'M'
            if rec.tuesday:
                days += 'T'
            if rec.wednesday:
                days += 'W'
            if rec.thursday:
                days += 'R'
            if rec.friday:
                days += 'F'
            rec.days = days
            if days == '':
                rec.timeslot = ''
                continue
            
            if rec.start_timeslot and rec.end_timeslot and rec.end_timeslot > rec.start_timeslot:
                start_hours = int(rec.start_timeslot)
                start_minutes = int((rec.start_timeslot - start_hours) * 60)
                if start_hours < 10:
                    start_hours = '0' + str(start_hours)
                else:
                    start_hours = str(start_hours)                
                if start_minutes < 10:
                    start_minutes = '0' + str(start_minutes)
                start_time = start_hours + ':' + str(start_minutes)
                
                end_hours = int(rec.end_timeslot)
                end_minutes = int((rec.end_timeslot - end_hours) * 60)
                if end_hours < 10:
                    end_hours = '0' + str(end_hours)
                else:
                    end_hours = str(end_hours)                
                if end_minutes < 10:
                    end_minutes = '0' + str(end_minutes)
                else:
                    end_minutes = str(end_minutes)
                end_time = end_hours + ':' + end_minutes
                rec.timeslot = days + ' ' + start_time + ' - ' + end_time
            else:
                rec.timeslot = ''

    @api.constrains('start_timeslot', 'start_timeslot')
    def _constrains_start_timeslot(self):
        for rec in self:
            if rec.start_timeslot >= rec.end_timeslot or rec.start_timeslot < 8 or rec.start_timeslot >= 24 or rec.end_timeslot < 8 or rec.end_timeslot >= 24:
                raise UserError('Error in timeslot')