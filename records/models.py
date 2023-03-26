from django.db import models
import uuid
from django.db.models import Case, Value, When
from typing import List, Tuple


# Record model
class Cycle(models.Model):
    """
    A model representing a cycle of a cannabis plant growth.

    Attributes:
        id (UUIDField): The primary key of the cycle, a UUID value.
        date (DateField): The date when the cycle started, set automatically on creation.
        genetics (CharField): The genetics of the plant being grown, a string value up to 200 characters.
        seedbank (CharField): The seed bank where the seeds were purchased from, a string value up to 80 characters.
        fixture (CharField): The type of light fixture used for the growth, a string value up to 200 characters.
        behavioral_response (CharField): The behavioral response of the plant, either "auto-flowering" or "photoperiodic".
        seed_type (CharField): The type of seeds used, either "regular", "feminized", or "clones".
        grow_medium (CharField): The type of grow medium used for the growth, a string value up to 30 characters.
        name (CharField): The name given to the cycle, a string value up to 80 characters.

    Methods:
        __str__(): Returns a string representation of the cycle object, formatted as "[name or genetics] - Q[quarter]/[year]".
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
        cycle (Cycle): The cycle associated with the log.
        date (DateField): The date the log was created.
        phase (str): The phase of the cycle associated with the log.
        temperature_day (DecimalField): The temperature during the day for the phase.
        temperature_night (DecimalField): The temperature during the night for the phase.
        humidity_day (IntegerField): The humidity during the day for the phase, in percent.
        humidity_night (IntegerField): The humidity during the night for the phase, in percent.
        ph (DecimalField): The pH level for the phase.
        ec (DecimalField): The electrical conductivity (EC) level for the phase.
        irrigation (str): The type of irrigation used for the phase.
        light_height (IntegerField): The height of the light from the plants during the phase.
        light_power (IntegerField): The power of the light during the phase, as a percentage (0-100%).
        calibration (bool): Whether or not the equipment was calibrated during the day.
        featured_image (ImageField): An optional image associated with the log.
        water (IntegerField): The amount of water given to the plants during the phase.
        comment (TextField): An optional comment about the day.

    Meta:
        ordering (List): The default ordering for logs, first by phase, then by date, then by id.

    Methods:
        __str__ (str): Returns the day number of the phase the log represents.
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
    water = models.IntegerField(blank=True, null=True)
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

    def __str__(self) -> str:
        logs_of_same_phase: models.QuerySet = Log.objects.filter(cycle=self.cycle, phase=self.phase)
        day_in_phase: int = list(logs_of_same_phase).index(self) + 1
        return str(day_in_phase)


# Nutrient model
class Nutrient(models.Model):
    """
    Model representing a nutrient used in growing.

    Attributes:
        NUTRIENT_TYPE_CHOICES (List[Tuple[str, str]]): A list of tuples representing the available types of nutrients.
        name (CharField): The name of the nutrient.
        brand (CharField): The brand of the nutrient.
        nutrient_type (CharField): The type of the nutrient.
        featured_image (ImageField): An image representing the nutrient.
        detail (TextField): Additional details about the nutrient.

    Methods:
        __str__(self): Returns the name of the nutrient as a string.

    """
    NUTRIENT_TYPE_CHOICES: List[Tuple[str, str]] = [
        ('medium_conditioner', 'Medium conditioner'),
        ('base_line', 'Base'),
        ('root_expander', 'Root expander'),
        ('bud_strengthener', 'Bud strengthener'),
        ('bud_enlarger', 'Bud enlarger'),
        ('bud_taste', 'Bud taste'),
    ]
    name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    nutrient_type = models.CharField(max_length=18, blank=True, null=True, choices=NUTRIENT_TYPE_CHOICES)
    featured_image = models.ImageField(null=True, blank=True, default="default_fertilizer.jpg")
    detail = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


# NutrientLog model
class NutrientLog(models.Model):
    """
    A model representing the nutrient logs for a specific `Log`.

    Attributes:
        log (ForeignKey): A foreign key referencing the `Log` model this nutrient log belongs to.
        nutrient (ForeignKey): A foreign key referencing the `Nutrient` model this nutrient log corresponds to.
        concentration (IntegerField): An integer representing the concentration of the nutrient for this log.

    Meta:
        ordering (List): A list of strings representing the fields to order the results by. The results will be ordered
                          by the `nutrient__nutrient_type` field.

    Methods:
        save(*args, **kwargs): Overrides the default save method. If a `NutrientLog` already exists for the same `Log`
                               and `Nutrient`, the concentrations are added together and the existing logs are
                               deleted before saving the new `NutrientLog` instance.
        __str__ (str):         Returns the name and concentration of the nutrient log as a string,
                                formatted as "[nutrient] - [concentration]".
    """
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='nutrient_logs')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    concentration = models.IntegerField()

    class Meta:
        ordering: List = ['nutrient__nutrient_type']

    def __str__(self) -> str:
        return f"{self.nutrient} - {self.concentration}"

    def save(self, *args, **kwargs) -> None:
        existing_logs = NutrientLog.objects.filter(log_id=self.log_id, nutrient=self.nutrient)
        if existing_logs.exists():
            self.concentration += sum(log.concentration for log in existing_logs)
            existing_logs.delete()
        super().save(*args, **kwargs)
