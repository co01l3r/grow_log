from typing import List, Tuple, Optional
import uuid

from django.db import models
from django.db.models import Case, Value, When


# Record model
class Cycle(models.Model):
    """
    A model representing a cycle of a plant growth.

    Fields:
        id (UUIDField): The primary key of the cycle, a UUID value. Required field.
        date (DateField): The date when the cycle started, set automatically on creation.
        genetics (CharField): The genetics of the plant being grown, a string value up to 200 characters. Required field.
        seedbank (CharField): The seed bank where the seeds were purchased from, a string value up to 80 characters.
        fixture (CharField): The type of light fixture used for the growth, a string value up to 200 characters. Required field.
        seed_type (CharField): The type of seeds used, either "regular", "feminized", or "clones".
        grow_medium (CharField): The type of grow medium used for the growth, a string value up to 30 characters.
        name (CharField): The name given to the cycle, a string value up to 80 characters.

    Meta:
        ordering (List): A list of strings representing the fields to order the results by. The results will be
        reverse ordered the first by date, then by id.

    Methods:
        __str__ (str): Returns a string representation of the cycle object. Formatted as "[name or genetics] - Q[quarter]/[year]".
    """
    BEHAVIORAL_RESPONSE_CHOICES: List[Tuple[str, str]] = [
        ('auto-flowering', 'Auto-flowering'),
        ('photoperiodic', 'Photoperiodic'),
    ]
    SEED_TYPE_CHOICES: List[Tuple[str, str]] = [
        ('regular', 'Regular'),
        ('feminized', 'Feminized'),
        ('clones', 'Clones'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    genetics = models.CharField(max_length=200)
    seedbank = models.CharField(max_length=80, blank=True, null=True)
    fixture = models.CharField(max_length=200)
    behavioral_response = models.CharField(max_length=30, blank=True, null=True, choices=BEHAVIORAL_RESPONSE_CHOICES)
    seed_type = models.CharField(max_length=30, blank=True, null=True, choices=SEED_TYPE_CHOICES)
    grow_medium = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True)

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
        get_day_in_cycle (int):             Returns the day in the cycle.
        get_phase_day_in_cycle (int):       Returns the day in the phase of cycle.
        get_previous_log (Optional['Log']): Returns the previous log object based on the ID of the current log object,
                                            if no previous logs exist, returns None.
        __str__ (str):                      Returns name or genetics and day position for the cycle.
                                            Formatted as "[cycle name or genetics] - [day_in_cycle]".
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
        all_logs: models.QuerySet = Log.objects.filter(cycle=self.cycle).order_by('date', 'id')
        day_in_cycle: int = list(all_logs).index(self) + 1
        return int(day_in_cycle)

    def get_phase_day_in_cycle(self) -> int:
        logs_of_same_phase: models.QuerySet = Log.objects.filter(cycle=self.cycle, phase=self.phase)
        day_in_phase: int = list(logs_of_same_phase).index(self) + 1
        return int(day_in_phase)

    def get_previous_log(self) -> Optional['Log']:
        previous_logs: models.QuerySet = self.cycle.logs.filter(id__lt=self.id).order_by('-id')
        if previous_logs.exists():
            return previous_logs.first()
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
        save(*args, **kwargs): Overrides the default save method. If a `NutrientLog` already exists for the same `Log`
                               and `Nutrient`, the concentrations are added together and the existing logs are
                               deleted before saving the new `NutrientLog` instance.
        __str__ (str):         Returns the name and concentration of the nutrient log as a string.
                                formatted as "[nutrient] - [concentration]".
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


# Reservoir model
class Reservoir(models.Model):
    RO_OPTIONS: List[Tuple[str, str]] = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('mix', 'Mix'),
    ]
    RESERVOIR_STATUS: List[Tuple[str, str]] = [
        ('refresh', 'Refresh'),
        ('refill', 'Refill'),
    ]
    log = models.ForeignKey('Log', on_delete=models.CASCADE)
    water = models.IntegerField()
    waste_water = models.IntegerField(blank=True, null=True)
    ro = models.BooleanField(choices=RO_OPTIONS, default='yes', max_length=3)
    status = models.CharField(choices=RESERVOIR_STATUS, max_length=7)

    def __str__(self) -> str:
        return f"{self.status} - {self.water}"
