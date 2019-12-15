from django.db import models

from weekday_field.forms import WeekdayFormField
from weekday_field import utils

def validate_csv(data):
    return all([isinstance(i, int) for i in data])

class WeekdayField(models.CommaSeparatedIntegerField):
    """
    Field to simplify the handling of a multiple choice of None->all days.

    Stores as CSInt.
    """
    __metaclass__ = models.SubfieldBase

    description = "CSV Weekday Field"
    default_validators = [validate_csv]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(WeekdayField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super(WeekdayField, self).formfield(form_class=WeekdayFormField, **kwargs)

    def to_python(self, value):
        if utils.is_str(value):
            if value:
                value = [int(x) for x in value.strip('[]').split(',') if x]
            else:
                value = []
        return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        return ",".join([str(x) for x in value or []])

try:
    from south.modelsinspector import add_introspection_rules
except ImportError:
    pass
else:
    add_introspection_rules([], ['^weekday_field\.fields\.WeekdayField'])
