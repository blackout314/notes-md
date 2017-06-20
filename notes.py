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
    """Initialize the notes folder."""
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)

        title = click.prompt("Title")
        author = click.prompt("Author")

        with click.open_file(os.path.join(BASE_PATH, ".title"), 'w') as title_file:
            title_file.write(title)

        with click.open_file(os.path.join(BASE_PATH, ".author"), 'w') as author_file:
            author_file.write(author)

    else:
        click.echo('Notes repository is initialized already.')


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

    # file_name = "%s.md" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # file_name = "{}.md".format('page')
    file_name = 'page.md'

    title_path = os.path.join(BASE_PATH, title)
    note_file = os.path.join(title_path, file_name)

    if not content:
        content = click.edit()

    if content:
        if not os.path.exists(title_path):
            os.makedirs(title_path)
        with click.open_file(note_file, "a") as new_note:
            new_note.write("\n{}\n".format(content))


def list_files(startpath, print_files=True):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        heading = '#' * level
        if level == 1:
            pass
        root_base_name = os.path.basename(root)
        if '.' not in root_base_name:
            click.echo('{} {}'.format(heading, root_base_name))
            subindent = ' ' * (level + 1)
            if print_files:
                for f in files:
                    click.echo('{}{}'.format(subindent, f))


@click.command()
def struct():
    list_files(BASE_PATH, print_files=True)


@click.command()
@click.argument('title')
def edit(title):
    note_path = os.path.join(BASE_PATH, title, "page.md")
    if os.path.exists(note_path):
        click.edit(filename=note_path)
    else:
        click.echo("No such title {}".format(title))


@click.command()
@click.argument('content')
def search(content):
    for root, dirs, files in os.walk(BASE_PATH, topdown=False):
        for name in files:
            abs_path = os.path.join(root, name)
            search_file = open(abs_path, "r")
            for line in search_file:
                if content in line:
                    click.echo(Fore.MAGENTA + "/".join(abs_path.split('/')[1:-1]) + ": " +
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
