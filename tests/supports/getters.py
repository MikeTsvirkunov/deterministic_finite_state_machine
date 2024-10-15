from io import StringIO
import polars as pl


def parse_list_test_property(property: str) -> list[str]:
    return property.split(', ')


def get_table(context, schema) -> pl.DataFrame:
    d = context.table
    d = [[i for i in r] for r in d]
    return pl.DataFrame(d, schema=schema, orient='row')

