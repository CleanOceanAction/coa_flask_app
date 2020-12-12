"""
A module handle the logic with the site table.
"""

from typing import List, Optional, TypedDict

from coa_flask_app.db_accessor import Accessor


Site = TypedDict(
    "Site",
    {
        "site_id": int,
        "site_name": str,
        "state": str,
        "county": str,
        "town": str,
        "street": str,
        "zipcode": str,
        "lat": Optional[float],
        "long": Optional[float],
    },
)


def get() -> List[Site]:
    """
    Gets a list of sites.

    Returns:
        A list of sites.
    """
    query = """
            SELECT
                site_id,
                site_name,
                state,
                county,
                town,
                street,
                zipcode,
                lat,
                `long`
            FROM coa_data.site
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        return [
            {
                "site_id": record["site_id"],
                "site_name": record["site_name"],
                "state": record["state"],
                "county": record["county"],
                "town": record["town"],
                "street": record["street"],
                "zipcode": record["zipcode"],
                "lat": None if record["lat"] is None else float(record["lat"]),
                "long": None if record["long"] is None else float(record["long"]),
            }
            for record in db_handle.fetchall()
        ]


def add(
    site_name: str,
    state: str,
    county: str,
    town: str,
    street: str,
    zipcode: str,
    lat: float,
    long_f: float,
) -> None:
    """
    Adds a site.

    Args:
        site_name: The name of the site.
        state: The state the site is in.
        county: The county the site is in.
        town: The town the site is in.
        street: The street the site is on.
        zipcode: The zipcode the site is in.
        lat: The latitude of the site.
        long_f: The longitude of the site.
    """
    query = """
            INSERT INTO coa_data.site(
                site_name,
                state,
                county,
                town,
                street,
                zipcode,
                lat,
                `long`
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """
    with Accessor() as db_handle:
        db_handle.execute(
            query, (site_name, state, county, town, street, zipcode, lat, long_f)
        )


def update(
    site_id: int,
    site_name: str,
    state: str,
    county: str,
    town: str,
    street: str,
    zipcode: str,
    lat: float,
    long_f: float,
) -> None:
    """
    Updates a site.

    Args:
        site_id: The ID of the site.
        site_name: The name of the site.
        state: The state the site is in.
        county: The county the site is in.
        town: The town the site is in.
        street: The street the site is on.
        zipcode: The zipcode the site is in.
        lat: The latitude of the site.
        long_f: The longitude of the site.
    """
    query = """
            UPDATE coa_data.site
            SET
                site_name = %s,
                state = %s,
                county = %s,
                town = %s,
                street = %s,
                zipcode = %s,
                lat = %s,
                `long` = %s
            WHERE site_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(
            query,
            (site_name, state, county, town, street, zipcode, lat, long_f, site_id),
        )


def remove(site_id: int) -> None:
    """
    Removes an site.

    Args:
        site_id: The ID of the site.
    """
    query = """
            DELETE FROM coa_data.site
            WHERE site_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (site_id,))
