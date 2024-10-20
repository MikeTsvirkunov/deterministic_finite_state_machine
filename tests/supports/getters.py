from io import StringIO
import polars as pl

from custom_types.directions import Directions


def parse_list_test_property(property: str) -> list[str]:
    return property.split(', ')


def get_table(context, schema) -> pl.DataFrame:
    d = context.table
    d = [[i for i in r] for r in d]
    return pl.DataFrame(d, schema=schema, orient='row')


def parse_bool(b: str) -> bool:
    return b.lower() == 'true'


def parse_direction(b: str) -> Directions:
    return {
        'up': Directions.up,
        'down': Directions.down,
    }[b]
