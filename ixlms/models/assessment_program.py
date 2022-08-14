from odoo import models, fields
import math


class AssessmentProgram(models.Model):
	_name = 'ixlms.assessment.program'
	_description = 'AssessmentProgram'
	_sql_constraints = [('assessment_program_ukey', 'unique(assessment_id, program_id)', 'Duplicate Assessment/Program lines')]

	assessment_id = fields.Many2one(comodel_name='ixlms.assessment', string='Assessment', required=True)
	program_id = fields.Many2one(comodel_name='ixcatalog.program', string='Program', required=True)
	max_grade = fields.Float(string='Max Grade', compute='_stats')
	min_grade = fields.Float(string='Min Grade', compute='_stats')
	avg_grade = fields.Float(string='Avg. Grade', compute='_stats')
	stdev = fields.Float(string='σ', compute='_stats')
	
	
	def _stats(self):
		for rec in self:
			min_grade, max_grade, s, s2, count = 100, 0, 0, 0, 0
			for assessment_line in rec.assessment_id.assessment_line_ids:
				if assessment_line.student_id.program_id != rec.program_id:
					continue
				
				if assessment_line.grade and assessment_line.grade != '':
					if assessment_line.egrade < min_grade:
						min_grade = assessment_line.egrade
					if assessment_line.egrade > max_grade:
						max_grade = assessment_line.egrade
					s += assessment_line.egrade
					s2 += assessment_line.egrade * assessment_line.egrade
					count += 1
			
			rec.max_grade = max_grade
			rec.min_grade = min_grade
			if count > 0:
				rec.avg_grade = s / count
				rec.stdev = math.sqrt(s2 / count - rec.avg_grade * rec.avg_grade)
			else:
				rec.avg_grade = 0
				rec.stdev = 0