"""config commands"""

import click


@click.group(name="cfg")
@click.pass_context
def cli(ctx):
    """configuration commands"""
    pass


@cli.command()
@click.pass_context
def ls(ctx):
    """list config items"""
    for k, v in ctx.obj.items():
        click.echo(f"{k}={v}")


@cli.command()
@click.argument("key", type=str)
@click.pass_context
def rm(ctx, key):
    """remove config item"""
    ctx.obj.pop(key, None)


@cli.command()
@click.argument("key", type=str)
@click.argument("value", type=str, default="", required=False)
@click.pass_context
def set(ctx, key, value):
    """set config value"""
    ctx.obj[key] = value


@cli.command()
@click.argument("key", type=str)
@click.pass_context
def get(ctx, key):
    """output config value"""
    click.echo(ctx.obj[key])
