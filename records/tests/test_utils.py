from django.test import TestCase
from records.models import Cycle, Log
from records.utils import calculate_average_veg_day_temp


class CalculateAverageVegDayTempTestCase(TestCase):
    def setUp(self):
        self.cycle = Cycle.objects.create(name='Test Cycle')
        self.log1 = Log.objects.create(cycle=self.cycle, phase='vegetative', temperature_day=20, temperature_night=15)
        self.log2 = Log.objects.create(cycle=self.cycle, phase='vegetative', temperature_day=None,
                                       temperature_night=None)
        self.log3 = Log.objects.create(cycle=self.cycle, phase='bloom', temperature_day=25, temperature_night=20)

    def test_calculate_average_veg_temp_with_logs(self):
        avg_day_temp = calculate_average_veg_day_temp(self.cycle)
        self.assertEqual(avg_day_temp, 20)

    def test_calculate_average_veg_temp_without_logs(self):
        cycle2 = Cycle.objects.create(name='Test Cycle 2')
        avg_day_temp = calculate_average_veg_day_temp(cycle2)
        self.assertIsNone(avg_day_temp)
