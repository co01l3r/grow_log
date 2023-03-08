from django.test import Client, TestCase
from django.urls import reverse
from records.models import Cycle
from records.forms import CycleForm
from django.utils import timezone


# record views test cases
class RecordsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cycle = Cycle.objects.create(
            name='Cycle 1', genetics='Unknown', seedbank='Unknown',
            fixture='Fixture 1', behavioral_response='auto-flowering',
            seed_type='feminized', grow_medium='soil',
        )
        self.url_records = reverse('records')
        self.url_record = reverse('record', args=[self.cycle.pk])
        self.url_create_record = reverse('create_record')
        self.url_edit_record = reverse('edit_record', args=[self.cycle.pk])
        self.url_delete_record = reverse('delete_record', args=[self.cycle.pk])

    def test_view_uses_correct_template(self):
        # Test records view
        response = self.client.get(self.url_records)
        self.assertTemplateUsed(response, 'records/records.html')

        # Test record view
        response = self.client.get(self.url_record)
        self.assertTemplateUsed(response, 'records/record.html')

        # Test create or edit record view
        response = self.client.get(self.url_create_record)
        self.assertTemplateUsed(response, 'records/new_record.html')
        self.assertIsInstance(response.context['form'], CycleForm)
        self.assertIsNone(response.context['cycle'])

    def test_view_returns_correct_data(self):
        Cycle.objects.create(
            name='Cycle 2', genetics='Unknown', seedbank='Unknown',
            fixture='Fixture 2', behavioral_response='photoperiodic',
            seed_type='regular', grow_medium='hydroponics',
        )
        response = self.client.get(self.url_records)
        self.assertEqual(len(response.context['cycles']), 2)

        response = self.client.get(self.url_record)
        self.assertEqual(response.context['cycle'], self.cycle)

    def test_view_returns_error_when_no_records(self):
        Cycle.objects.all().delete()
        response = self.client.get(self.url_records)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cycles']), 0)
        self.assertContains(response, 'No records found')

    def test_create_record_get(self):
        response = self.client.get(self.url_create_record)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CycleForm)
        self.assertIsNone(response.context['cycle'])

    def test_create_record_post(self):
        data = {
            'genetics': 'Updated Genetics',
            'seedbank': 'Updated Seedbank',
            'fixture': 'Updated Fixture',
            'behavioral_response': 'photoperiodic',
            'seed_type': 'clones',
            'grow_medium': 'hydroponics',
            'name': 'Updated Name',
            'beginning_phase': 'seedling',
        }
        response = self.client.post(self.url_create_record, data)
        self.assertEqual(response.status_code, 302)
        cycle = Cycle.objects.last()
        self.assertEqual(cycle.genetics, 'Updated Genetics')
        self.assertEqual(cycle.seedbank, 'Updated Seedbank')
        self.assertEqual(cycle.fixture, 'Updated Fixture')
        self.assertEqual(cycle.behavioral_response, 'photoperiodic')
        self.assertEqual(cycle.seed_type, 'clones')
        self.assertEqual(cycle.grow_medium, 'hydroponics')
        self.assertEqual(cycle.name, 'Updated Name')
        self.assertEqual(cycle.beginning_phase, 'seedling')

    def test_edit_record_get(self):
        response = self.client.get(self.url_edit_record)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CycleForm)
        self.assertEqual(response.context['cycle'], self.cycle)

    def test_edit_record_post(self):
        data = {
            'genetics': 'Updated Genetics',
            'seedbank': 'Updated Seedbank',
            'fixture': 'Updated Fixture',
            'behavioral_response': 'photoperiodic',
            'seed_type': 'clones',
            'grow_medium': 'hydroponics',
            'name': 'Updated Name',
            'beginning_phase': 'seedling',
        }
        response = self.client.post(self.url_edit_record, data)
        self.assertEqual(response.status_code, 302)
        cycle = Cycle.objects.get(pk=self.cycle.pk)
        self.assertEqual(cycle.genetics, 'Updated Genetics')
        self.assertEqual(cycle.seedbank, 'Updated Seedbank')
        self.assertEqual(cycle.fixture, 'Updated Fixture')
        self.assertEqual(cycle.behavioral_response, 'photoperiodic')
        self.assertEqual(cycle.seed_type, 'clones')
        self.assertEqual(cycle.grow_medium, 'hydroponics')
        self.assertEqual(cycle.name, 'Updated Name')
        self.assertEqual(cycle.beginning_phase, 'seedling')

    def test_delete_record_get(self):
        response = self.client.post(self.url_delete_record)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('records'))

    def test_delete_record_post(self):
        response = self.client.post(self.url_delete_record)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(Cycle.DoesNotExist):
            Cycle.objects.get(pk=self.cycle.pk)



# log views test cases
# nutrient views test cases
# nutrientLog views test cases
# other views test cases
