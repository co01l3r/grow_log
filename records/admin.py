from django.contrib import admin
from .models import Cycle, DayLog, Nutrient

# Register your models here.

admin.site.register(Cycle)
admin.site.register(DayLog)
admin.site.register(Nutrient)
