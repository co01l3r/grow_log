from django.core.exceptions import ValidationError
from django.test import TestCase

from records.models import Cycle, Log, Nutrient, NutrientLog


# Cycle model test cases
class CycleModelTestCase(TestCase):
    def setUp(self):
        Cycle.objects.create(
            name="Cycle 1 - Q1",
            genetics="Sativa",
            seedbank="Seed Co.",
            fixture="led",
        )

    def test_cycle_created(self):
        cycle1 = Cycle.objects.get(name="Cycle 1 - Q1")
        self.assertEqual(cycle1.genetics, "Sativa")
        self.assertEqual(cycle1.fixture, "led")

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
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 200 characters", str(context.exception))

    def test_seedbank_field_max_length(self):
        cycle = Cycle(name="Cycle 1 - Q1", seedbank="a" * 81)
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 80 characters", str(context.exception))

    def test_fixture_field_max_length(self):
        cycle = Cycle(name="Cycle 1 - Q1", fixture="a" * 201)
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 200 characters", str(context.exception))

    def test_behavioral_response_choices(self):
        cycle = Cycle.objects.create(name="Cycle 1 - Q1", genetics="Sativa", fixture="led", behavioral_response="not-a-valid-choice")
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn("is not a valid choice", str(context.exception))

    def test_seed_type_choices(self):
        cycle = Cycle.objects.create(name="Cycle 1 - Q1", genetics="Sativa", fixture="led", seed_type="not-a-valid-choice")
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn("is not a valid choice", str(context.exception))

    def test_grow_medium_max_length(self):
        cycle = Cycle(name="Cycle 1 - Q1", grow_medium="a" * 31)
        with self.assertRaises(ValidationError) as context:
            cycle.full_clean()
        self.assertIn("Ensure this value has at most 30 characters", str(context.exception))


# Log model test cases
class LogModelTestCase(TestCase):
    def setUp(self):
        self.cycle = Cycle.objects.create(
            name="Cycle 1",
            genetics="Test Genetics",
            seedbank="Test Seedbank",
            fixture="Test Fixture"
        )
        self.cycle_2 = Cycle.objects.create(
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
        self.log_2 = Log.objects.create(
            cycle=self.cycle,
            phase="flowering",
            temperature_day=24.0,
            temperature_night=21.0,
            humidity_day=55,
            humidity_night=65,
            ph=5.7,
            ec=1.2,
            irrigation="Test Irrigation 2",
            light_height=90,
            light_power=30,
            calibration=True
        )
        self.log_3 = Log.objects.create(
            cycle=self.cycle,
            phase="vegetative",
            temperature_day=23.0,
            temperature_night=22.0,
            humidity_day=60,
            humidity_night=70,
            ph=5.8,
            ec=1.5,
            irrigation="Test Irrigation 3",
            light_height=80,
            light_power=35,
            calibration=True
        )
        self.log_4 = Log.objects.create(
            cycle=self.cycle_2,
            phase="vegetative",
            temperature_day=23.0,
            temperature_night=22.0,
            humidity_day=60,
            humidity_night=70,
            ph=5.8,
            ec=1.5,
            irrigation="Test Irrigation 3",
            light_height=80,
            light_power=35,
            calibration=True
        )

    def test_log_str_representation_with_name(self):
        log_str = str(self.log)
        self.assertEqual(log_str, "Cycle 1 - day 1")

    def test_log_str_representation_without_name(self):
        log_str = str(self.log_4)
        self.assertEqual(log_str, "Test Genetics - day 1")

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

    def test_log_has_correct_day_in_cycle(self):
        self.assertEqual(self.log.get_day_in_cycle(), 1)
        self.assertEqual(self.log_2.get_day_in_cycle(), 2)
        self.assertEqual(self.log_3.get_day_in_cycle(), 3)

    def test_log_has_correct_phase_day_in_cycle(self):
        self.assertEqual(self.log.get_phase_day_in_cycle(), 1)
        self.assertEqual(self.log_2.get_phase_day_in_cycle(), 1)
        self.assertEqual(self.log_3.get_phase_day_in_cycle(), 2)


# Nutrient model test cases
class NutrientTestCase(TestCase):
    def setUp(self):
        self.nutrient = Nutrient.objects.create(
            name='NPK Fertilizer',
            brand='Brand X',
            detail='High-quality NPK fertilizer for all plants',
        )

    def test_nutrient_creation(self):
        nutrient = Nutrient.objects.get(name='NPK Fertilizer')
        self.assertEqual(nutrient.brand, 'Brand X')
        self.assertEqual(nutrient.detail, 'High-quality NPK fertilizer for all plants')

    def test_nutrient_string_representation(self):
        self.assertEqual(str(self.nutrient), 'NPK Fertilizer')

    def test_nutrient_type_default(self):
        nutrient = Nutrient.objects.create(
            name='Test Nutrient',
            brand='Test Brand',
            detail='Test Detail'
        )
        self.assertIsNone(nutrient.nutrient_type)

    def test_nutrient_featured_image_default(self):
        nutrient = Nutrient.objects.create(
            name='Test Nutrient',
            brand='Test Brand',
            detail='Test Detail'
        )
        self.assertEqual(nutrient.featured_image.name, 'default_fertilizer.jpg')

    def test_nutrient_detail_blank(self):
        nutrient = Nutrient.objects.create(
            name='Test Nutrient',
            brand='Test Brand',
        )
        self.assertIsNone(nutrient.detail)

    def test_nutrient_type(self):
        nutrient = Nutrient.objects.create(
            name='Test Nutrient',
            brand='Test Brand',
            nutrient_type='bud_strengthener'
        )
        self.assertEqual(nutrient.nutrient_type, 'bud_strengthener')


# NutrientLog model test cases
class NutrientLogTestCase(TestCase):
    def setUp(self):
        cycle = Cycle.objects.create(name="Test Cycle")
        self.log = Log.objects.create(cycle=cycle, phase="vegetative")
        self.nutrient1 = Nutrient.objects.create(name="Test Nutrient 1", brand="Test Brand 1")
        self.nutrient2 = Nutrient.objects.create(name="Test Nutrient 2", brand="Test Brand 2")
        self.nutrient_log = NutrientLog.objects.create(log=self.log, nutrient=self.nutrient1, concentration=100)

    def test_nutrient_log_str(self):
        self.assertEqual(str(self.nutrient_log), "Test Nutrient 1 - 100")

    def test_nutrient_log_concentration(self):
        self.assertEqual(self.nutrient_log.concentration, 100)

    def test_nutrient_log_save_multiple_nutrients(self):
        NutrientLog.objects.create(log=self.log, nutrient=self.nutrient2, concentration=75)
        self.assertEqual(NutrientLog.objects.count(), 2)

    def test_nutrient_log_ordering(self):
        nutrient3 = Nutrient.objects.create(name="Test Nutrient 3", brand="Test Brand 3")
        NutrientLog.objects.create(log=self.log, nutrient=self.nutrient2, concentration=75)
        NutrientLog.objects.create(log=self.log, nutrient=nutrient3, concentration=50)
        logs = NutrientLog.objects.filter(log=self.log)
        self.assertEqual(logs[0].nutrient, self.nutrient1)
        self.assertEqual(logs[1].nutrient, self.nutrient2)
        self.assertEqual(logs[2].nutrient, nutrient3)
