from django.test import TestCase
from utils.testing.test import preserve_MEDIA, return_preserved_MEDIA, get_testing_img_path
from .models import Account
from django.db import transaction
from django.db.utils import IntegrityError
from django.conf import settings
from django.core.files import File
from PIL import Image, ImageChops
import os


class AccountTestCase(TestCase):

    def setUp(self) -> None:
        self.normal_user = Account.objects.create_user(
            username='normal_user',
            email='normal@mail.com',
            password='1234'
        )
        self.MEDIA_preserved = preserve_MEDIA()
        self.MEDIA_for_tests = settings.MEDIA_ROOT
        self.avatars_location = os.path.join(self.MEDIA_for_tests, 'avatars')
        self.avatar1_path = get_testing_img_path('test_avatar.png')
        self.avatar2_path = get_testing_img_path('test_avatar2.png')

    def tearDown(self) -> None:
        return_preserved_MEDIA(self.MEDIA_for_tests, self.MEDIA_preserved)

    def test_instance(self):
        user = Account.objects.get(username='normal_user')
        assert user == self.normal_user

    def test_requiered_fields(self):
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Account.objects.create_user(email=None, username='u1', password='123')
        with self.assertRaises(ValueError):
            with transaction.atomic():
                Account.objects.create_user(email='e@m.com', username='u1', password=None)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Account.objects.create_user(email='e@m.com', username=None, password='123')

    def test_unique_fields(self):
        with self.assertRaises(IntegrityError, msg='emails must be unique'):
            with transaction.atomic():
                Account.objects.create_user(email='normal@mail.com', username='u1', password='123')

        with self.assertRaises(IntegrityError, msg='usernames must be unique'):
            with transaction.atomic():
                Account.objects.create_user(email='e2@m.com', username='normal_user', password='123')

    def test_avatar_field(self):
        # new account without a specified avatar shouldn't have an avatar stored in database,
        # default avatar's data shouldn't be dublicated
        self.assertRaises(ValueError, lambda: self.normal_user.avatar.url)

        default_avatar_url = self.normal_user.avatar_url
        assert default_avatar_url

        assign_avatar(self.normal_user, self.avatar1_path)
        assert self.normal_user.avatar_url != default_avatar_url

    def test_one_user_has_only_one_avatar(self):
        assert count_files(self.avatars_location) == 0

        avatar1 = Image.open(self.avatar1_path)
        avatar2 = Image.open(self.avatar2_path)
        assert not images_are_equal(avatar1, avatar2)

        assign_avatar(self.normal_user, self.avatar1_path)
        assert images_are_equal(avatar1, Image.open(self.normal_user.avatar))

        assign_avatar(self.normal_user, self.avatar2_path)
        assert images_are_equal(avatar2, Image.open(self.normal_user.avatar))

        assert count_files(self.avatars_location) == 1

    def test_different_users_avatars_dont_overlap(self):
        assert count_files(self.avatars_location) == 0

        assign_avatar(self.normal_user, self.avatar1_path)
        user2 = Account.objects.create(email='e@m.com', username='u2', password='123')
        assign_avatar(user2, self.avatar2_path)

        assert count_files(self.avatars_location) == 2


def assign_avatar(user, img_path, name='test_avatar'):
    with open(img_path, 'rb') as avatar:
        user.avatar.save(
            name,
            File(avatar)
        )
        user.save()


def images_are_equal(im1, im2):
    return ImageChops.difference(im1, im2).getbbox() is None


def count_files(path):
    try:
        return len(os.listdir(path))
    except FileNotFoundError:
        return 0
