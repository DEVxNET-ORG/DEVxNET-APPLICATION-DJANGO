from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_group(sender, instance, created, **kwargs):
    if created:
        if instance.is_admin():
            group, _ = Group.objects.get_or_create(name='Admins')
            instance.groups.add(group)
        elif instance.is_manager():
            group, _ = Group.objects.get_or_create(name='Managers')
            instance.groups.add(group)
        elif instance.is_employee():
            group, _ = Group.objects.get_or_create(name='Employees')
            instance.groups.add(group)
