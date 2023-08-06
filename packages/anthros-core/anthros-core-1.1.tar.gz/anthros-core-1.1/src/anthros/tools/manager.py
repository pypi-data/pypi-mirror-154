from tools import simple
import os, shutil, sys

def remove(path: 'str'):
    r'''Удаляет файл или папку по переданному раположению'''
    if simple.file_exist(path) == 'folder':
        return shutil.rmtree(path)
    elif simple.file_exist(path) == 'file':
        return shutil.os.remove(path)
    else:
        raise Exception('file or folder not exist')

def open_file(link, stream: 'boolean' = False):
    r'''Возвращает данные из файла в виде строки
    *При stream = True вернёт io.stream объект'''
    pos = sys.path[0]
    try: file = open(link, 'r', encoding='utf-8')
    except: file = open(pos + '\\' + link, 'r', encoding='utf-8')

    if stream: return file
    file = file.read()
    if file[0] == '\ufeff':
        file = file[1:]
    return file


def save_file(link, fill, rewrite = False):
    r'''Записывает файл по указанному пути с переданными данными
    *Если переменная rewrite = True перезапишет существующий файл'''
    pos = sys.path[0]
    if rewrite:
        w = 'w'
    else:
        w = 'x'

    try:
        file = open(link, w, encoding='utf-8')
    except:
        file = open(pos + '\\' + link, w, encoding='utf-8')
    file.write(fill)
    file.close()


def pickling(link: (str, 'link'), fill):
    pickle.dump(fill, open(link, 'bw'))


def unpickling(link: (str, 'link')):
    try:
        file = pickle.load(open(link, 'br'))
    except:
        pickle.dump(None, open(link, 'bw'))
        file = pickle.load(open(link, 'br'))
    return file