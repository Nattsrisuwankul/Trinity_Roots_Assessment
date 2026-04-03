from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TodoTag(models.Model):
    _name = "todo.tag"
    _description = "Todo Tag"

    name = fields.Char(required=True)


class TodoList(models.Model):
    _name = "todo.list"
    _description = "Todo List"
    _order = "start_date desc, id desc"

    name = fields.Char(required=True)
    tag_ids = fields.Many2many("todo.tag", string="Tags")
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("in_progress", "In Progress"),
            ("complete", "Complete"),
        ],
        default="draft",
        required=True,
    )
    line_ids = fields.One2many("todo.list.line", "todo_id", string="Todo Items")
    attendee_ids = fields.One2many("todo.list.attendee", "todo_id", string="Attendees")
    all_lines_done = fields.Boolean(compute="_compute_all_lines_done")

    @api.depends("line_ids.is_done", "line_ids")
    def _compute_all_lines_done(self):
        for record in self:
            record.all_lines_done = bool(record.line_ids) and all(record.line_ids.mapped("is_done"))

    @api.constrains("start_date", "end_date")
    def _check_date_range(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date <= record.start_date:
                raise ValidationError(_("End Date must be greater than Start Date."))

    def action_start_progress(self):
        for record in self.filtered(lambda rec: rec.state == "draft"):
            record.state = "in_progress"

    def action_mark_complete(self):
        for record in self:
            if not record.all_lines_done:
                raise ValidationError(_("All todo items must be completed before marking the todo list as complete."))
            record.state = "complete"


class TodoLine(models.Model):
    _name = "todo.list.line"
    _description = "Todo Item"

    todo_id = fields.Many2one("todo.list", required=True, ondelete="cascade")
    name = fields.Char(required=True)
    description = fields.Text()
    is_done = fields.Boolean(string="Done")


class TodoAttendee(models.Model):
    _name = "todo.list.attendee"
    _description = "Todo Attendee"
    _sql_constraints = [
        ("todo_list_attendee_unique_user", "unique(todo_id, user_id)", "This attendee is already added to the todo list."),
    ]

    todo_id = fields.Many2one("todo.list", required=True, ondelete="cascade")
    user_id = fields.Many2one("res.users", string="Attendee", required=True)
