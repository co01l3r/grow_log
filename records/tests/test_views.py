from django.test import Client, TestCase
from django.urls import reverse
from records.models import Cycle


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