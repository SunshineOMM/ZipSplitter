import time
import random
import patoolib
import os
import glob
from zipfile import ZipFile
import shutil
import threading

# подготовка пути к временной дирректории
class back_thread (threading.Thread):
   def __init__(self,print_f,FILE_NAME_OLD_ARC,NAME_SEP_DIR,BATCH,START):
       threading.Thread.__init__(self)
       self.print_f=print_f
       self.FILE_NAME_OLD_ARC=FILE_NAME_OLD_ARC
       self.NAME_SEP_DIR=NAME_SEP_DIR
       self.BATCH=BATCH
       self.START=START
   def run(self):
       self.print_f(f"====================START====================!")
       main_prosess(self.print_f,self.FILE_NAME_OLD_ARC,self.NAME_SEP_DIR,self.BATCH,self.START)
       self.print_f(f"====================END====================!")

def create_temp_dir(zips_path,print_f):
    temp_path = os.path.join(zips_path,f"{random.randint(4352,432724357)}tempdir")

    try:
        os.mkdir(temp_path)
    except OSError:
        print_f(f"Создать временную директорию {temp_path} не удалось")
        raise
    else:
        print_f(f"Успешно создана директория {temp_path}")
        return temp_path

def unzip_in_tmp_dir(rar_path,zips_path,print_f):
    temp_path=create_temp_dir(zips_path,print_f)
    try:
        if rar_path[-3:]=="rar":
            pass
            patoolib.extract_archive(rar_path, outdir=temp_path)
        else:
            with ZipFile(rar_path) as f:
                pass
                f.extractall(temp_path)
    except:
        print_f("Во время разархивирования произошла ошибка!")
        raise
    else:
        print_f("Разархивирование произошло успешно!")
        return temp_path

def splitting_filenames_by_batchs(START,BATCH,file_names):
    i = START
    files_name_for_bach = []
    while i < len(file_names):
        if i + BATCH >= len(file_names):
            files_name_for_bach.append(file_names[i:len(file_names)])
            i += BATCH
        else:
            files_name_for_bach.append(file_names[i:i + BATCH])
            i += BATCH
    return files_name_for_bach

def group_files_and_zip(files_name_for_bach,zips_path,print_f):
    try:
        for ind,batch in enumerate(files_name_for_bach):
             print_f(f"Архивирование {ind+1}/{len(files_name_for_bach)}")
             with ZipFile(f"{zips_path}{ind}.zip","w") as f:
                 for file_name in batch:
                     f.write(file_name,file_name[max(file_name.rfind("/"),file_name.rfind("\\")):])

    except:
        print_f("Во время архивирования произошла ошибка!")
        raise
    else:
        print_f("Архивирование прошло успешно!")

def main_prosess(print_f,FILE_NAME_OLD_ARC,NAME_SEP_DIR,BATCH,START):
    print_f("Разархивация файлов...")
    temp_path = unzip_in_tmp_dir(FILE_NAME_OLD_ARC, NAME_SEP_DIR,print_f)

    ## Получаем список архивируемых имён файлов
    file_names = glob.glob(os.path.join(temp_path, '*.xcf'))
    print_f(f"Find {len(file_names)} objects!")
    start_time = time.time()

    ## Формируем разбиение имён по группам размера BATCH
    files_name_for_bach = splitting_filenames_by_batchs(START, BATCH, file_names)
    print_f(f"Разбиение произойдёт на {len(files_name_for_bach)} архива(ов)!")
    ## В указанную директорию архивируем файлы из files_name_for_bach
    group_files_and_zip(files_name_for_bach, NAME_SEP_DIR,print_f)

    # удаляем временные файлы
    print_f("Удаление временных файлов...")
    shutil.rmtree(temp_path)

    all_time = time.time() - start_time
    print_f(f"Успех! Программа работала: {int(all_time // 3600)}:{int((all_time % 3600) // 60)}:{int((all_time % 3600) % 60)}.\n"
                    f" Теперь можете её закрыть!")


if __name__=="__main__":
    FILE_NAME_OLD_ARC = "../no_markup/output.rar"
    NAME_SEP_DIR = "../no_markup/slices_zip/"
    # Выбираем начиная со START файлов от начала, по BATCH файлов нужного расширения и формируем из них архивы zip
    START=1
    BATCH=40
    main_prosess(print_f=print)