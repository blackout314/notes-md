import click
from datetime import datetime

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
def init()
    if not os.path.exists('.notes'):
        os.makedirs('.notes')

@click.command()
@click.argument('content')
def add(content):
    click.echo("Adding '%s' to %s" % (content, datetime.now()))

@click.command()
@click.argument('content')
def search(content):
    click.echo("Searching for '%s'" % content)

cli.add_command(init)
cli.add_command(add)
cli.add_command(search)

if __name__ == '__main__':
    cli()
