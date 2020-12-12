"""
A module handle the logic with the event table.
"""

from datetime import datetime
from typing import List, TypedDict

from coa_flask_app.db_accessor import Accessor


Event = TypedDict(
    "Event",
    {
        "event_id": int,
        "site_id": int,
        "volunteer_cnt": int,
        "trashbag_cnt": int,
        "trash_weight": float,
        "walking_distance": float,
    },
)


def get(volunteer_year: int, volunteer_season: str) -> List[Event]:
    """
    Gets a list of events.

    Returns:
        A list of events.
    """
    query = """
            SELECT
                event_id,
                site_id,
                volunteer_cnt,
                trashbag_cnt,
                trash_weight,
                walking_distance
            FROM coa_data.event AS cde
            WHERE
                cde.volunteer_year = %s AND
                cde.volunteer_season = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (volunteer_year, volunteer_season))
        return db_handle.fetchall()


def add(
    updated_by: str,
    site_id: int,
    volunteer_year: int,
    volunteer_season: str,
    volunteer_cnt: int,
    trashbag_cnt: int,
    trash_weight: float,
    walking_distance: float,
) -> None:
    """
    Adds an item.

    Args:
        updated_by: The user adding the item.
        site_id: The ID of the site where the event took place.
        volunteer_year: The year of event.
        volunteer_season: The season of the event.
        volunteer_cnt: The count of volunteers at the event.
        trashbag_cnt: The count of trashbags collected.
        trash_weight: The weight of the trashbags.
        walking_distance: The total distance walked of the volunteers.
    """
    mon = 4 if volunteer_season == "Spring" else 10
    volunteer_date = datetime.strptime(f"{volunteer_year}-{mon}", "%Y-%m").date()
    query = """
            INSERT INTO coa_data.event(
                updated_by,
                site_id,
                volunteer_date,
                volunteer_cnt,
                trashbag_cnt,
                trash_weight,
                walking_distance
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """
    with Accessor() as db_handle:
        db_handle.execute(
            query,
            (
                updated_by,
                site_id,
                volunteer_date,
                volunteer_cnt,
                trashbag_cnt,
                trash_weight,
                walking_distance,
            ),
        )


def update(
    event_id: int,
    updated_by: str,
    site_id: int,
    volunteer_year: int,
    volunteer_season: str,
    volunteer_cnt: int,
    trashbag_cnt: int,
    trash_weight: float,
    walking_distance: float,
) -> None:
    """
    Updates an event.

    Args:
        event_id: The ID of the event.
        updated_by: The user adding the item.
        site_id: The ID of the site where the event took place.
        volunteer_year: The year of event.
        volunteer_season: The season of the event.
        volunteer_cnt: The count of volunteers at the event.
        trashbag_cnt: The count of trashbags collected.
        trash_weight: The weight of the trashbags.
        walking_distance: The total distance walked of the volunteers.
    """
    mon = 4 if volunteer_season == "Spring" else 10
    volunteer_date = datetime.strptime(f"{volunteer_year}-{mon}", "%Y-%m").date()
    query = """
            UPDATE coa_data.event
            SET
                updated_by = %s,
                site_id = %s,
                volunteer_date = %s,
                volunteer_cnt = %s,
                trashbag_cnt = %s,
                trash_weight = %s,
                walking_distance = %s
            WHERE item_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(
            query,
            (
                updated_by,
                site_id,
                volunteer_date,
                volunteer_cnt,
                trashbag_cnt,
                trash_weight,
                walking_distance,
                event_id,
            ),
        )


def remove(event_id: int) -> None:
    """
    Removes an event.

    Args:
        event_id: The ID of the event.
    """
    query = """
            DELETE FROM coa_data.event
            WHERE event_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (event_id,))
