"""
A module handle the logic with the sites table.
"""

from typing import List, Tuple

from coa_flask_app.db_accessor import Accessor


Site = Tuple[int, str, str, str, str, str, str, float, float]


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
                long
            FROM coa_data.sites
            """
    with Accessor() as db_handle:
        db_handle.execute(query)
        return db_handle.fetchall()


def add(site_name: str,
        state: str,
        county: str,
        town: str,
        street: str,
        zipcode: str,
        lat: float,
        long_f: float) -> None:
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
            INSERT INTO coa_data.sites(
                site_name,
                state,
                county,
                town,
                street,
                zipcode,
                lat,
                long
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (site_name,
                                  state,
                                  county,
                                  town,
                                  street,
                                  zipcode,
                                  lat,
                                  long_f))


def update(site_id: int,
           site_name: str,
           state: str,
           county: str,
           town: str,
           street: str,
           zipcode: str,
           lat: float,
           long_f: float) -> None:
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
            UPDATE coa_data.sites
            SET
                site_name = %s,
                state = %s,
                county = %s,
                town = %s,
                street = %s,
                zipcode = %s,
                lat = %s,
                long = %s
            WHERE site_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (site_name,
                                  state,
                                  county,
                                  town,
                                  street,
                                  zipcode,
                                  lat,
                                  long_f,
                                  site_id))


def remove(site_id: int) -> None:
    """
    Removes an site.

    Args:
        site_id: The ID of the site.
    """
    query = """
            DELETE FROM coa_data.sites
            WHERE site_id = %s
            """
    with Accessor() as db_handle:
        db_handle.execute(query, (site_id,))
