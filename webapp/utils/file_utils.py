#!/usr/bin/python3
import os
import shutil
from werkzeug.utils import secure_filename

def save_file(file, upload_folder):
    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def move_file(source, destination):
    shutil.move(source, destination)

def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()