from django.contrib import admin
import models
# Register your models here.

admin.site.register(models.all)
admin.site.register(models.daily)
admin.site.register(models.dpartTrade)
admin.site.register(models.coTrade)
admin.site.register(models.monthGoal)
admin.site.register(models.DpartDetail)
admin.site.register(models.SpartDetail)
admin.site.register(models.personalScore)
admin.site.register(models.Intergral_rank)