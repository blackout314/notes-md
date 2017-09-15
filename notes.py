import os
import click
from datetime import datetime

from slugify import slugify
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

    nested_titles = [t.strip() for t in title.split('/')]

    for i in range(len(nested_titles) + 1):
        current_path = os.path.join(BASE_PATH, *[slugify(t) for t in nested_titles[:i]])
        if not os.path.exists(current_path):
            os.makedirs(current_path)
            with click.open_file(os.path.join(current_path, '.title'), 'w') as title_file:
                title_file.write(nested_titles[i - 1])

    title_path = os.path.join(BASE_PATH, *[slugify(t) for t in nested_titles])
    note_file = os.path.join(title_path, file_name)

    if not content:
        content = click.edit()

    if content:
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
            with click.open_file(os.path.join(root, '.title'), 'r') as title_file:
                title = title_file.read()
                click.echo('{} {}'.format(heading, title))
                subindent = ' ' * (level + 1)
                if print_files:
                    for f in files:
                        if not f.startswith('.'):
                            click.echo('{}{}'.format(subindent, f))


@click.command()
def struct():
    list_files(BASE_PATH, print_files=True)


@click.command()
@click.argument('title')
def edit(title):
    title = "/".join([slugify(t.strip()) for t in title.split('/')])

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
            with click.open_file(abs_path, 'r') as search_file:
                for line in search_file:
                    if content.lower() in line.lower():
                        click.echo(Fore.MAGENTA + "/".join(abs_path.split('/')[1:-1]) + ": " +
                                   Fore.RESET + line.strip())


@click.command()
@click.argument('title', default="")
def read(title):
    """Read your notes"""
    if title:
        click.echo("Read {} notes".format(title))

    for root, dirs, files in os.walk(BASE_PATH, topdown=True):

        for f in files:
            title_path = os.path.join(root, f)
            with click.open_file(title_path, 'r') as title_file:
                content = title_file.read()

            level = (title_path.count(os.sep) - 1)
            if level > 0 and f == '.title':
                content = '\n' + '#' * level + ' ' + content

            click.echo(content)


cli.add_command(init)
cli.add_command(clear)
cli.add_command(add)
cli.add_command(edit)
cli.add_command(struct)
cli.add_command(search)
cli.add_command(read)

if __name__ == '__main__':
    cli()
