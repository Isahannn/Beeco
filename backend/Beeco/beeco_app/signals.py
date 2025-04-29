from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post, GroupMember

@receiver(post_save,sender=Post)
def add_created_as_admin(sender,instance,created,**kwargs):
    if created and instance.user:
        if not GroupMember.objects.filter(post=instance, user=instance.user).exists():
            GroupMember.objects.create(
                post=instance,
                user=instance.user,
                role=GroupMember.Role.ADMIN
            )


