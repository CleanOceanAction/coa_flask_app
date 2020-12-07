"""
A module handle the logic with the item table.
"""

from typing import List, Tuple

from coa_flask_app.db_accessor import Accessor


Item = Tuple[int, str, str, str]


def get() -> List[Item]:
    """
    Gets a list of items.

    Returns:
        A list of items.
    """
    query = """
            SELECT
                item_id,
                material,
                category,
                item_name
            FROM coa_data.item
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        return db_handle.fetchall()


def add(material: str, category: str, item_name: str) -> None:
    """
    Adds an item.

    Args:
        material: The material of the item.
        category: The category of the item.
        item_name: The name of the item.
    """
    query = """
            INSERT INTO coa_data.item(
                material,
                category,
                item_name
            )
            VALUES(%s, %s, %s)
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (material, category, item_name))


def update(item_id: int, material: str, category: str, item_name: str) -> None:
    """
    Updates an item.

    Args:
        item_id: The ID of the item.
        material: The material of the item.
        category: The category of the item.
        item_name: The name of the item.
    """
    query = """
            UPDATE coa_data.item
            SET
                material = %s,
                category = %s,
                item_name = %s
            WHERE item_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (material, category, item_name, item_id))


def remove(item_id: int) -> None:
    """
    Removes an item.

    Args:
        item_id: The ID of the item.
    """
    query = """
            DELETE FROM coa_data.item
            WHERE item_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (item_id,))
