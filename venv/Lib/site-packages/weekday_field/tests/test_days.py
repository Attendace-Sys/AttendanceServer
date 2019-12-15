
import functools
import operator

from django.http.request import QueryDict
from django.forms import ValidationError
from django.test import TestCase

from weekday_field.fields import WeekdayField
from weekday_field.forms import WeekdayFormField, AdvancedWeekdayFormField, \
     BitwiseWeekdayFormField
from weekday_field.utils import DAY_CHOICES, BITWISE_DAY_CHOICES, \
     ADVANCED_DAY_CHOICES
from weekday_field.widgets import ToggleCheckboxes

class TestWeekdayField(TestCase):
    def test_field(self):
        f = WeekdayField()
        self.assertEqual([1, 2, 3, 4], f.to_python("1,2,3,4"))
        self.assertEqual([], f.to_python(""))
        self.assertIsInstance(f.formfield(), WeekdayFormField)
        self.assertEqual(True, f.validators[0]([1, 2, 3, 4]))
        self.assertEqual("1,2,3,4", f.get_db_prep_value([1, 2, 3, 4]))

class TestWeekdayFormField(TestCase):
    days = [i[0] for i in DAY_CHOICES]

    def test_field(self):
        f = WeekdayFormField()
        self.assertEqual(
            [str(i) for i in self.days],
            f.clean(self.days),
            )
        self.assertEqual(
            [str(i) for i in self.days],
            f.clean([str(i) for i in self.days]),
            )
        self.assertRaisesMessage(
            ValidationError,
            "'Select a valid choice. -1 is not one of the available choices.'",
            f.clean, [-1],
            )
        self.assertRaisesMessage(
            ValidationError,
            "'Select a valid choice. 7 is not one of the available choices.'",
            f.clean, [7],
            )

class TestWeekdayAdvancedFormField(TestCase):
    def test_field(self):
        f = AdvancedWeekdayFormField()
        choices = [
            ([0, 1, 2, 3, 4], "Weekdays"),
            ([5, 6], "Weekends"),
            ([], "Any day"),
            ]
        for expected, choice in choices:
            value = [i[0].split(",") for i in f.choices if i[1] == choice][0]
            self.assertEqual([str(i) for i in expected], f.clean(value))

class TestWeekdayBitwiseFormField(TestCase):
    def test_field(self):
        f = BitwiseWeekdayFormField(required=False)
        value = [i[0] for i in BITWISE_DAY_CHOICES]
        self.assertEqual(functools.reduce(operator.or_, value),
                         f.clean([str(i) for i in value]))
        self.assertEqual(0, f.clean([]))

    def test_short(self):
        f = BitwiseWeekdayFormField()
        short = [(x[0], x[1]) for x in BITWISE_DAY_CHOICES]
        not_short = [(x[0], x[2]) for x in BITWISE_DAY_CHOICES]
        self.assertEqual(f.choices, not_short)
        f = BitwiseWeekdayFormField(short=True)
        self.assertEqual(f.choices, short)
        f = BitwiseWeekdayFormField(short=False)
        self.assertEqual(f.choices, not_short)

class TestToggleCheckboxes(TestCase):
    def test_render_widget(self):
        f = ToggleCheckboxes(choices=DAY_CHOICES)
        self.assertHTMLEqual('''
        <ul>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="0" />
        Monday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="1" />
        Tuesday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="2" />
        Wednesday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="3" />
        Thursday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="4" />
        Friday</label></li>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="5" />
        Saturday</label></li>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="6" />
        Sunday</label></li>
        </ul>
        ''',
            f.render("Test Widget Name", list(range(5))),
            )
        self.maxDiff = None
        self.assertHTMLEqual('''
        <ul>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="0" />
        Monday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="1" />
        Tuesday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="2" />
        Wednesday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="3" />
        Thursday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="4" />
        Friday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="5" />
        Saturday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="6" />
        Sunday</label></li>
        </ul>
        ''',
            f.render("Test Widget Name", ""),
            )
        self.assertHTMLEqual('''
        <ul>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="0" />
        Monday</label></li>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="1" />
        Tuesday</label></li>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="2" />
        Wednesday</label></li>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="3" />
        Thursday</label></li>
        <li><label><input class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="4" />
        Friday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="5" />
        Saturday</label></li>
        <li><label><input checked="checked" class=" advanced-weekday-field"
        name="Test Widget Name" type="checkbox" value="6" />
        Sunday</label></li>
        </ul>
        ''',
            f.render("Test Widget Name", [5, 6]),
            )

    def test_value_from_datadict(self):
        f = ToggleCheckboxes(choices=ADVANCED_DAY_CHOICES)
        self.assertEqual(
            [],
            f.value_from_datadict(QueryDict(""), {}, "test"),
            )
        self.assertEqual(
            [''],
            f.value_from_datadict(QueryDict("test="), {}, "test"),
            )
        self.assertEqual(
            ["1", "2", "3"],
            f.value_from_datadict(QueryDict("test=1&test=2&test=3"), {}, "test"),
            )
        self.assertEqual(
            ["1", "2", "3"],
            f.value_from_datadict(QueryDict("test=1,2,3"), {}, "test"),
            )
