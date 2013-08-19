import re
import subprocess
import os
import shutil
import Image
import zipfile

from django.conf import settings


def title_to_filename(title):
    title = title.lower()
    title = re.sub(r' /.*', '', title)
    title = re.sub(r'[^\w -]', '', title)
    title = re.sub(r' +', '-', title)
    return title


def zip(filename, files_to_zip):
    if os.path.exists(filename):
        zip_args = ['zip', '-j', '-u', filename]
    else:
        zip_args = ['zip', '-j', filename]
    zip_args.extend(files_to_zip)
    zip = subprocess.Popen(zip_args)
    zip.communicate()

    if os.path.exists(filename):
        existing_files = zipfile.ZipFile(filename).namelist()
        existing_files = [os.path.join(os.path.dirname(filename), f) for f in existing_files]
        files_to_delete = list(set(existing_files) - set(files_to_zip))
        if files_to_delete:
            zip_args = ['zip', '-j', '-d', filename] + files_to_delete
            zip = subprocess.Popen(zip_args)
            zip.communicate()


def create_thumbnails(folder_path, max_width, max_height, thumb_folder_name='thumbs'):
    folder_path = os.path.join(settings.STATIC_ROOT, 'images', folder_path)
    images = get_files(folder_path)
    thumb_path = os.path.join(folder_path, thumb_folder_name)
    if os.path.exists(thumb_path):
        shutil.rmtree(thumb_path)
    os.mkdir(thumb_path)
    for image in images:
        filename = os.path.splitext(os.path.basename(image))[0]
        try:
            image = Image.open(image)
        except:
            continue
        image.thumbnail((max_width, max_height), Image.ANTIALIAS)
        image.save(os.path.join(thumb_path, '%s.jpg' % filename), quality=100)


def get_exif_title(image_path):
    exif_data = Image.open(image_path)._getexif() or {}
    return exif_data.get(270, '') # 270 = ImageDescription


def get_files(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]


def get_dirs(folder_path):
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
