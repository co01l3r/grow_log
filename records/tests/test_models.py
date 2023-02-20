from django.test import TestCase
from records.models import Cycle, Log, Nutrient, NutrientLog
from django.core.exceptions import ValidationError


class CycleModelTestCase(TestCase):
    def setUp(self):
        Cycle.objects.create(
            name="Cycle 1 - Q1",
            genetics="Sativa",
            seedbank="Seed Co.",
            fixture="Indoor grow tent",
        )

    def test_cycle_created(self):
        cycle1 = Cycle.objects.get(name="Cycle 1 - Q1")
        self.assertEqual(cycle1.genetics, "Sativa")
        self.assertEqual(cycle1.fixture, "Indoor grow tent")

    def test_str_representation_with_name(self):
        cycle1 = Cycle.objects.get(name="Cycle 1 - Q1")
        self.assertEqual(str(cycle1), "Cycle 1 - Q1/2023")

    def test_str_representation_without_name(self):
        cycle2 = Cycle.objects.create(genetics="Indica")
        self.assertEqual(str(cycle2), "Indica - Q1/2023")

    def test_date_auto_now_add(self):
        cycle1 = Cycle.objects.get(name="Cycle 1 - Q1")
        self.assertIsNotNone(cycle1.date)

    def test_name_field_max_length(self):
        max_length = Cycle._meta.get_field('name').max_length
        cycle = Cycle(name='a' * (max_length + 1))
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn('Ensure this value has at most', str(context.exception))

    def test_genetics_field_max_length(self):
        cycle = Cycle(name="Cycle 1 - Q1", genetics="a" * 201)
        with self.assertRaises(Exception) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 200 characters", str(context.exception))

    def test_seedbank_field_max_length(self):
        cycle = Cycle(name="Cycle 1 - Q1", seedbank="a" * 81)
        with self.assertRaises(Exception) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 80 characters", str(context.exception))

    def test_fixture_field_max_length(self):
        cycle = Cycle(name="Cycle 1 - Q1", fixture="a" * 201)
        with self.assertRaises(Exception) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 200 characters", str(context.exception))


class LogModelTestCase(TestCase):
    def setUp(self):
        self.cycle = Cycle.objects.create(
            name="Cycle 1",
            genetics="Test Genetics",
            seedbank="Test Seedbank",
            fixture="Test Fixture"
        )
        self.log = Log.objects.create(
            cycle=self.cycle,
            phase="vegetative",
            temperature_day=25.0,
            temperature_night=20.0,
            humidity_day=50,
            humidity_night=60,
            ph=5.5,
            ec=1.0,
            irrigation="Test Irrigation",
            light_height=100,
            light_power=25,
            calibration=True
        )

    def test_log_str_representation(self):
        log_str = str(self.log)
        self.assertEqual(log_str, "1")

    def test_log_is_associated_with_cycle(self):
        self.assertEqual(self.log.cycle, self.cycle)

    def test_log_has_correct_phase(self):
        self.assertEqual(self.log.phase, "vegetative")

    def test_log_has_correct_temperatures(self):
        self.assertEqual(self.log.temperature_day, 25.0)
        self.assertEqual(self.log.temperature_night, 20.0)

    def test_log_has_correct_humidity(self):
        self.assertEqual(self.log.humidity_day, 50)
        self.assertEqual(self.log.humidity_night, 60)

    def test_log_has_correct_ph_and_ec(self):
        self.assertEqual(self.log.ph, 5.5)
        self.assertEqual(self.log.ec, 1.0)

    def test_log_has_correct_irrigation(self):
        self.assertEqual(self.log.irrigation, "Test Irrigation")

    def test_log_has_correct_light_height_and_power(self):
        self.assertEqual(self.log.light_height, 100)
        self.assertEqual(self.log.light_power, 25)


class NutrientTestCase(TestCase):
    def setUp(self):
        self.nutrient = Nutrient.objects.create(
            name='NPK Fertilizer',
            brand='Brand X',
            detail='High-quality NPK fertilizer for all plants'
        )

    def test_nutrient_creation(self):
        nutrient = Nutrient.objects.get(name='NPK Fertilizer')
        self.assertEqual(nutrient.brand, 'Brand X')
        self.assertEqual(nutrient.detail, 'High-quality NPK fertilizer for all plants')

    def test_nutrient_string_representation(self):
        self.assertEqual(str(self.nutrient), 'NPK Fertilizer')


class NutrientLogTestCase(TestCase):
    def setUp(self):
        cycle = Cycle.objects.create(name="Test Cycle")
        log = Log.objects.create(cycle=cycle, phase="vegetative")
        nutrient = Nutrient.objects.create(name="Test Nutrient", brand="Test Brand")
        self.nutrient_log = NutrientLog.objects.create(log=log, nutrient=nutrient, concentration=100)

    def test_nutrient_log_str(self):
        self.assertEqual(str(self.nutrient_log), "Test Nutrient - 100")

    def test_nutrient_log_concentration(self):
        self.assertEqual(self.nutrient_log.concentration, 100)
