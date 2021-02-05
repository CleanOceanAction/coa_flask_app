"""
A module handle the logic with the event table.
"""

from datetime import datetime
from typing import List, Optional, TypedDict

from coa_flask_app.db_accessor import Accessor


Event = TypedDict(
    "Event",
    {
        "event_id": int,
        "site_id": int,
        "volunteer_cnt": Optional[int],
        "trash_items_cnt": int,
        "trashbag_cnt": Optional[float],
        "trash_weight": Optional[float],
        "walking_distance": Optional[float],
        "updated_by": str,
        "updated_tsp": datetime,
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
                cde.event_id,
                cde.site_id,
                cde.volunteer_cnt,
                IFNULL(SUM(cei.quantity), 0) AS trash_items_cnt,
                cde.trashbag_cnt,
                cde.trash_weight,
                cde.walking_distance,
                cde.updated_by,
                cde.updated_tsp
            FROM coa_data.event AS cde
            LEFT JOIN coa_data.event_items AS cei ON cei.event_id = cde.event_id
            WHERE
                cde.volunteer_year = %s AND
                cde.volunteer_season = %s
            GROUP BY cde.event_id
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (volunteer_year, volunteer_season))
        return [
            {
                "event_id": record["event_id"],
                "site_id": record["site_id"],
                "volunteer_cnt": record["volunteer_cnt"],
                "trash_items_cnt": int(record["trash_items_cnt"]),
                "trashbag_cnt": record["trashbag_cnt"],
                "trash_weight": record["trash_weight"],
                "walking_distance": record["walking_distance"],
                "updated_by": record["updated_by"],
                "updated_tsp": record["updated_tsp"].strftime("%Y-%m-%d %H:%M"),
            }
            for record in db_handle.fetchall()
        ]


def add(
    updated_by: str,
    site_id: int,
    volunteer_year: int,
    volunteer_season: str,
    volunteer_cnt: Optional[int],
    trashbag_cnt: Optional[float],
    trash_weight: Optional[float],
    walking_distance: Optional[float],
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
    volunteer_cnt: Optional[int],
    trashbag_cnt: Optional[float],
    trash_weight: Optional[float],
    walking_distance: Optional[float],
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
            WHERE event_id = %s
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
