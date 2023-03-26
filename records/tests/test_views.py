from django.test import Client, TestCase
from django.urls import reverse
from records.models import Cycle, Log
from records.forms import CycleForm
from django.core.files.uploadedfile import SimpleUploadedFile


# record views test cases
class RecordsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cycle = Cycle.objects.create(
            name='Cycle 1', genetics='Updated Genetics', seedbank='Unknown',
            fixture='Fixture 1', behavioral_response='auto-flowering',
            seed_type='feminized', grow_medium='soil',
        )
        self.url_records = reverse('records')
        self.url_record = reverse('record', args=[self.cycle.pk])
        self.url_create_record = reverse('create_record')
        self.url_edit_record = reverse('edit_record', args=[self.cycle.pk])
        self.url_delete_record = reverse('delete_record', args=[self.cycle.pk])

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url_records)
        self.assertTemplateUsed(response, 'records/records.html')

        response = self.client.get(self.url_record)
        self.assertTemplateUsed(response, 'records/record.html')

        response = self.client.get(self.url_create_record)
        self.assertTemplateUsed(response, 'records/record_form.html')
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
class CreateLogTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.cycle = Cycle.objects.create(
            genetics="Test Genetics",
            fixture="Test Fixture",
            grow_medium="Test Medium"
        )
        self.url = reverse('create_log', kwargs={'pk': self.cycle.pk})

    def test_create_log_with_valid_data(self):
        data = {
            'phase': 'seedling',
            'temperature_day': 24.0,
            'temperature_night': 20.0,
            'humidity_day': 60,
            'humidity_night': 50,
            'ph': 6.0,
            'ec': 2.0,
            'irrigation': 'test',
            'light_height': 50,
            'light_power': 50,
            'calibration': False,
            'water': '',
            'comment': 'test comment',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('record', kwargs={'pk': self.cycle.pk}))
        self.assertEqual(Log.objects.count(), 1)
        log = Log.objects.first()
        self.assertEqual(log.phase, 'seedling')
        self.assertEqual(log.temperature_day, 24.0)
        self.assertEqual(log.temperature_night, 20.0)
        self.assertEqual(log.humidity_day, 60)
        self.assertEqual(log.humidity_night, 50)
        self.assertEqual(log.ph, 6.0)
        self.assertEqual(log.ec, 2.0)
        self.assertEqual(log.irrigation, 'test')
        self.assertEqual(log.light_height, 50)
        self.assertEqual(log.light_power, 50)
        self.assertFalse(log.calibration)
        self.assertIsNone(log.water)
        self.assertEqual(log.comment, 'test comment')

    def test_create_log_with_invalid_data(self):
        data = {
            'phase': 'invalid_phase',
            'temperature_day': 'invalid_temperature',
            'temperature_night': 'invalid_temperature',
            'humidity_day': 'invalid_humidity',
            'humidity_night': 'invalid_humidity',
            'ph': 'invalid_ph',
            'ec': 'invalid_ec',
            'irrigation': 'test',
            'light_height': 'invalid_light_height',
            'light_power': 'invalid_light_power',
            'calibration': False,
            'water': '',
            'comment': 'test comment',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)

    def test_create_log_with_missing_required_fields(self):
        data = {
            'phase': '',
            'temperature_day': '',
            'temperature_night': '',
            'humidity_day': '',
            'humidity_night': '',
            'ph': '',
            'ec': '',
            'irrigation': '',
            'light_height': '',
            'light_power': '',
            'calibration': False,
            'water': '',
            'comment': '',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Log.objects.count(), 0)

    def test_create_log_with_missing_optional_fields(self):
        data = {
            'phase': 'vegetative',
            'temperature_day': 25.0,
            'temperature_night': 20.0,
            'humidity_day': 60,
            'humidity_night': 50,
            'ph': 6.0,
            'ec': 2.0,
            'irrigation': '',
            'light_height': '',
            'light_power': '',
            'calibration': False,
            'water': '',
            'comment': '',
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('record', kwargs={'pk': self.cycle.pk}))
        self.assertEqual(Log.objects.count(), 1)
        log = Log.objects.first()
        self.assertEqual(log.phase, 'vegetative')
        self.assertEqual(log.temperature_day, 25.0)
        self.assertEqual(log.temperature_night, 20.0)
        self.assertEqual(log.humidity_day, 60)
        self.assertEqual(log.humidity_night, 50)
        self.assertEqual(log.ph, 6.0)
        self.assertEqual(log.ec, 2.0)
        self.assertIsNone(log.light_height)
        self.assertIsNone(log.light_power)
        self.assertFalse(log.calibration)
        self.assertIsNone(log.water)
        self.assertEqual(log.comment, '')


