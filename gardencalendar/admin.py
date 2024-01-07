
from django.contrib import admin

from .models import User_Profile, Task, GeneralTask, Garden, GrowthStage, Plant, UserTask



# Customizing ModelAdmin classes

@admin.register(UserTask)

class UserTaskAdmin(admin.ModelAdmin):

    list_display = ['user', 'garden', 'description', 'frequency', 'start_date']



    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        return qs.filter(user=request.user)
    




@admin.register(User_Profile)

class User_ProfileAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'is_staff', 'is_superuser', 'is_active']



@admin.register(Task)

class TaskAdmin(admin.ModelAdmin):

    list_display = ['plant', 'description', 'frequency']



@admin.register(GeneralTask)

class GeneralTaskAdmin(admin.ModelAdmin):

    list_display = ['description', 'frequency']



@admin.register(Garden)

class GardenAdmin(admin.ModelAdmin):

    list_display = ['user', 'name', 'zip_code']



    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        return qs.filter(user=request.user)



@admin.register(GrowthStage)

class GrowthStageAdmin(admin.ModelAdmin):

    list_display = ['plant', 'description', 'growing_time']



@admin.register(Plant)

class PlantAdmin(admin.ModelAdmin):

    list_display = ['name', 'description']

