from django.conf import settings
import shutil
import os


def preserve_MEDIA():
    preserved_MEDIA = settings.MEDIA_ROOT + '_preserved'
    if os.path.exists(settings.MEDIA_ROOT):
        os.rename(settings.MEDIA_ROOT, preserved_MEDIA)
    return preserved_MEDIA


def return_preserved_MEDIA(testing_MEDIA, preserved_MEDIA):
    try:
        shutil.rmtree(testing_MEDIA)
    except FileNotFoundError:
        pass
    finally:
        if os.path.exists(preserved_MEDIA):
            os.rename(preserved_MEDIA, settings.MEDIA_ROOT)


def get_testing_img_path(img_name):
    return os.path.join(settings.BASE_DIR, 'utils', 'testing', 'img', img_name)
