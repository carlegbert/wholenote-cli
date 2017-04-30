import click


@click.command()
@click.option('--email', prompt='email')
@click.option('--password', prompt='password', hide_input=True)
def login(email, password):
    click.echo('Login in with {0}:{1}'.format(email, password))
