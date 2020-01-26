from django.db.models.signals import post_save, post_delete, post_init, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Category, BlogPost, Illustration


def backup_thumbnail(sender, instance, **kwargs):
    instance._thumbnail_bac = instance.thumbnail


def delete_old_thumbnail_if_changed(sender, instance, **kwargs):
    if hasattr(instance, '_thumbnail_bac'):
        if instance._thumbnail_bac != instance.thumbnail:
            instance._thumbnail_bac.delete(False)


post_init.connect(backup_thumbnail, sender=Category, dispatch_uid=0)
post_save.connect(delete_old_thumbnail_if_changed, sender=Category, dispatch_uid=0)
post_init.connect(backup_thumbnail, sender=BlogPost, dispatch_uid=0)
post_save.connect(delete_old_thumbnail_if_changed, sender=BlogPost, dispatch_uid=0)


def delete_thumbnail(sender, instance, **kwargs):
    instance.thumbnail.delete(False)


post_delete.connect(delete_thumbnail, sender=Category, dispatch_uid=0)
post_delete.connect(delete_thumbnail, sender=BlogPost, dispatch_uid=0)


@receiver(pre_save, sender=BlogPost)
def attach_slug(sender, instance, **kwargs):
    # TODO (?) tag instance with it's old slug
    instance.slug = slugify(instance.title)


@receiver(post_delete, sender=Illustration)
def delete_picture(sender, instance, **kwargs):
    instance.picture.delete(False)

