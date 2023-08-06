""" default command """

from decimal import Decimal

import click
import requests
from eth_utils import denoms, from_wei, to_wei


@click.command()
@click.argument("args", nargs=-1)
@click.pass_context
def cli(ctx, args):
    args = list(args)
    args.insert(0, ctx.info_name)
    _input = ctx.obj["_input"]
    _output = ctx.obj["_output"]
    if len(args) == 3:
        _input, _output, in_value = args
    elif len(args) == 2:
        _input, in_value = args
    elif len(args) == 1:
        in_value = args[0]
    else:
        in_value = Decimal(1)

    _input = _input.lower()
    _output = _output.lower()
    in_value = Decimal(in_value)

    out_value = convert_from_wei(_output, convert_to_wei(_input, in_value))

    if ctx.obj.verbose:
        out = f"{in_value} {_input} == {out_value} {_output}"
    elif _output == "usd":
        out = "%.2f" % out_value
    else:
        out = f"{out_value}"
    click.echo(out)


def _convert_type(currency):
    if currency == "eth":
        currency = "ether"
    return currency


def convert_to_wei(currency, value):
    _type = _convert_type(currency)
    if hasattr(denoms, _type):
        return to_wei(value, _type)
    else:
        if _type == "usd":
            return to_wei(usd_to_eth(value), "ether")
        else:
            raise TypeError(f"unkown input type: {currency.upper()}")


def convert_from_wei(currency, value):
    _type = _convert_type(currency)

    if hasattr(denoms, _type):
        return from_wei(value, _type)
    else:
        if _type == "usd":
            return eth_to_usd(from_wei(value, "ether"))
        else:
            raise TypeError(f"unknown output type: {currency.upper()}")


def eth_to_usd(eth_value):
    price = coingecko_price("ethereum", "usd")
    return eth_value * price


def usd_to_eth(usd_value):
    price = coingecko_price("ethereum", "usd")
    return usd_value / price


def coingecko_price(coin="ethereum", unit="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    headers = {"accept": "application/json"}
    params = {"ids": coin, "vs_currencies": unit}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return Decimal(data[coin][unit])
