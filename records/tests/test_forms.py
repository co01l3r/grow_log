from django.test import TestCase
from decimal import Decimal

from records.models import Cycle, Log, Nutrient, NutrientLog, ReservoirLog
from records.forms import CycleForm, LogForm, NutrientLogForm, ReservoirLogForm


# cycleForm test case
class CycleFormTest(TestCase):
    def setUp(self):
        self.cycle_data = {
            'name': 'Test Cycle',
            'genetics': 'Test Genetics',
            'seedbank': 'Test Seedbank',
            'fixture': 'Test Fixture',
            'behavioral_response': 'photoperiodic',
            'seed_type': 'feminized',
            'grow_medium': 'Test Medium'
        }

    def test_valid_form(self):
        form = CycleForm(data=self.cycle_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        # Testing with missing required fields
        form = CycleForm(data={
            'name': 'Test Cycle',
            'genetics': '',
            'seedbank': 'Test Seedbank',
            'fixture': 'Test Fixture',
            'behavioral_response': 'Test Response',
            'seed_type': '',
            'grow_medium': 'Test Medium'
        })
        self.assertFalse(form.is_valid())

    def test_form_widget_classes(self):
        form = CycleForm()
        self.assertIn('form-control', str(form.fields['behavioral_response'].widget.attrs))
        self.assertIn('form-control', str(form.fields['seed_type'].widget.attrs))
        self.assertIn('form-control', str(form.fields['grow_medium'].widget.attrs))


# logForm test case
class LogFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'phase': 'vegetative',
            'temperature_day': 25.5,
            'temperature_night': 20.0,
            'humidity_day': 60,
            'humidity_night': 70,
            'ph': 6.2,
            'ec': 1.8,
            'irrigation': '2x drip',
            'light_height': 50,
            'light_power': '75',
            'calibration': True,
        }
        form = LogForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors.as_json())
        log = form.save(commit=False)
        self.assertIsInstance(log, Log)
        self.assertEqual(log.phase, 'vegetative')
        self.assertEqual(log.temperature_day, Decimal('25.5'))
        self.assertEqual(log.temperature_night, Decimal('20.0'))
        self.assertEqual(log.humidity_day, 60)
        self.assertEqual(log.humidity_night, 70)
        self.assertEqual(log.ph, Decimal('6.2'))
        self.assertEqual(log.ec, Decimal('1.8'))
        self.assertEqual(log.irrigation, '2x drip')
        self.assertEqual(log.light_height, 50)
        self.assertEqual(str(log.light_power), '75')
        self.assertEqual(log.calibration, True)
