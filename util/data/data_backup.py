import os
import zipfile
from datetime import datetime as dt
from os import listdir
from os import path
from os.path import isfile, join

from util.logger import Logger

data_path = "data/"
backups_folder_name = "backups"
zip_name = "backups.zip"


def backup_databases(always_run=True):
    subfolder_name = get_subfolder_name()

    if path.exists(f"{backups_folder_name}/{subfolder_name}/{zip_name}") and not always_run:
        return

    if not os.path.exists(f"{backups_folder_name}/{subfolder_name}"):
        os.makedirs(f"{backups_folder_name}/{subfolder_name}")

    loczip = f"{backups_folder_name}/{subfolder_name}/{zip_name}"
    zip = zipfile.ZipFile(loczip, "w", zipfile.ZIP_DEFLATED)

    only_files = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    for file in only_files:
        backup_file(zip, f"{data_path}{file}")

    Logger.info(f"Backed up {len(only_files)} files to {backups_folder_name}/{subfolder_name}/{zip_name}")


def get_subfolder_name():
    return str(dt.now().strftime('%m%d%y'))


def backup_file(zip, filename: str):

    folder_name = backups_folder_name
    subfolder_name = get_subfolder_name()
    # backup_loc = f"{folder_name}/{subfolder_name}/"
    # backup_name = f"{backup_loc}/{filename}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    if not os.path.exists(f"{folder_name}/{subfolder_name}"):
        os.makedirs(f"{folder_name}/{subfolder_name}")

    zip.write(filename, os.path.basename(filename))

    # Logger.info(f"Backed up {filename} to {backup_loc}{zip_name}")
