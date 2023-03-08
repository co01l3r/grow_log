from django.db import models
import uuid


# Record model
class Cycle(models.Model):
    BEHAVIORAL_RESPONSE_CHOICES = [
        ('auto-flowering', 'Auto-flowering'),
        ('photoperiodic', 'Photoperiodic'),
    ]
    SEED_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('feminized', 'Feminized'),
        ('clones', 'Clones'),
    ]
    BEGINNING_PHASE_CHOICES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField(auto_now_add=True)
    genetics = models.CharField(max_length=200)
    seedbank = models.CharField(max_length=80, blank=True, null=True)
    fixture = models.CharField(max_length=200)
    behavioral_response = models.CharField(max_length=80, blank=True, null=True, choices=BEHAVIORAL_RESPONSE_CHOICES)
    seed_type = models.CharField(max_length=80, blank=True, null=True, choices=SEED_TYPE_CHOICES)
    grow_medium = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=80, blank=True)
    beginning_phase = models.CharField(max_length=80, blank=True, null=True, choices=BEGINNING_PHASE_CHOICES, default='vegetative')

    def __str__(self):
        quarter = "Q" + str((self.date.month - 1) // 3 + 1)
        year = str(self.date.year)

        if self.name:
            name = self.name if quarter in self.name else f"{self.name} - {quarter}"
            return f"{name}/{year}"
        else:
            return f"{self.genetics} - {quarter}/{year}"


# Log model
class Log(models.Model):
    PHASE_CHOICES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('bloom', 'Bloom'),
    ]
    LIGHT_POWER_CHOICES = [
        (0, 'Darkness'),
        (25, '25%'),
        (50, '50%'),
        (75, '75%'),
        (100, '100%'),
    ]
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='logs')
    phase = models.CharField(max_length=12, choices=PHASE_CHOICES)
    temperature_day = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    temperature_night = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    humidity_day = models.IntegerField(blank=True, null=True)
    humidity_night = models.IntegerField(blank=True, null=True)
    ph = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    ec = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    irrigation = models.TextField(max_length=20, blank=True, null=True)
    light_height = models.IntegerField(blank=True, null=True)
    light_power = models.IntegerField(blank=True, null=True, choices=LIGHT_POWER_CHOICES)
    calibration = models.BooleanField(default=False, blank=True, null=True)
    featured_image = models.ImageField(null=True, blank=True)
    water = models.IntegerField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        logs_of_same_phase = Log.objects.filter(cycle=self.cycle, phase=self.phase)
        day_in_phase = list(logs_of_same_phase).index(self) + 1
        return str(day_in_phase)


# Nutrient model
class Nutrient(models.Model):
    name = models.CharField(max_length=80)
    brand = models.CharField(max_length=80)
    featured_image = models.ImageField(null=True, blank=True, default="default_fertilizer.jpg")
    detail = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# NutrientLog model
class NutrientLog(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='nutrient_logs')
    nutrient = models.ForeignKey(Nutrient, on_delete=models.CASCADE)
    concentration = models.IntegerField()

    def __str__(self):
        return f"{self.nutrient} - {self.concentration}"
