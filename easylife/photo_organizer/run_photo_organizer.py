import os
import re
import logging
import exifread
from datetime import datetime
from shutil import copyfile

from easylife import get_logger
from easylife.photo_organizer import PHOTO_EXTENSIONS, PATTERN

LOG = get_logger(__name__, log_level=logging.INFO)


def validate_template(template):
    """
    Validates if template match to pattern.
    :param template: A template string.
    :type template: str
    """
    pattern = re.compile(PATTERN)
    if not pattern.match(template):
        raise Exception("Template '{0}' do not match to pattern '{1}'.".format(template, PATTERN))


def template_to_path(template, destination, filename, date):
    """
    Basing on given template creates new path to the file.

    :param template: template.
    :type template: str
    :param filename: filename of the photo including extension.
    :type filename: str
    :param destination: Target destination dir where file should go.
    :type destination: str
    :param date: date and time when photo was captured.
    :type date: datetime
    :return: Return destination of the photo.
    :rtype: str
    """
    return os.path.join(destination,
                        template.replace("RRRR", str(date.year)).replace("MM", str(date.month)).replace("DD", str(
                            date.day)).replace("NAME", filename))


def build_new_destination(template, src, destination):
    """
    Builds new path and filename for given photo. Basing on given template and photo EXIF DateTimeOriginal field.

    :param template: template.
    :type template: str
    :param src: Source path of the file, including filename.
    :type src: str
    :param destination: Target destination dir where file should go.
    :type destination: str
    :return: new destination path and name.
    :rtype: str
    """
    # open image file for reading (binary mode) and get exif tags
    f = open(src, 'rb')
    exif_info = exifread.process_file(f)
    f.close()

    # get proper field and convert to datetime
    exif_info = str(exif_info['EXIF DateTimeOriginal'])
    exif_info = datetime.strptime(exif_info, '%Y:%m:%d %H:%M:%S')

    return template_to_path(template, destination, os.path.basename(src), exif_info)


def organize_photos(source_dir, destination, template, override_existing=False, remove_org=False):
    """
    Organises target directory by searching all image files and coping them into destination directory
    according to given template and read image EXIF data.

    :param template: template to apply on the copied path and name of the photo.
    :type template: str
    :param source_dir: Source path of the photos to organize.
    :type source_dir: str
    :param destination: Target destination dir where file should go.
    :type destination: str
    :param remove_org: (Optional) If set to True will remove source directory.
    :type remove_org: bool
    :param override_existing: (Optional) If set to True will will overwrite existing file in destination directory.
    :type override_existing: bool
    """

    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exists: {0}".format(source_dir))

    # read whole directory and subdirs
    for dirname, dirnames, filenames in os.walk(source_dir):

        # skip it to prevent stupid things
        if destination in dirname:
            LOG.warn("Destination dir is a child of target dir. Skipping %s.", dirname)
            continue

        for filename in filenames:
            try:
                # if this is image type file try to process it
                if filename[filename.index(".") + 1:] in PHOTO_EXTENSIONS:
                    file_src = os.path.join(dirname, filename)
                    file_dest = build_new_destination(template, file_src, destination)

                    # create all required subdirs to target dir
                    if not os.path.exists(os.path.dirname(file_dest)):
                        os.makedirs(os.path.dirname(file_dest))

                    if override_existing is True or (override_existing is False and os.path.isfile(file_dest) is False):
                        LOG.info("Coping %s to %s.", file_src, file_dest)
                        copyfile(file_src, file_dest)
                    else:
                        LOG.info("File exists, skipping %s.", file_dest)

            except ValueError:
                LOG.debug("File %s has no extension, skipping.", filename)

    # Removes whole source directory
    if remove_org is True:
        LOG.info("Removing source directory!")
        os.rmdir(source_dir)
