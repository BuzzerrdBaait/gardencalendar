from django.contrib import admin

from .models import *




@admin.register(UserTask)

class UserTaskAdmin(admin.ModelAdmin):

    list_display = ['garden', 'description', 'frequency', 'start_date']



    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        return qs.filter(user=request.user)



@admin.register(User_Profile)

class User_ProfileAdmin(admin.ModelAdmin):

    list_display = ['username', 'email', 'is_staff', 'is_superuser', 'is_active']



@admin.register(Plant_specific_task)

class Plant_specific_taskAdmin(admin.ModelAdmin):

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

    list_display = ['plant', 'description', 'min_time_in_days', 'max_time_in_days']



@admin.register(Plant)

class PlantAdmin(admin.ModelAdmin):

    list_display = ['name', 'description']



    def get_queryset(self, request):

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs

        return qs.filter(growth_stages__plant__user=request.user, tasks__plant__user=request.user)

