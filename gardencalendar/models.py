import secrets

import string

from django.db import models

from django.utils import timezone

from datetime import timedelta

from django.db.models.signals import post_save

from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser



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



class Task(models.Model):

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

    plants = models.ManyToManyField('Plant', related_name='gardens', blank=True)

    user_tasks = models.ManyToManyField('UserTask', related_name='gardens', blank=True)

    general_tasks = models.ManyToManyField(GeneralTask, related_name='gardens', blank=True)



    def save(self, *args, **kwargs):

        if not self.pk:

            garden_count = Garden.objects.filter(user=self.user).count() + 1

            self.name = f"Garden {garden_count} - {self.name}"

        super().save(*args, **kwargs)



    def __str__(self):

        return self.name



class GrowthStage(models.Model):

    plant = models.ForeignKey('Plant', on_delete=models.CASCADE, related_name='plant_growth_stages')

    description = models.TextField()

    growing_time = models.DurationField(default=timedelta(days=1))

    
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

    tasks = models.ManyToManyField(Task, related_name='plants', blank=True)



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

