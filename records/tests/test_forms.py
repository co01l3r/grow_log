from django.test import TestCase

from records.models import Cycle, Log, Nutrient, NutrientLog, ReservoirLog
from records.forms import CycleForm, NutrientLogForm, ReservoirLogForm


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
