from django.test import TestCase
from django.test.utils import override_settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import SuspiciousFileOperation
from mixer.backend.django import mixer
from django.db.models.deletion import ProtectedError
from django.conf import settings
from utils.testing.test import get_testing_img_path
from . import models
import tempfile
import os


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class BlogPostTestCase(TestCase):

    def setUp(self):
        self.category = mixer.blend(models.Category)
        self.post = mixer.blend(models.BlogPost, category=self.category, slug=mixer.SKIP, thumbnail=mixer.RANDOM)

    def test_delete_category_w_posts(self):
        with self.assertRaises(ProtectedError, msg="You shouldn't be able to delete a category with posts in it"):
            self.category.delete()

    def test_slug(self):
        title = 'Django 3.0 TDD in a nutshell...'
        self.post.title = title
        self.post.save()
        assert self.post.slug == 'django-30-tdd-in-a-nutshell', 'Slug should be attached automatically'

    def test_thumbnail(self):
        assert self.post.thumbnail_url == self.post.thumbnail.url
        self.post.thumbnail.delete()
        self.post.save()
        assert self.post.thumbnail_url == self.category.thumbnail.url


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class IllustrationTestCase(TestCase):

    def mock_upload(self, filename):
        with open(get_testing_img_path(filename), 'rb') as img:
            uploaded_img = UploadedFile(img, 'test_img.png')
            return models.Illustration.upload_illustration(uploaded_img)

    def test_upload_illustration(self):
        img_url = self.mock_upload('test_avatar.png')
        storage = FileSystemStorage()
        img_name = img_url[len(settings.MEDIA_URL):]
        assert storage.exists(img_name), 'File must be uploaded into MEDIA_ROOT directory'

    def test_assign_illustration(self):
        post = mixer.blend(models.BlogPost)
        img_url = self.mock_upload('test_avatar.png')
        illustration = models.Illustration.assign_illustration(img_url, post)
        assert illustration == post.illustrations.first(), 'Illustration must be in the database'

        storage = FileSystemStorage()
        img_filename = os.path.basename(illustration.picture.name)
        assert not (storage.exists(f'{settings.MEDIA_URL}tmp/{img_filename}')), 'Image must be moved from tmp folder after saving'

    def test_steal_illustration(self):
        post = mixer.blend(models.BlogPost)
        post2 = mixer.blend(models.BlogPost)

        img_url = self.mock_upload('test_avatar.png')
        illustration = models.Illustration.assign_illustration(img_url, post)
        with self.assertRaises(SuspiciousFileOperation):
            models.Illustration.assign_illustration(illustration.picture.url, post2)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class CleanupTestCase(TestCase):

    def test_category_cleanup(self):
        category = mixer.blend(models.Category)
        thumbnail = category.thumbnail.name
        self.assertMediaCleanedUp(category, thumbnail)

    def test_blogpost_cleanup(self):
        post = mixer.blend(models.BlogPost, thumbnail=mixer.RANDOM)
        thumbnail = post.thumbnail.name
        self.assertMediaCleanedUp(post, thumbnail)

    def test_illustration_cleanup(self):
        illustration = mixer.blend(models.Illustration)
        pic = illustration.picture.name
        self.assertMediaCleanedUp(illustration, pic)

    def test_illustrations_cleanup_when_post_deleted(self):
        post = mixer.blend(models.BlogPost, thumbnail=mixer.RANDOM)
        illustrations = mixer.cycle().blend(models.Illustration, post=post)
        img_stornames = [illustration.picture.name for illustration in illustrations]
        img_stornames.append(post.thumbnail.name)
        self.assertMediaCleanedUp(post, *img_stornames)

    def assertMediaCleanedUp(self, instance, *files_stornames, msg_case_not_created=None, msg_case_not_deleted=None):
        storage = FileSystemStorage()
        assert all(storage.exists(file) for file in files_stornames), msg_case_not_created or 'Files must be created and still exist'
        instance.delete()
        assert all(not storage.exists(file) for file in files_stornames), msg_case_not_deleted or f'Media dir must be cleaned up after deletion of the {instance._meta.verbose_name}'
