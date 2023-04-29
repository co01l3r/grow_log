from django.contrib import admin
from .models import Cycle, Log, Nutrient, NutrientLog, ReservoirLog

# Register your models here.

admin.site.register(Cycle)
admin.site.register(Log)
admin.site.register(Nutrient)
admin.site.register(NutrientLog)
admin.site.register(ReservoirLog)
