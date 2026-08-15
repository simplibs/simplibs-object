from .create_simple_object_bulk_from_bulk_dict import create_simple_object_bulk_from_bulk_dict
from .BulkDict import BulkDict

def create_simple_object_bulk_from_table(table: list[list[Any]]):
    bulk = tuple(
        BulkDict(
            class_name=row[0],
            default=row[1],
            value_type=row[2],
            validate=row[3],
            logic=row[4],
            decompose=row[5],
            return_instance=row[6],
        )
        for row in table
    )
    return create_simple_object_bulk_from_bulk_dict(bulk)
