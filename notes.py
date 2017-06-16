import os
import click
from datetime import datetime

import slugify as slugify
from colorama import Fore, Back, Style

BASE_PATH = '.notes'


@click.group()
def cli():
    """A simple note taking CLI application"""
    pass


@click.command()
def init():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)


@click.command()
@click.confirmation_option(help='All your notes will be erased. Are you sure you want to continue?')
def clear():
    for root, dirs, files in os.walk(BASE_PATH, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


@click.command()
@click.argument('title')
@click.argument('content', default="")
def add(title, content):
    if not os.path.exists(BASE_PATH):
        click.echo('Not initialized. Please run "notes init" to initialize.')
        exit()

    file_name = "%s.md" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    title_path = os.path.join(BASE_PATH, title)
    note_file = os.path.join(title_path, file_name)

    if not content:
        content = click.edit()

    if content:
        if not os.path.exists(title_path):
            os.makedirs(title_path)
        with click.open_file(note_file, "a") as new_note:
            new_note.write(content)


def list_files(startpath, print_files=True):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        heading = '#' * level
        if level == 1:
            print("")
        print('{} {}'.format(heading, os.path.basename(root)))
        subindent = ' ' * (level + 1)
        if print_files:
            for f in files:
                print('{}{}'.format(subindent, f))


@click.command()
def struct():
    list_files(BASE_PATH, print_files=True)


@click.command()
@click.argument('file')
def edit():
    click.edit(filename='.notes/1/2/3/ciao2.md')


@click.command()
@click.argument('content')
def search(content):
    for root, dirs, files in os.walk(BASE_PATH, topdown=False):
        for name in files:
            abs_path = os.path.join(root, name)
            search_file = open(abs_path, "r")
            for line in search_file:
                if content in line:
                    click.echo(Fore.MAGENTA + "/".join(abs_path.split('/')[1:]) + ": " +
                               Fore.RESET + line.strip())
            search_file.close()


cli.add_command(init)
cli.add_command(clear)
cli.add_command(add)
cli.add_command(edit)
cli.add_command(struct)
cli.add_command(search)

if __name__ == '__main__':
    cli()
