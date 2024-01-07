

from django.contrib import admin

from .models import Task, Garden, GrowthStage, Plant, UserTask



@admin.register(Task)

class TaskAdmin(admin.ModelAdmin):

    list_display = ('plant', 'description', 'frequency')



@admin.register(Garden)

class GardenAdmin(admin.ModelAdmin):

    list_display = ('user', 'name', 'zip_code')



@admin.register(GrowthStage)

class GrowthStageAdmin(admin.ModelAdmin):

    list_display = ('plant', 'description', 'growing_time')



@admin.register(Plant)

class PlantAdmin(admin.ModelAdmin):

    list_display = ('name', 'description')



@admin.register(UserTask)

class UserTaskAdmin(admin.ModelAdmin):

    list_display = ('user', 'plant', 'description', 'frequency', 'start_date')
