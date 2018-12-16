from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField
from wtforms.validators import InputRequired


class BaseForm(FlaskForm):
    def get_error(self):
        form_error = ''
        if self.errors:
            form_error = self.errors.popitem()[1][0]
        return form_error


class UpdateStatusFrom(BaseForm):
    id = IntegerField(validators=[InputRequired(message='missed bha.id')])
    status = StringField(validators=[InputRequired(message='missed bha.status')])
