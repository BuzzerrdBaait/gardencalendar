import secrets
import string
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models



from django.utils import timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver



"""
I will go back and put some foreign keys into the user profile. This is just a base user model extended and we need to migrate first then we can edit it how we want.

"""


class User_Profile(AbstractUser):
    
    email= models.CharField(max_length=40,blank=True,null=True, unique=True)

    authentication_key = models.CharField(max_length=50, unique=True)

    is_verified = models.CharField(max_length=1, default='N')

    user_image = models.ImageField(upload_to='user_images/', blank=True, null=True)

    user_library = models.CharField(max_length=255, default='', blank=True)



    """
    AUTHENTICATION LINK CODE
    """

    def generate_unique_link(self):

        link = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))

        link = link.replace('\\', str(secrets.randbelow(1000)))

        link = link.replace('/', str(secrets.randbelow(1000)))

        link = link.replace("'", str(secrets.randbelow(1000)))

        link = link.replace('"', str(secrets.randbelow(1000)))

        return link
    

    authentication_link = models.CharField(max_length=50, blank=True, null=True)


    def save(self, *args, **kwargs):

        if not self.authentication_key:

            self.authentication_key = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(30))


        if not self.authentication_link:

            self.authentication_link = self.generate_unique_link()


        super().save(*args, **kwargs)






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

