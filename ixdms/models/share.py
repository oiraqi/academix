from odoo import models, fields


class Share(models.Model):
	_inherit = 'ixdms.node'
	_description = 'Share'


	student_share_ids = fields.One2many(
        comodel_name='ixdms.student.share', inverse_name='share_id', string='Student Shares')
	faculty_share_ids = fields.One2many(
        comodel_name='ixdms.faculty.share', inverse_name='share_id', string='Faculty Shares')

	implied_student_share_ids = fields.Many2many(
        comodel_name='ixdms.student.share', compute='_implied_share', string='Implied Student Shares')
	implied_faculty_share_ids = fields.Many2many(
        comodel_name='ixdms.faculty.share', compute='_implied_share', string='Implied Faculty Shares')

	implied_student_user_ids = fields.Many2many(
        comodel_name='res.users', compute='_implied_share', string='Implied Student Users')
	implied_faculty_user_ids = fields.Many2many(
        comodel_name='res.users', compute='_implied_share', string='Implied Faculty Users')

	student_user_ids = fields.One2many(
        comodel_name='res.users', compute='_student_user_ids')
	faculty_user_ids = fields.One2many(
        comodel_name='res.users', compute='_faculty_user_ids')

	def _student_user_ids(self):
		for rec in self:
			users = []
			for share in rec.student_share_ids:
				if not share.program_id:
					students = self.env['ix.student'].search(
                        [('school_id', '=', share.school_id.id)])
				else:
					students = self.env['ix.student'].search(
                        [('program_id', '=', share.program_id.id)])

				for student in students:
					if student.user_id.id not in users:
						users.append(student.user_id.id)
			if len(users) > 0:
				rec.student_user_ids = users
			else:
				rec.student_user_ids = False

	def _faculty_user_ids(self):
		for rec in self:
			users = []
			for share in rec.faculty_share_ids:
				if not share.discipline_id:
					faculties = self.env['ix.faculty'].search(
                        [('school_id', '=', share.school_id.id)])
				else:
					faculties = self.env['ix.faculty'].search(
                        [('discipline_ids', 'in', share.discipline_id.id)])

				for faculty in faculties:
					if faculty.user_id.id not in users:
						users.append(faculty.user_id.id)
			if len(users) > 0:
				rec.faculty_user_ids = users
			else:
				rec.faculty_user_ids = False

	def _implied_share(self):
		for rec in self:            
			implied_student_share_ids = []
			implied_faculty_share_ids = []
			implied_student_user_ids = []
			implied_faculty_user_ids = []

			rec._rec_implied_share(implied_student_share_ids, implied_faculty_share_ids)

			if len(implied_student_share_ids) > 0:
				rec.implied_student_share_ids = implied_student_share_ids
				for share in rec.implied_student_share_ids:
					if not share.program_id:
						students = self.env['ix.student'].search(
                            [('school_id', '=', share.school_id.id)])
					else:
						students = self.en['ix.student'].search(
                            [('program_id', '=', share.program_id.id)])
					for student in students:
						implied_student_user_ids.append(student.user_id.id)
				if len(implied_student_user_ids) > 0:
					rec.implied_student_user_ids = implied_student_user_ids
				else:
					rec.implied_student_user_ids = False
			else:
				rec.implied_student_share_ids = False
				rec.implied_student_user_ids = False

			if len(implied_faculty_share_ids) > 0:
				rec.implied_faculty_share_ids = implied_faculty_share_ids
				for share in rec.implied_faculty_share_ids:
					if not share.discipline_id:
						faculties = self.env['ix.faculty'].search(
                            [('school_id', '=', share.school_id.id)])
					else:
						faculties = self.en['ix.faculty'].search(
                            [('discipline_ids', 'in', share.discipline_id.id)])
					for faculty in faculties:
						implied_faculty_user_ids.append(faculty.user_id.id)
				if len(implied_faculty_user_ids) > 0:
					rec.implied_faculty_user_ids = implied_faculty_user_ids
				else:
					rec.implied_faculty_user_ids = False
			else:
				rec.implied_faculty_share_ids = False
				rec.implied_faculty_user_ids = False


	def _rec_implied_share(self, implied_student_share_ids, implied_faculty_share_ids):
		sself = self.sudo()
		if not sself.parent_id:
			return

		for student_share in sself.parent_id.student_share_ids:
			if student_share.id not in implied_student_share_ids:
				implied_student_share_ids.append(student_share.id)

		for faculty_share in sself.parent_id.faculty_share_ids:
			if faculty_share.id not in implied_faculty_share_ids:
				implied_faculty_share_ids.append(faculty_share.id)

		return sself.parent_id._rec_implied_share(implied_student_share_ids, implied_faculty_share_ids)
