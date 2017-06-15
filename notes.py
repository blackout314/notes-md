import os
import click
from datetime import datetime

BASE_PATH = '.notes'


@click.command()
@click.option('--count', default=1, help="number of greetings")
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)


@click.group()
def cli():
    pass


@click.command()
def init():
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)


@click.command()
@click.confirmation_option(help='Are you sure you want to delete all your notes?')
def drop():
    for root, dirs, files in os.walk(BASE_PATH, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

    os.removedirs(BASE_PATH)


@click.command()
@click.argument('content')
def add(content):
    if not os.path.exists(BASE_PATH):
        click.echo('Not initialized. Please run "notes init" to initialize.')
        exit()
    file_name = "%s.md" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    click.echo("Adding '%s' to %s" % (content, file_name))

    new_note = open(os.path.join(BASE_PATH, file_name), "w")

    new_note.write(content)

    new_note.close()

    click.edit(filename=open(os.path.join(BASE_PATH, file_name)))


@click.command()
def edit():
    click.edit(filename='.notes/prova.md')

@click.command()
@click.argument('content')
def search(content):
    click.echo("Searching for '%s'" % content)


cli.add_command(init)
cli.add_command(drop)
cli.add_command(add)
cli.add_command(edit)
cli.add_command(search)

if __name__ == '__main__':
    cli()
