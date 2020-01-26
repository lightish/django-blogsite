from django.db.models.fields.files import ImageFieldFile, ImageField
from utils.storage import parse_storage_name, parse_filename
import shutil
import os


class MovableImageFieldFile(ImageFieldFile):

    def save_existing(self, url, save=True):
        storage_name = parse_storage_name(url)
        file_path = self.storage.path(storage_name)
        if not self.storage.exists(file_path):
            raise ValueError("Image doesn't exist")

        filename = parse_filename(storage_name)
        new_name = self.field.generate_filename(self.instance, filename)
        self.name = self.storage.get_available_name(new_name, max_length=self.field.max_length)
        new_path = self.storage.path(self.name)
        new_path_dir = os.path.dirname(new_path)
        if not os.path.exists(new_path_dir):
            os.makedirs(new_path_dir)
        shutil.move(file_path, new_path)

        setattr(self.instance, self.field.name, self.name)
        self._committed = True

        if save:
            self.instance.save()
    save_existing.alters_data = True


class MovableImageField(ImageField):
    attr_class = MovableImageFieldFile





