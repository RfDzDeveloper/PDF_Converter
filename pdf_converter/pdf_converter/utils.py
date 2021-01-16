from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from shutil import make_archive
from xhtml2pdf import pisa
from io import BytesIO
from PIL import Image
import zipfile
import os

#Extension metods

def image_to_pdf(file_list):    
    pdf_list = []
    new_file_name_list = []
    save_file_path = get_dir_path()
    for item in file_list:
        image = Image.open(item)
        pdf = image.convert('RGB')
        new_file_name = change_file_name_to_save(item.name)
        new_file_name_list.append(new_file_name)
        pdf.save(save_file_path + new_file_name)
        pdf_list.append(pdf)
    return pdf_list, new_file_name_list

def change_file_name_to_save(file_name):
    temp = file_name.split(".")
    if temp[1] == "jpg":        
        temp[1] = "pdf"        
        new_file_name = '.'.join(temp)
        return new_file_name
        
    elif temp[1] == "png":        
        temp[1] = "pdf"        
        new_file_name = '.'.join(temp)
        return new_file_name
    else:
        return False
    
def remove_file_by_name(file_name):
    save_file_path = get_dir_path()
    path_to_file = save_file_path + file_name
    if os.path.exists(path_to_file):
        os.remove(path_to_file)
        return True
    else:
        return False
def remove_file_by_path(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False

def remove_all_files_from_dir(dir_path):
    try:
        files_list = get_list_files(dir_path)
        for item in files_list:
            print(item)
            remove_file_by_name(item)
        return True
    except Exception:
        return False

#Here get pdf dir path
def get_dir_path():    
    path_list = settings.MEDIA_ROOT
    save_file_path = path_list[0] + '/'
    return save_file_path

def make_tar(): 
    try:   
        dir_path = get_dir_path()            
        file_path = make_archive(
            base_name = dir_path + "/Converted_dir",
            format = "tar",
            root_dir = dir_path,  
        )                  
        return file_path
    except Exception:
        return False


def make_zip(): 
    try:   
        dir_path = get_dir_path()             
        file_path = make_archive(
            base_name = dir_path + "/Converted_dir",
            format = "zip",
            root_dir = dir_path,  
        )                  
        return file_path
    except Exception:
        return False

def make_zip_using_zipfile():
    try:
        dir_path = get_dir_path()
        file_list = get_list_files(dir_path)
        file = zipfile.ZipFile(
            file = dir_path + "Converted_dir.zip",
            mode = 'w',
            compression = zipfile.ZIP_DEFLATED,
        )
        print(file.filename)
        for item in file_list:
            file.write(dir_path + item)
        return file.filename
    except:
        return False

def get_list_files(dir_path):
    files_list = os.listdir(dir_path)
    return files_list
