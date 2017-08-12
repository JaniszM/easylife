import os
import re
import logging
import exifread
import shutil
import platform
from datetime import datetime
from shutil import copy2

from easylife import get_logger
from easylife.photo_organizer import PHOTO_EXTENSIONS, VIDEO_EXTENSIONS, METADATA_EXTENSIONS, PATTERN, \
    DEFAULT_COPY_DIR, FILE_DATE_FORMAT

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
    if date is None:
        date = os.path.join(destination, DEFAULT_COPY_DIR, filename)
        LOG.error("Cannot describe creation date of the %s. Setting it to %s", filename, date)
        return date
    else:
        return os.path.join(destination,
                            template.replace("YYYY", str(date.year)).replace("MONTH", str(date.strftime("%B"))).
                            replace("MM", str(date.month)).replace("DD", str(date.day)).replace("NAME", filename))


def build_new_photo_destination(template, src, destination):
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
    try:
        exif_info = str(exif_info['EXIF DateTimeOriginal'])
        exif_info = datetime.strptime(exif_info, FILE_DATE_FORMAT)
        return template_to_path(template, destination, os.path.basename(src), exif_info)
    except KeyError:
        LOG.info('Missing exif DateTimeOriginal tag for %s. Reading date from system file property...', src)
        return build_new_file_destination(template, src, destination)


def build_new_file_destination(template, src, destination):
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

    if platform.system() == 'Windows':
        date = os.path.getctime(src)
    else:
        stat = os.stat(src)
        try:
            date = stat.st_ctime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            date = stat.st_mtime

    date = datetime.fromtimestamp(int(date))

    return template_to_path(template, destination, os.path.basename(src), date)


def organize_photos(source_dir, destination, template, overwrite_existing=False, remove_source=False):
    """
    Organises target directory by searching all image files and coping them into destination directory
    according to given template and read image EXIF data.

    :param template: template to apply on the copied path and name of the photo.
    :type template: str
    :param source_dir: Source path of the photos to organize.
    :type source_dir: str
    :param destination: Target destination dir where file should go.
    :type destination: str
    :param remove_source: (Optional) If set to True will remove source directory.
    :type remove_source: bool
    :param overwrite_existing: (Optional) If set to True will will overwrite existing file in destination directory.
    :type overwrite_existing: bool
    """

    if not os.path.exists(source_dir):
        raise Exception("Source directory does not exists: {0}".format(source_dir))

    copied_count = 0

    # read whole directory and subdirs
    for dirname, dirnames, filenames in os.walk(source_dir):

        # skip it to prevent stupid things
        if destination in dirname:
            LOG.warn("Destination dir is a child of target dir. Skipping %s.", dirname)
            continue

        for filename in filenames:
            try:
                extension = filename[filename.index(".") + 1:].lower()
                create = False
                file_src = os.path.join(dirname, filename)

                # if this is image type file try to process it
                if extension in PHOTO_EXTENSIONS:
                    file_dest = build_new_photo_destination(template, file_src, destination)
                    create = True
                elif extension in VIDEO_EXTENSIONS or extension in METADATA_EXTENSIONS:
                    file_dest = build_new_file_destination(template, file_src, destination)
                    create = True

                if create:
                    # create all required subdirs to target dir
                    if not os.path.exists(os.path.dirname(file_dest)):
                        os.makedirs(os.path.dirname(file_dest))

                    if overwrite_existing is True or (overwrite_existing is False and os.path.isfile(file_dest) is False):
                        LOG.info("Coping %s to %s.", file_src, file_dest)
                        copy2(file_src, file_dest)
                        copied_count += 1
                    else:
                        LOG.info("File exists, skipping %s.", file_dest)

            except ValueError:
                LOG.debug("File %s has no extension, skipping.", filename)
            except Exception as err:
                LOG.exception(err)

    LOG.info("%d files copied.", copied_count)

    # Removes whole source directory
    if remove_source is True:
        LOG.info("Removing source directory!")
        shutil.rmtree(source_dir)
