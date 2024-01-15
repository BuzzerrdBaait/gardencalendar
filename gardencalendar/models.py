import secrets

import string

from django.db import models

from django.utils import timezone

from datetime import timedelta

from django.db.models.signals import post_save

from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser

from .frost_scraper import scrape, clean_data, frost_info

from .geolocator import geocode



class User_Profile(AbstractUser):

    email = models.CharField(max_length=40, blank=True, null=True, unique=True)

    authentication_key = models.CharField(max_length=50, unique=True)

    is_verified = models.CharField(max_length=1, default='N')

    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    user_library = models.CharField(max_length=255, default='', blank=True)

    authentication_link = models.CharField(max_length=50, blank=True, null=True)



    def generate_unique_link(self):

        link = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))

        link = link.replace('\\', str(secrets.randbelow(1000)))

        link = link.replace('/', str(secrets.randbelow(1000)))

        link = link.replace("'", str(secrets.randbelow(1000)))

        link = link.replace('"', str(secrets.randbelow(1000)))

        return link



    def save(self, *args, **kwargs):

        if not self.authentication_key:

            self.authentication_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))

        if not self.authentication_link:

            self.authentication_link = self.generate_unique_link()

        super().save(*args, **kwargs)



class Plant_specific_task(models.Model):

    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='plant_tasks')

    description = models.TextField(default='no description available')

    frequency = models.DurationField(default=timedelta(days=1))



    def save(self, *args, **kwargs):

        if not self.pk:
            
            super().save(*args, **kwargs)

            self.plant.tasks.add(self)

            self.plant.save()



    def __str__(self):

        return f"Task for {self.plant.name} - {self.description}"



class GeneralTask(models.Model):

    description = models.TextField(default='no description available')

    frequency = models.DurationField(default=timedelta(days=1))



    def __str__(self):

        return self.description



class Garden(models.Model):

    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE, related_name='gardens')

    name = models.CharField(max_length=50)

    zip_code = models.CharField(max_length=10)

    x_coord=models.CharField(max_length=40, blank=True, default='leave blank')

    y_coord=models.CharField(max_length=40, blank=True, default='leave blank')

    city_state=models.CharField(max_length=25,blank=True,default='leave blank')

    spring_frost=models.CharField(max_length=25,blank=True,default='leave blank')

    fall_frost=models.CharField(max_length=25, blank=True,default='leave blank')

    season_length=models.CharField(max_length=25, blank=True, default='leave blank')

    plants = models.ManyToManyField('Plant', related_name='gardens', blank=True, through='PlantInGarden')

    user_tasks = models.ManyToManyField('UserTask', related_name='gardens', blank=True)

    general_tasks = models.ManyToManyField(GeneralTask, related_name='gardens', blank=True)

    

    def save(self, *args, **kwargs):

        if self.city_state == 'leave blank' or self.spring_frost == 'leave blank' or self.fall_frost == 'leave blank' or self.season_length == 'leave blank':

            country='USA'

            # If any of the fields are set to "leave blank," fetch data from the scraper

            zipcode = self.zip_code

            coords=geocode(zipcode,country)

            if coords:
                location_info=coords[2].split(",")
                city_state=f"{location_info[0]}, {location_info[3]}"
                credit=coords[3]
                x=coords[0]
                y=[coords[1]]

                print(f"Your location is {city_state}")
                
                print(f"Latitude == {coords[0]}, Longitude == {coords[1]}")

                print(f"Geolocation done by--> {coords[3]}")


                self.x_coord=x
                self.y_coord=y

            url_to_scrape = f'https://www.almanac.com/gardening/frostdates/zipcode/{zipcode}'

            html_content = scrape(url_to_scrape)



            if html_content:

                clean_data(html_content)

                # Update the Garden model fields with the scraped information if the corresponding field is set to "leave blank"

                self.city_state = self.city_state if self.city_state != 'leave blank' else frost_info[0]

                self.spring_frost = self.spring_frost if self.spring_frost != 'leave blank' else frost_info[2]

                self.fall_frost = self.fall_frost if self.fall_frost != 'leave blank' else frost_info[3]

                self.season_length = self.season_length if self.season_length != 'leave blank' else frost_info[4]



        super().save(*args, **kwargs)
    

    def __str__(self):

        return self.name



