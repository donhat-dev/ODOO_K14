from odoo import models, fields, api

from odoo.exceptions import ValidationError

class TrainingCourse(models.Model):
    _name = 'training.course'
    _description = 'Training Course'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_active(self):
        return True

    name = fields.Char(string="Course Name", required=True, tracking=True)
    code = fields.Char(string="Course Code", required=True)
    description = fields.Text(string="Description", tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date")
    active = fields.Boolean(string="Active", default=_default_active)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('published', 'Published'),
         ('archived', 'Archived')],
        string="Status",
        default='draft',
        tracking=True
    )

    tutor_id = fields.Many2one(
        comodel_name='res.partner',
        string="Tutor",
        ondelete="set null",
        tracking=True
    )

    course_session_ids = fields.One2many(
        'training.course.session',
        inverse_name='course_id',
        string="Course Sessions",
        tracking=True
    )

    level_ids = fields.Many2many(
        'training.course.level',
        'training_course_level_rel',
        'course_id',
        'level_id',
        string="Course Levels",
        tracking=True
    )

    level_ids_2 = fields.Many2many(
        comodel_name='training.course.level',
        relation='training_course_level_rel_2',
        column1='course_id',
        column2='level_id',
        string="Course Levels 2"
    )

    level_ids_3 = fields.Many2many(
        'training.course.level',
        'training_course_level_rel_3',
        'course_id',
        'level_id',
        string="Course Levels 3"
    )

    def button_publish(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Only draft courses can be published.")

            record.state = 'published'
    
    def button_archive(self):
        for record in self:
            if record.state != 'published':
                raise ValidationError("Only published courses can be archived.")

            record.state = 'archived'
    
    def button_set_draft(self):
        for record in self:
            record.state = 'draft'


class TrainingCourseSession(models.Model):
    _name = 'training.course.session'
    _description = 'Training Course Session'

    course_id = fields.Many2one(comodel_name='training.course', string="Course", required=True, ondelete="cascade")
    session_date = fields.Date(string="Session Date", required=True)
    instructor = fields.Char(string="Instructor")

class TrainingCourseLevel(models.Model):
    _name = 'training.course.level'
    _description = 'Training Course Level'

    name = fields.Char(string="Level Name", required=True)
