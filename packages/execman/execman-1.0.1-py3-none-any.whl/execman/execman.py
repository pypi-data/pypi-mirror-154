import os
from datetime import datetime


def execman(commands):
    try:
        lines = []
        if os.path.isfile('./.execmanignore'):
            with open('./.execmanignore') as file:
                lines = file.readlines()
                lines = [line.rstrip() for line in lines]

        exclude = lines + ['venv', '.idea', '.git', '__pycache__', 'execman', 'lib']
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
