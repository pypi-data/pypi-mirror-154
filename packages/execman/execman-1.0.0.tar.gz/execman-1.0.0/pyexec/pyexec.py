import os
from datetime import datetime


def pyexec(exclude, commands):
    try:
        exclude += ['venv', '.idea', '.git', '__pycache__', 'pyexec']
        main_folder = [str(name) for name in os.listdir(".") if
                       os.path.isdir(name) and name not in exclude]
        for first_level_folder in main_folder:
            os.chdir(f'./{first_level_folder}')
            sub_folder = [name for name in os.listdir(f".") if os.path.isdir(name)]
            for second_level_folder in sub_folder:
                os.chdir(f'./{second_level_folder}')
                for command in commands:
                    os.system(command)
                print(datetime.now(), f' :: {second_level_folder} is execute')
                os.chdir('../')
            os.chdir('../')
        print(datetime.now(), ':: finished')
    except Exception as error:
        print(error)