class EditLogViewTestCase(TestCase):
    def setUp(self):
        self.cycle = Cycle.objects.create(
            genetics='Test Genetics',
            fixture='Test Fixture',
        )
        self.log = Log.objects.create(
            cycle=self.cycle,
            phase='vegetative',
            temperature_day=25,
            temperature_night=20,
            humidity_day=60,
            humidity_night=50,
            ph=6.0,
            ec=1.0,
            irrigation='Test Irrigation',
            light_height=30,
            light_power=100,
            calibration=True,
            water=500,
            comment='Test Comment',
        )
        self.url = reverse('edit_log', args=[self.cycle.pk, self.log.pk])
        self.data = {
            'phase': 'bloom',
            'temperature_day': 27,
            'temperature_night': 22,
            'humidity_day': 50,
            'humidity_night': 45,
            'ph': 6.5,
            'ec': 1.5,
            'irrigation': 'New Irrigation',
            'light_height': 40,
            'light_power': 75,
            'calibration': False,
            'water': 700,
            'comment': 'New Comment',
        }

    def test_edit_log_view_with_valid_data(self):
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('record', args=[self.cycle.pk]))
        self.log.refresh_from_db()
        self.assertEqual(self.log.phase, 'bloom')
        self.assertEqual(self.log.temperature_day, 27)
        self.assertEqual(self.log.temperature_night, 22)
        self.assertEqual(self.log.humidity_day, 50)
        self.assertEqual(self.log.humidity_night, 45)
        self.assertEqual(self.log.ph, 6.5)
        self.assertEqual(self.log.ec, 1.5)
        self.assertEqual(self.log.irrigation, 'New Irrigation')
        self.assertEqual(self.log.light_height, 40)
        self.assertEqual(self.log.light_power, 75)
        self.assertFalse(self.log.calibration)
        self.assertEqual(self.log.water, 700)
        self.assertEqual(self.log.comment, 'New Comment')

    def test_edit_log_view_with_invalid_data(self):
        self.data['phase'] = ''
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/log_form.html')
        self.log.refresh_from_db()
        self.assertEqual(self.log.phase, 'vegetative')
        self.assertEqual(self.log.temperature_day, 25)
        self.assertEqual(self.log.temperature_night, 20)
        self.assertEqual(self.log.humidity_day, 60)
        self.assertEqual(self.log.humidity_night, 50)
        self.assertEqual(self.log.ph, 6.0)
        self.assertEqual(self.log.ec, 1.0)
        self.assertEqual(self.log.irrigation, 'Test Irrigation')
        self.assertEqual(self.log.light_height, 30)
        self.assertEqual(self.log.light_power, 100)
        self.assertTrue(self.log.calibration)
        self.assertEqual(self.log.water, 500)
        self.assertEqual(self.log.comment, 'Test Comment')


class DeleteLogTestCase(TestCase):
    def setUp(self):
        self.cycle = Cycle.objects.create(genetics='Sour Diesel', fixture='LED')
        self.log = Log.objects.create(cycle=self.cycle, phase='day 1', temperature_day=24.0, temperature_night=20.0,
                                      humidity_day=70, humidity_night=60, ph=6.0, ec=1.2, irrigation='drip',
                                      light_height=50, light_power=100, calibration=True, water=200,
                                      comment='This is a test log')

    def test_delete_log(self):
        self.assertTrue(Log.objects.filter(pk=self.log.pk).exists())
        response = self.client.get(reverse('delete_log', args=[self.cycle.pk, self.log.pk]))
        self.assertFalse(Log.objects.filter(pk=self.log.pk).exists())
        self.assertRedirects(response, reverse('record', args=[self.cycle.pk]))

# nutrient views test cases
# nutrientLog views test cases
# other views test cases
