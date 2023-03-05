from django.test import Client, TestCase
from django.urls import reverse
from records.models import Cycle
from records.forms import CycleForm
from django.utils import timezone


class RecordsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('records'))
        self.assertTemplateUsed(response, 'records/records.html')

    def test_view_returns_correct_data(self):
        Cycle.objects.create(name='Cycle 1', genetics='Unknown', seedbank='Unknown')
        Cycle.objects.create(name='Cycle 2', genetics='Unknown', seedbank='Unknown')

        response = self.client.get(reverse('records'))
        self.assertEqual(len(response.context['cycles']), 2)

    def test_view_returns_error_when_no_records(self):
        response = self.client.get(reverse('records'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['cycles']), 0)
        self.assertContains(response, 'No records found')


class RecordViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cycle = Cycle.objects.create(name='Cycle 1', genetics='Unknown', seedbank='Unknown')

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('record', args=(self.cycle.pk,)))
        self.assertTemplateUsed(response, 'records/record.html')

    def test_view_returns_correct_data(self):
        response = self.client.get(reverse('record', args=(self.cycle.pk,)))
        self.assertEqual(response.context['cycle'], self.cycle)

    def test_view_returns_404_when_record_not_found(self):
        response = self.client.get(reverse('record', args=(100,)))
        self.assertEqual(response.status_code, 404)


class CreateOrEditRecordViewTestCase(TestCase):
    def setUp(self):
        self.cycle = Cycle.objects.create(genetics='Example Genetics', fixture='Example Fixture')
        self.url = reverse('create_record')

    def test_create_record_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/new_record.html')
        self.assertIsInstance(response.context['form'], CycleForm)
        self.assertIsNone(response.context['cycle'])

    def test_create_record_post(self):
        data = {
            'genetics': 'Updated Genetics',
            'fixture': 'Updated Fixture',
            'behavioral_response': 'auto-flowering',
            'seed_type': 'feminized',
            'grow_medium': 'soil',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        cycle = Cycle.objects.last()
        self.assertEqual(cycle.genetics, 'Updated Genetics')
        self.assertEqual(cycle.fixture, 'Updated Fixture')
        self.assertEqual(cycle.behavioral_response, 'auto-flowering')
        self.assertEqual(cycle.seed_type, 'feminized')
        self.assertEqual(cycle.grow_medium, 'soil')

    def test_create_record_post_invalid_data(self):
        # Test invalid data in form submission
        data = {
            'genetics': '',  # empty value
            'fixture': 'Updated Fixture',
            'behavioral_response': 'auto-flowering',
            'seed_type': 'feminized',
            'grow_medium': 'soil',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/new_record.html')
        self.assertIsInstance(response.context['form'], CycleForm)
        self.assertIsNone(response.context['cycle'])
        self.assertEqual(Cycle.objects.count(), 1)

    def test_create_record_post_missing_required_fields(self):
        # Test missing required fields in form submission
        data = {
            'genetics': 'Updated Genetics',
            'fixture': '',  # missing value
            'behavioral_response': 'auto-flowering',
            'seed_type': 'feminized',
            'grow_medium': 'soil',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/new_record.html')
        self.assertIsInstance(response.context['form'], CycleForm)
        self.assertIsNone(response.context['cycle'])
        self.assertEqual(Cycle.objects.count(), 1)

class DeleteRecordViewTestCase(TestCase):

    def setUp(self):
        self.cycle = Cycle.objects.create(
            date=timezone.now().date(),
            genetics='Test Genetics',
            fixture='Test Fixture'
        )
        self.url = reverse('delete_record', args=[self.cycle.pk])

    def test_delete_record(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Cycle.objects.filter(pk=self.cycle.pk).exists())
