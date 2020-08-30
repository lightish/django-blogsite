from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousFileOperation

from utils.fields import MovableImageField


def upload_illustration(instance, filename):
    return f'blog/posts/{instance.post.id}/{filename}'


def upload_thumbnail(instance, filename):
    return f'blog/posts/{instance.id}/thumb'


class Category(models.Model):
    name = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='blog/cat/')


class BlogPost(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0               # author is still editing the post
        AWAITING_APPROVAL = 1   # post is waiting editor's approval
        PUBLISHED = 2           # the only valid status for posts to be shown
        # to normal users
        DISABLED = 3            # staff or editors disabled post to address
        # some issue

    title = models.CharField(max_length=200)
    content = models.TextField(max_length=50_000)
    category = models.ForeignKey(Category,
                                 on_delete=models.PROTECT,
                                 related_name='posts')
    thumbnail = models.ImageField(upload_to=upload_thumbnail,
                                  null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    created_on = models.DateField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='posts_made',
                               on_delete=models.CASCADE)
    editor = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name='posts_edited',
                               on_delete=models.SET_NULL,
                               limit_choices_to={'is_staff': True},
                               null=True, blank=True)
    status = models.IntegerField(choices=Status.choices)
    view_count = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        try:
            return self.thumbnail.url
        except ValueError:
            return self.category.thumbnail.url


class Illustration(models.Model):
    """
    A picture inside a post.
    """
    post = models.ForeignKey(BlogPost,
                             on_delete=models.CASCADE,
                             related_name='illustrations')
    picture = MovableImageField(upload_to=upload_illustration)

    storage = FileSystemStorage()

    def __str__(self):
        return self.picture.name

    @classmethod
    def upload_illustration(cls, image):
        """
        Upload a picture in media/tmp directory for previewing in text editor.
        upload_illustration doesn't create an Illustration instance and doesn't
        make a database entry.
        :param image: UploadedFile instance
        :return: relative url for previewing
        """
        file = cls.storage.save(f'tmp/{image.name}', image)
        return cls.storage.url(file)

    @staticmethod
    def assign_illustration(img_url, post, save=True):
        """
        Create an Illustration instance out of preview picture
        in media/tmp directory.
        :param img_url: relative url for an image in media/tmp directory
        :param post: BlogPost which the image is illustrating
        :param save: if True saves instance to database
        :return: created Illustration instance
        """
        if not img_url.startswith(f'{settings.MEDIA_URL}tmp/'):
            raise SuspiciousFileOperation(f'Invalid url: {img_url}')

        illustration = Illustration(post=post)
        illustration.picture.save_existing(img_url, save)
        return illustration
