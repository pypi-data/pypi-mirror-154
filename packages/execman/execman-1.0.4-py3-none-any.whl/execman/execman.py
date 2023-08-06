import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List

import typer

app = typer.Typer()


@app.command()
def execman(commands: List[Path], level):
    commands = [command.name for command in commands]
    lines = []
    is_contained_ignore = os.path.isfile('./.execmanignore')
    if is_contained_ignore:
        with open('./.execmanignore') as file:
            lines = file.readlines()
            lines = [line.rstrip() for line in lines]

    exclude = lines + ['venv', '.idea', '.git', '__pycache__', 'execman', 'lib', 'result', 'build', 'dist']
    if level == 1:
        main_folder = [str(name) for name in os.listdir(".") if
                       os.path.isdir(name) and name not in exclude]
        for first_level_folder in main_folder:
            os.chdir(f'./{first_level_folder}')
            for command in commands:
                os.system(command)
            print(datetime.now(), f' :: {first_level_folder} is execute')
            os.chdir('../')
        print(datetime.now(), ':: finished')
    elif level == 2:
        try:
            main_folder = [str(name) for name in os.listdir(".") if
                           os.path.isdir(name) and name not in exclude]
            for first_level_folder in main_folder:
                os.chdir(f'./{first_level_folder}')
                sub_folder = [name for name in os.listdir(f".") if os.path.isdir(name) and name not in exclude]
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


if __name__ == '__main__':
    app()
