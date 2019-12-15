from django.forms.widgets import CheckboxSelectMultiple
from django.utils.safestring import mark_safe

from weekday_field import utils

class ToggleCheckboxes(CheckboxSelectMultiple):
    class Media:
        js = (
            'weekday_field/js/checkbox-widget.js',
        )

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        if utils.is_str(value):
            value = [int(i) for i in value.split(',') if i]
        if not value or value == range(7):
            value = [str(x[0]) for x in self.choices]
        if all([x in value for x in range(5)]):
            value.append('0,1,2,3,4')
        if 5 in value and 6 in value:
            value.append('5,6')
        if 'class' not in attrs:
            attrs['class'] = ""
        attrs['class'] += " advanced-weekday-field"
        result = super(ToggleCheckboxes, self).render(name, value, attrs)
        result = result.replace(
            " Weekends</label></li>",
            " Weekends</label></li></ul><ul>")
        return mark_safe(result)

    def value_from_datadict(self, data, files, name):
        value = super(ToggleCheckboxes, self).value_from_datadict(data, files, name)
        return sorted(set([x for sub in value for x in sub.split(',')]))
