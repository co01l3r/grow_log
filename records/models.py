from typing import List, Tuple, Optional
import uuid, logging

from django.db import models
from django.db.models import Case, Value, When


# Record model
class Cycle(models.Model):
    """
    A model representing a cycle of a plant growth.

    Fields:
        id (UUIDField): The primary key of the cycle, a UUID value.
        date (DateField): The date when the cycle started, set automatically on creation.
        light_type(CharField): The type of light fixture used for the growth, a string value up to 32 characters
        fixture (CharField): Fixture model used, a string value up to 80 characters.
        name (CharField): The name given to the cycle, a string value up to 80 characters.
        genetics (CharField): The genetics of the plant being grown, a string value up to 150 characters.
        seedbank (CharField): The seed bank where the seeds were purchased from, a string value up to 80 characters.
        reproductive_cycle (CharField): The type of plant reproductive cycle, either "auto-flowering", "photoperiodic".
        seed_type (CharField): The type of seeds used, either "regular", "feminized", or "clones".
        grow_medium (CharField): The type of grow medium used for the growth, a string value up to 30 characters.

    Meta:
        ordering (List): A list of strings representing the fields to order the results by. The results will be
        reverse ordered the first by date, then by id.

    Methods:
        __str__ (str): Returns a string representation of the cycle object. Formatted as "[name or genetics] - Q[quarter]/[year]".
    """
    CYCLE_OPTIONS: List[Tuple[str, str]] = [
        ('auto-flowering', 'Auto-flowering'),
        ('photoperiodic', 'Photoperiodic'),
    ]
    LIGHT_TYPE_OPTIONS: List[Tuple[str, str]] = [
        ('led', 'Light-Emitting Diode (LED)'),
        ('hps', 'High pressure sodium vapor (HPS)'),
        ('cfl', 'Compact fluorescent (CFL)'),
        ('hid', 'High-intensity discharge (HID)'),
        ('cmh', 'Ceramic metal halide (CMH)'),
    ]
    SEED_TYPE_CHOICES: List[Tuple[str, str]] = [
        ('regular', 'Regular'),
        ('feminized', 'Feminized'),
        ('clones', 'Clones'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    light_type = models.CharField(max_length=32, choices=LIGHT_TYPE_OPTIONS,  default='led')
    fixture = models.CharField(max_length=80, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True)
    genetics = models.CharField(max_length=150)
    seedbank = models.CharField(max_length=80, blank=True, null=True)
    reproductive_cycle = models.CharField(max_length=30, choices=CYCLE_OPTIONS, default='photoperiodic')
    seed_type = models.CharField(max_length=30, choices=SEED_TYPE_CHOICES, default='feminized')
    grow_medium = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        ordering: List = [
            '-date',
            '-id',
        ]

    def __str__(self) -> str:
        quarter: str = "Q" + str((self.date.month - 1) // 3 + 1)
        year: str = str(self.date.year)

        if self.name:
            name: str = self.name if quarter in self.name else f"{self.name} - {quarter}"
            return f"{name}/{year}"
        else:
            return f"{self.genetics} - {quarter}/{year}"


# Log model
class Log(models.Model):
    """
    Model to represent a log for a specific phase of a cycle of growth.

    Fields:
        cycle (Cycle): The cycle associated with the log. Required field.
        date (DateField): The date when the log was created, set automatically on creation.
        phase (str): The phase of the cycle associated with the log. Required field.
        temperature_day (DecimalField): The temperature during the day.
        temperature_night (DecimalField): The temperature during the night.
        humidity_day (IntegerField): The humidity during the day, as a percentage.
        humidity_night (IntegerField): The humidity during the night, as a percentage.
        ph (DecimalField): The pH level for the day.
        ec (DecimalField): The electrical conductivity (EC) level for the day.
        irrigation (str): The irrigation applied during the day.
        light_height (IntegerField): The height of the light from the plants canopy during the day.
        light_power (IntegerField): The power of the light during the day, as a percentage.
        calibration (bool): Whether the equipment was calibrated during the day.
        featured_image (ImageField): A photo associated with the log.
        carbon_dioxide (IntegerField): The amount of average co2 in the growing area during the day.
        comment (TextField): An optional comment about the day.

    Meta:
        ordering (List): The default ordering for logs, first by phase, then by date, then by id.

    Methods:
        get_day_in_cycle (int):                     Returns the day in the cycle.
        get_phase_day_in_cycle (int):               Returns the day in the phase of cycle.
        get_previous_log (Optional['Log']):         Returns the previous log object based on the ID of the current
                                                    log object, if no previous logs exist, returns None.
        __str__ (str):                              Returns name or genetics and day position for the cycle.
                                                    Formatted as "[cycle name or genetics] - [day_in_cycle]".
        get_days_since_calibration(Optional[int]):  Returns the number of consecutive days that the equipment was not
                                                    calibrated, up to the current log.
    """
    PHASE_CHOICES: List[Tuple[str, str]] = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('bloom', 'Bloom'),
    ]
    LIGHT_POWER_CHOICES: List[Tuple[int, str]] = [
        (0, 'Darkness'),
        (25, '25%'),
        (50, '50%'),
        (75, '75%'),
        (100, '100%'),
    ]
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(auto_now_add=True)
    phase = models.CharField(max_length=12, choices=PHASE_CHOICES, default='vegetative')
    temperature_day = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temperature_night = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    humidity_day = models.IntegerField(blank=True, null=True)
    humidity_night = models.IntegerField(blank=True, null=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ec = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    irrigation = models.CharField(max_length=20, blank=True, null=True)
    light_height = models.IntegerField(blank=True, null=True)
    light_power = models.IntegerField(blank=True, null=True, choices=LIGHT_POWER_CHOICES)
    calibration = models.BooleanField(default=False, blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True)
    carbon_dioxide = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering: List = [
            Case(
                When(phase='seedling', then=Value(1)),
                When(phase='vegetative', then=Value(2)),
                When(phase='bloom', then=Value(3)),
            ),
            'date',
            'id',
        ]

    def get_day_in_cycle(self) -> int:
        try:
            all_logs: models.QuerySet = Log.objects.filter(cycle=self.cycle).order_by('date', 'id')
            day_in_cycle: int = list(all_logs).index(self) + 1
            return int(day_in_cycle)
        except Exception as e:
            logging.exception(f"Unable to get the day in cycle value: {e}")

    def get_phase_day_in_cycle(self) -> int:
        try:
            logs_of_same_phase: models.QuerySet = Log.objects.filter(cycle=self.cycle, phase=self.phase)
            day_in_phase: int = list(logs_of_same_phase).index(self) + 1
        except ValueError:
            day_in_phase = 1
        return int(day_in_phase)

    def get_previous_log(self) -> Optional['Log']:
        try:
            previous_logs: models.QuerySet = self.cycle.logs.filter(id__lt=self.id).order_by('-id')
        except Exception as e:
            logging.exception(f"Unable to fetch the previous 'Log': {e}")
            return None

        if previous_logs.exists():
            return previous_logs.first()
        return None

    def get_days_since_calibration(self) -> Optional[int]:
        try:
            consecutive_false_count: int = 0
            for log in self.cycle.logs.filter(pk__lte=self.pk).order_by('-id'):
                if not log.calibration:
                    consecutive_false_count += 1
                elif log.calibration:
                    break
            return consecutive_false_count if consecutive_false_count > 0 else None
        except Exception as e:
            logging.exception(f"An error occurred during the calculation: {e}")
            return None

    def __str__(self) -> str:
        day_in_cycle = self.get_day_in_cycle()
        if self.cycle.name:
            return f"{self.cycle.name} - day {str(day_in_cycle)}"
        else:
            return f"{self.cycle.genetics} - day {str(day_in_cycle)}"


# Nutrient model
class Nutrient(models.Model):
    """
    Model representing a nutrient used in growing.

    Fields:
        name (CharField): The name of the nutrient. Required field.
        brand (CharField): The brand of the nutrient. Required field.
        nutrient_type (CharField): The type of the nutrient.
        featured_image (ImageField): An image representing the nutrient.
        detail (TextField): Additional details about the nutrient.

    Meta:
        ordering (List): A list of strings representing the fields to order the results by. The results will be ordered
                         the first by brand, then by nutrient_type, then by name.

    Methods:
        __str__ (str): Returns the name of the nutrient as a string.

    """
    NUTRIENT_TYPE_CHOICES: List[Tuple[str, str]] = [
        ('medium_conditioner', 'Medium conditioner'),
        ('base_line', 'Base'),
        ('root_expander', 'Root expander'),
        ('bud_strengthener', 'Strengthener'),
        ('bud_enlarger', 'Bud enlarger'),
        ('bud_taste', 'Bud taste'),
    ]
    name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    nutrient_type = models.CharField(max_length=18, blank=True, null=True, choices=NUTRIENT_TYPE_CHOICES)
    featured_image = models.ImageField(null=True, blank=True, default="default_fertilizer.jpg")
    detail = models.TextField(blank=True, null=True)

    class Meta:
        ordering: List = [
            'brand',
            'nutrient_type',
            'name',
        ]

    def __str__(self) -> str:
        return self.name


# NutrientLog model
class NutrientLog(models.Model):
    """
    A model representing the nutrient logs for a specific `Log`.

    Fields:
        log (ForeignKey): A foreign key referencing the `Log` model this nutrient log belongs to. Required field.
        nutrient (ForeignKey): A foreign key referencing the `Nutrient` model this nutrient log corresponds to. Reuired field.
        concentration (IntegerField): An integer representing the concentration of the nutrient for this log. Required field.

    Meta:
        ordering (List): A list of strings representing the fields to order the results by. The results will be ordered
                         the first by medium_conditioner, then by base_line, then by root_expander,
                         then by bud_strengthener, then by bud_enlarger, then by bud_taste.

    Methods:
        save():                                             Overrides the default save method. If a `NutrientLog`
                                                            already exists for the same `Log` and `Nutrient`, the
                                                            concentrations are added together and the existing logs
                                                            are deleted before saving the new `NutrientLog` instance.

        __str__ (str):                                      Returns the name and concentration of the nutrient log as
                                                            a string. formatted as "[nutrient] - [concentration]".

        get_nutrient_usage_per_liter (Optional[float]):     Calculates the nutrient usage per liter for the current
                                                            `NutrientLog` instance, if possible. Returns the nutrient
                                                            usage per liter as a float rounded to two decimal places,
                                                            or `None` if the required data is missing.
    """
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='nutrient_logs')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    concentration = models.IntegerField()

    class Meta:
        ordering: List = [
            Case(
                When(nutrient__nutrient_type='medium_conditioner', then=Value(1)),
                When(nutrient__nutrient_type='base_line', then=Value(2)),
                When(nutrient__nutrient_type='root_expander', then=Value(3)),
                When(nutrient__nutrient_type='bud_strengthener', then=Value(4)),
                When(nutrient__nutrient_type='bud_enlarger', then=Value(5)),
                When(nutrient__nutrient_type='bud_taste', then=Value(6)),
            ),
        ]

    def __str__(self) -> str:
        return f"{self.nutrient} - {self.concentration}"

    def save(self, *args, **kwargs) -> None:
        existing_logs: models.QuerySet = NutrientLog.objects.filter(log_id=self.log_id, nutrient=self.nutrient)
        if existing_logs.exists():
            self.concentration += sum(log.concentration for log in existing_logs)
            existing_logs.delete()
        super().save(*args, **kwargs)

    def get_nutrient_usage_per_liter(self) -> Optional[float]:
        try:
            reservoir_log = self.log.reservoir_logs.first()
            if reservoir_log:
                water = reservoir_log.water
                if water:
                    usage: float = self.concentration / water
                    return round(usage, 2)
        except ReservoirLog.DoesNotExist:
            pass


# ReservoirLog model
class ReservoirLog(models.Model):
    """
    A model representing a log entry for a reservoir, storing information such as the amount of water, waste water,
    reverse osmosis usage, and reservoir status.

    Fields:
        log (ForeignKey): A foreign key to the Log model, representing the log entry that this reservoir log belongs to.
        status (CharField): A character field representing the status of the reservoir.
        reverse_osmosis (CharField): A character field representing whether reverse osmosis is used or not.
        water (IntegerField): An optional integer field representing the amount of water.
        waste_water (IntegerField): An optional integer field representing the amount of waste water.
        ro_amount (IntegerField): An optional integer field representing the amount of water that underwent reverse osmosis.

    Methods:
        __str__(str):                           Returns a string representation of the ReservoirLog object.

        get_ro_water_ratio(Optional[int]):      Calculates and returns the ratio of water that underwent reverse
                                                osmosis to the total water amount in %.

        save():                                 Overrides the default save method to update existing logs and calculate
                                                reverse osmosis usage.
        _update_existing_log():                 Helper method to update an existing log.
        _update_existing_ro_amount():           Helper method to update the reverse osmosis amount of an existing log.
        _update_existing_waste_water():         Helper method to update the waste water amount of an existing log.
    """
    RO_OPTIONS: List[Tuple[str, str]] = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    RESERVOIR_STATUS: List[Tuple[str, str]] = [
        ('refresh', 'Refresh'),
        ('refill', 'Refill'),
    ]
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='reservoir_logs')
    status = models.CharField(choices=RESERVOIR_STATUS, default='refill', max_length=7, editable=False)
    reverse_osmosis = models.CharField(choices=RO_OPTIONS, default='yes', max_length=3)
    water = models.IntegerField(blank=True, null=True)
    waste_water = models.IntegerField(blank=True, null=True)
    ro_amount = models.IntegerField(blank=True, null=True, editable=False)

    def __str__(self) -> str:
        return f"{self.status} - {self.water}"

    def save(self, *args, **kwargs):
        if self.reverse_osmosis == 'yes':
            if self.ro_amount is None:
                self.ro_amount = self.water
            else:
                self.ro_amount += self.water
        else:
            self.ro_amount = None

        try:
            existing_log: models.QuerySet = ReservoirLog.objects.get(log=self.log)
            existing_log.water = (existing_log.water or 0) + (self.water or 0)
            self._update_existing_log(existing_log)
            super(ReservoirLog, existing_log).save(*args, **kwargs)
        except ReservoirLog.DoesNotExist:
            if self.waste_water is not None:
                self.status = 'refresh'
            super().save(*args, **kwargs)
        except Exception as e:
            logging.exception(f"An error occurred: {e}")

    def _update_existing_log(self, existing_log: 'ReservoirLog') -> None:
        if self.reverse_osmosis == 'yes':
            self._update_existing_ro_amount(existing_log)
        if self.waste_water is not None:
            self._update_existing_waste_water(existing_log)

    def _update_existing_ro_amount(self, existing_log: 'ReservoirLog') -> None:
        existing_log.ro_amount = existing_log.ro_amount or 0
        existing_log.ro_amount += self.water if self.water is not None else 0

    def _update_existing_waste_water(self, existing_log: 'ReservoirLog') -> None:
        existing_log.waste_water = (existing_log.waste_water or 0) + (self.waste_water or 0)
        if self.waste_water != 0:
            existing_log.status = 'refresh'
        elif existing_log.waste_water == 0:
            existing_log.status = 'refill'

    def get_percent_ro_ratio(self) -> Optional[int]:
        try:
            if self.ro_amount is not None and self.water != 0:
                return round(self.ro_amount / self.water * 100)
            else:
                return None
        except Exception as e:
            logging.exception(f"An error occurred during the calculation: {e}")
            return None
