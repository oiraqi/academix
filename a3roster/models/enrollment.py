from odoo import models, fields, api
from odoo.exceptions import ValidationError

PASSING_GRADES = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']

class Enrollment(models.Model):
	_name = 'a3roster.enrollment'
	_inherit = 'mail.thread'
	_description = 'Enrollment'
	_sql_constraints = [('student_section_ukey', 'unique(student_id, section_id)', 'Student already enrolled in this section')]

	name = fields.Char('Name', compute='_set_name')
	student_id = fields.Many2one(comodel_name='a3.student', string='Student', required=True)
	section_id = fields.Many2one(comodel_name='a3roster.section', string='Section', required=True)
	state = fields.Selection(string='State', selection=[('created', 'Created'), ('enrolled', 'Enrolled'),
		('dropped', 'Dropped'), ('withdrawn', 'Withdrawn')], default='created', required=True, tracking=True)
	dstate = fields.Selection(string='Drop State', selection=[('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft')
	dtriggered = fields.Boolean(default=False)	
	wstate = fields.Selection(string='W State', selection=[('draft', 'Draft'), ('wreq', 'Request To Withdraw'), ('wadv', 'W Approved by Advisor'), ('winst', 'W Approved by Instructor')], default='draft', tracking=True)
	wtriggered = fields.Boolean(default=False)
	wfstate = fields.Selection(string='WF State', selection=[('draft', 'Draft'), ('wfreq', 'WF Request'), ('wfdean', 'WF Approved by the Dean/Director'), ('wfreg', 'WF Processed')],
		default='draft', tracking=True)
	wftriggered = fields.Boolean(default=False)
	wpstate = fields.Selection(string='WP State', selection=[('draft', 'Draft'), ('wpreq', 'WP Request'), ('wpdean', 'WP Approved by the Dean/Director'), ('wpreg', 'WP Processed')],
		default='draft', tracking=True)
	wptriggered = fields.Boolean(default=False)
	ipstate = fields.Selection(string='IP State', selection=[('draft', 'Draft'), ('ipreq', 'IP Request'), ('ipdean', 'IP Approved by the Dean/Director'), ('ipreg', 'IP Processed')],
		default='draft', tracking=True)
	iptriggered = fields.Boolean(default=False)
	wdtime = fields.Datetime()

	# Related fields
	school_id = fields.Many2one(comodel_name='a3.school', string='School', related='section_id.school_id', store=True)
	discipline_id = fields.Many2one(comodel_name='a3.discipline', string='Discipline', related='section_id.course_id.discipline_id', store=True)
	course_id = fields.Many2one(comodel_name='a3.course', string='Course', related='section_id.course_id', store=True)
	term_id = fields.Many2one(comodel_name='a3.term', string='Term', related='section_id.term_id', store=True)
	sid = fields.Char(related="student_id.sid")
	program_id = fields.Many2one(comodel_name='a3catalog.program', related='student_id.program_id', store=True)
	attendance_mode = fields.Selection(related='student_id.attendance_mode')
	email = fields.Char(related='student_id.email')	

	# Max protection for grade: group restriction (faculty, registrar) + accounting (tracking who did what, when)
	grade = fields.Char(string='Grade', groups='a3.group_faculty,a3roster.group_registrar', tracking=True)
	
	# Computed read-only grade and passed
	rgrade = fields.Char(string='Grade', compute='_grade', store=True)
	passed = fields.Boolean(string='Passed', compute='_grade', store=True)

	@api.depends('grade')
	def _grade(self):
		for rec in self:
			grade = rec.sudo().grade
			rec.rgrade = grade
			rec.passed = grade in PASSING_GRADES

	@api.constrains('student_id', 'section_id')
	def _check_student_section(self):
		for rec in self:
			if rec.state != 'created':
				raise ValidationError('Can\'t change a student/section mapping once enrolled!')
			
			if rec.student_id and rec.section_id:
				# From a performance perspective, we should start with the cheap is_open check,
				# then the time conflict check, and only then, the prerequisites check.
				# However, for a more pertinent feedback to the user, we deem it's worth it to start
				# with the more expensive prerequisites check.
				self.env['a3roster.enrollment'].check_prerequisites(rec.student_id, rec.section_id.course_id)				
				if not rec.section_id.is_open:
					raise ValidationError('Section closed!')
				self.env['a3roster.enrollment'].check_time_conflict(rec.student_id, rec.section_id)

	@api.model
	def check_prerequisites(self, student, course):
		for prerequisite in course.prerequisite_ids:
			alternatives = []
			for alternative in prerequisite.alternative_ids:
				alternatives.append(alternative.name)
				fulfilled = False
				if self.search([('student_id', '=', student.id), ('section_id.course_id', '=', alternative.id), ('passed', '=', True)]):
					fulfilled = True
					break
				if not fulfilled:
					if len(alternatives) > 1:
						raise ValidationError('None of these alternative prerequisites is fulfilled: ' + str(alternatives))
					else:
						raise ValidationError('Unfulfilled prerequisite: ' + alternatives[0])
				
	
	@api.model
	def check_time_conflict(self, student, section):
		current_sections = self.search([('student_id', '=', student.id), ('term_id', '=', section.term_id.id), ('state', '=', 'enrolled')])
		for sec in current_sections:
			if section.start_time <= sec.end_time and section.end_time >= sec.start_time:
				raise ValidationError('Time Conflict with ' + sec.name + ': ' + sec.timeslot)
	
	@api.onchange('student_id', 'section_id')
	def _set_name(self):
		for rec in self:
			if rec.student_id and rec.section_id:
				rec.name = rec.student_id.name + ' / ' + rec.section_id.name
			else:
				rec.name = ''

	def enroll(self):
		if self.state == 'created':
			self.state='enrolled'
	
	def drop(self):
		self.dtriggered = True

	def req_w(self):
		self.wtriggered = True
	
	def file_wp(self):
		self.wptriggered = True
	
	def file_wf(self):
		self.wftriggered = True

	def file_ip(self):
		self.iptriggered = True
	
	def confirm_drop(self):
		for rec in self:
			rec.state = 'dropped'
			rec.wdtime = fields.Datetime.now()		

	def cancel_drop(self):
		self.dtriggered = False
	
	def confirm_wrequest(self):
		return
	
	def cancel_wrequest(self):
		self.wtriggered = False
	
	def app_w_adv(self):
		return
	
	def app_w_ins(self):
		self.write({
			'state': 'withdrawn',
			'wdtime': fields.Datetime.now()
		})
	
	def confirm_wprequest(self):
		return
	
	def cancel_wprequest(self):
		self.wptriggered = False
	
	def app_wp_dean(self):
		return
	
	def app_wp_reg(self):
		return
	
	def confirm_wfrequest(self):
		return
	
	def cancel_wfrequest(self):
		self.wftriggered = False
	
	def app_wf_dean(self):
		return
	
	def app_wf_reg(self):
		return
	
	def confirm_iprequest(self):
		return
	
	def cancel_iprequest(self):
		self.iptriggered = False
	
	def app_ip_dean(self):
		return
	
	def app_ip_reg(self):
		return