class PlantInGarden(models.Model):

    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)

    garden = models.ForeignKey('Garden', on_delete=models.CASCADE)

    quantity=models.IntegerField(blank=True, default=None)

    added_at = models.DateTimeField(default=timezone.now)

    min_completion = models.DateTimeField(default=None, blank=True)

    max_completion = models.DateTimeField(default=None, blank=True)

    growth_phase_info = models.JSONField(default=dict, blank=True)



    def calculate_completion_dates(self):

        # Calculate min and max completion based on related Plant model

        min_growth_time = self.plant.min_growth_time

        max_growth_time = self.plant.max_growth_time

        self.min_completion = self.added_at + min_growth_time

        self.max_completion = self.added_at + max_growth_time



        # Calculate min and max growth phase end based on GrowthStage model

        growth_phase_info = {}



        for stage in self.plant.growth_stages.all():

            min_growth_end = self.added_at + stage.min_time_of_start_within_the_cycle + stage.min_length_in_days

            max_growth_end = self.added_at + stage.max_time_of_start_within_the_cycle + stage.max_length_in_days

            json_title=f"{stage.pk} {stage.growth_stages}"



            growth_phase_info[json_title] = {

                'min_growth_phase_end': min_growth_end.strftime('%Y-%m-%d %H:%M:%S'),

                'max_growth_phase_end': max_growth_end.strftime('%Y-%m-%d %H:%M:%S'),

            }



        return growth_phase_info



    def save(self, *args, **kwargs):

        self.growth_phase_info = self.calculate_completion_dates()

        super().save(*args, **kwargs)


class GrowthStage(models.Model):

    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='plant_growth_stages')

    stage_number=models.IntegerField(null=True)

    growth_stages=models.CharField(default='Name of growth stage', max_length=50)

    description = models.TextField(blank=True, null=True)

    min_time_of_start_within_the_cycle= models.DurationField(default='0 00:00:00')

    max_time_of_start_within_the_cycle= models.DurationField(default='0 00:00:00')

    min_length_in_days = models.DurationField(default='0 00:00:00', blank=True)

    max_length_in_days = models.DurationField(default='0 00:00:00', blank=True)



    
    def save(self, *args, **kwargs):

        if not self.pk:
            
            super().save(*args, **kwargs)

            self.plant.growth_stages.add(self)

            self.plant.save()


    def __str__(self):

        return f"{self.description}"



class Plant(models.Model):

    name = models.CharField(max_length=50)

    description = models.TextField(default='no description available')

    growth_stages = models.ManyToManyField(GrowthStage, related_name='plants', blank=True)

    tasks = models.ManyToManyField(Plant_specific_task, related_name='plants', blank=True)

    min_growth_time = models.DurationField(default=timedelta(days=1))

    max_growth_time = models.DurationField(default=timedelta(days=2))



    def __str__(self):

        return self.name



class UserTask(models.Model):

    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='tasks')


    description = models.TextField(blank=True, null=True)

    frequency = models.DurationField(default=timedelta(days=1))

    start_date = models.DateField(default=timezone.now())



    def save(self, *args, **kwargs):

        if not self.pk:
            
            super().save(*args, **kwargs)
            self.garden.user_tasks.add(self)

            self.garden.save()




    def __str__(self):

        return f"{self.user.username}'s Task - {self.description}"





"""I TOOK THIS CODE OUT BECAUSE... the models have fields which connect them now. I think that is a better way to do this and the 

@ receiver function is for when models have fields that don't relate. It lets another model recognize that a change took place.

I want to keep this in here incase I want to reference it later. 


@receiver(post_save, sender=Task)


@receiver(post_save, sender=UserTask)


def update_garden_tasks(sender, instance, **kwargs):

    if isinstance(instance, (Task, UserTask)):

        if hasattr(instance, 'garden'):

            instance.garden.tasks.add(instance)

            instance.garden.save()

        elif hasattr(instance, 'plant'):

                instance.plant.tasks.add(instance)

                instance.plant.save()


"""


"""
GONNA NEED THIS LATER:

This segment of code updates the titles within my notecard app. 
It reorders them so if you delete something everything renumbers
so a number isn't missing.



    def save(self, *args, **kwargs):

        if not self.pk:  # Only update on new note creation

            note_count_in_deck = Note.objects.filter(deck=self.deck).count() + 1

            self.title = f"Note {note_count_in_deck} of {self.deck.title}"

        super().save(*args, **kwargs)



    def __str__(self):

        return self.title



@receiver(pre_delete, sender=Note)

def update_note_titles_on_delete(sender, instance, **kwargs):

    remaining_notes = Note.objects.filter(deck=instance.deck).exclude(pk=instance.pk).order_by('pk')

    for index, note in enumerate(remaining_notes, start=1):

        note.title = f"Note {index} of {note.deck.title}"

        note.save()



"""

