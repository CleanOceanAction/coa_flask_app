"""
A module handle the logic with the items table.
"""

from typing import List, Tuple

from coa_flask_app.db_accessor import Accessor


EventItem = Tuple[int, int, int, int, str]


def get(event_id: int) -> List[EventItem]:
    """
    Gets a list of event items.

    Args:
        event_id: The ID of the event.

    Returns:
        A list of event items.
    """
    query = """
            SELECT
                record_id,
                event_id,
                item_id,
                quantity,
                updated_by,
            FROM coa_data.event_items AS cdei
            WHERE cdei.event_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (event_id,))
        return db_handle.fetchall()


def add(event_id: int, item_id: int, quantity: int, updated_by: str) -> None:
    """
    Adds an event item.

    Args:
        event_id: The ID of the event.
        item_id: The ID of the item collected.
        quantity: The quantity of the item collected.
        updated_by: The user making the update.
    """
    query = """
            INSERT INTO coa_data.event_items(
                event_id,
                item_id,
                quantity,
                updated_by
            )
            VALUES(%s, %s, %s, %s)
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (event_id, item_id, quantity, updated_by))


def update(record_id: int,
           event_id: int,
           item_id: int,
           quantity: int,
           updated_by: str) -> None:
    """
    Updates an event item.

    Args:
        record_id: The ID of the event item.
        event_id: The ID of the event.
        item_id: The ID of the item collected.
        quantity: The quantity of the item collected.
        updated_by: The user making the update.
    """
    query = """
            UPDATE coa_data.event_items
            SET
                event_id = %s,
                item_id = %s,
                quantity = %s,
                updated_by = %s
            WHERE record_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (event_id,
                                  item_id,
                                  quantity,
                                  updated_by,
                                  record_id))


def remove(record_id: int) -> None:
    """
    Removes an event item.

    Args:
        record_id: The ID of the event item.
    """
    query = """
            DELETE FROM coa_data.event_items
            WHERE record_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (record_id,))
