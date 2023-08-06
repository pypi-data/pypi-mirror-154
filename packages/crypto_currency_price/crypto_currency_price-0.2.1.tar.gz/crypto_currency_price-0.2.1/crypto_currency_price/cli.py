"""Console script for crypto_price_convert."""

import atexit
import json
import sys
from collections import UserDict
from pathlib import Path

import click

from .version import __timestamp__, __version__

NAME = "ccp"

CURRENCIES = ["USD", "ETH", "GWEI", "WEI"]
header = f"{NAME} v{__version__} {__timestamp__}"


class Context(UserDict):
    def __init__(self, config_file, debug, verbose):
        super().__init__()
        self.debug = debug
        self.verbose = verbose
        self.read_config(config_file)
        atexit.register(self.write_config)

    def read_config(self, config_file):
        self.config_file = config_file
        if self.config_file.exists():
            with self.config_file.open("r") as ifp:
                self.data = json.load(ifp)

    def write_config(self):
        with self.config_file.open("w") as ofp:
            json.dump(self.data, ofp)


class CustomMultiCommand(click.MultiCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        commands = Path(__file__).parent / "commands"
        self._cmd = {}
        for src in [e for e in commands.iterdir() if e.is_file()]:
            if src.suffix == ".py" and src.stem != "__init__":
                cmd = src.stem
                src = src.resolve()
                self._cmd[cmd] = src

    def list_commands(self, ctx):
        return sorted(list(self._cmd.keys()))

    def get_command(self, ctx, name):
        cmd = self._cmd.get(name, self._cmd["default"])
        code = compile(cmd.read_text(), cmd, "exec")
        ns = {}
        eval(code, ns, ns)
        return ns["cli"]


@click.command(cls=CustomMultiCommand, name=NAME)
@click.version_option(message=header)
@click.option("-d", "--debug", is_flag=True, envvar="DEBUG", help="debug mode")
@click.option(
    "-v", "--verbose", is_flag=True, envvar="VERBOSE", help="verbose output"
)
@click.option(
    "-i",
    "--input",
    "_input",
    type=click.Choice(CURRENCIES, case_sensitive=False),
)
@click.option(
    "-o",
    "--output",
    "_output",
    type=click.Choice(CURRENCIES, case_sensitive=False),
)
@click.option(
    "-c",
    "--config-file",
    envvar=f"{NAME}_CONFIG",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path.home() / f".{NAME}",
)
@click.pass_context
def cli(ctx, debug, verbose, _input, _output, config_file):
    """ccp converts prices"""

    def exception_handler(
        exception_type, exception, traceback, debug_hook=sys.excepthook
    ):

        if debug:
            debug_hook(exception_type, exception, traceback)
        else:
            click.echo(f"{exception_type.__name__}: {exception}", err=True)

    sys.excepthook = exception_handler

    ctx.obj = Context(config_file, bool(debug), bool(verbose))

    ctx.obj["_input"] = _input or ctx.obj.get("input", "GWEI")
    ctx.obj["_output"] = _output or ctx.obj.get("output", "USD")

    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
