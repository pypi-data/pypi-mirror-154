import time

def time_record(func, mode='t'):
    def wrapping(*args, **kwargs):
        start = time.time()
        tmp = func(*args, **kwargs)
        str1 = f'Function: {func.__name__} 耗时: {time.time() - start} 秒'
        if mode == 't':
            print('-' * (len(str1) + 4))
            print('|' + str1 + '|')
            print('-' * (len(str1) + 4))
        return tmp
    return wrapping

import os
def get_all_txt(root):
    g = os.walk(root)
    for path, dir_list, file_list in g:
        img_list = [item for item in file_list if item.lower().endswith(".txt")]
    return img_list

def get_all_img(root):
    g = os.walk(root)
    img_end = ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')
    for path, dir_list, file_list in g:
        img_list = [item for item in file_list if item.lower().endswith(img_end)]
    return img_list

import pickle
def save_file_data(text, save_file):
    f = open(save_file, 'wb')
    pickle.dump(text, f)
    f.close()
