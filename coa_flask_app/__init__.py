"""
The main entrance to the flask app.

This includes the setting up of flask as well as all of the routes for
the application.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from coa_flask_app import auth, items, sites, events, event_items


APP = Flask(__name__)
CORS(APP)


@APP.route("/")
def index():
    """
    Index holds the main page for the REST API.

    This is mainly designed to send over a list of valid routes.

    Returns:
        The json list of valid routes.
    """
    return jsonify([str(rule) for rule in APP.url_map.iter_rules()])


@APP.route("/login", methods=["POST"])
def login():
    """
    A route for logging in.

    This app route itself contains:
        username - The user trying to login.
        password - The password of the user logging in.

    Returns:
        A JWT to be used for further authentication.
    """
    args = json.loads(request.data.decode())
    username = args["username"]
    password = args["password"]

    return jsonify(token=auth.login(username, password))


@APP.route("/items")
def get_items():
    """
    The items route returns all the items.

    Returns:
        A json list of all the items.
    """
    return jsonify(items=items.get())


@APP.route("/items/add", methods=["POST"])
@auth.verify_token
def add_item():
    """
    The add items route adds an item.

    The app route itself contains:
        material  - The name of the material.
        category  - The name of the category.
        item_name - The name of the item.
    """
    args = json.loads(request.data.decode())
    material = args["material"]
    category = args["category"]
    item_name = args["item_name"]

    items.add(material, category, item_name)
    return jsonify()


@APP.route("/items/update", methods=["POST"])
@auth.verify_token
def update_item():
    """
    The update items route updates an existing item.

    The app route itself contains:
        item_id   - The ID of the item to update.
        material  - The name of the material.
        category  - The name of the category.
        item_name - The name of the item.
    """
    args = json.loads(request.data.decode())
    item_id = args["item_id"]
    material = args["material"]
    category = args["category"]
    item_name = args["item_name"]

    items.update(item_id, material, category, item_name)
    return jsonify()


@APP.route("/items/remove", methods=["POST"])
@auth.verify_token
def remove_item():
    """
    The remove items route removes an existing item.

    The app route itself contains:
        item_id - The ID of the item to remove.
    """
    args = json.loads(request.data.decode())
    item_id = args["item_id"]

    items.remove(item_id)
    return jsonify()


@APP.route("/sites")
def get_sites():
    """
    The sites route returns all the sites.

    Returns:
        A json list of all the sites.
    """
    return jsonify(sites=sites.get())


@APP.route("/sites/add", methods=["POST"])
@auth.verify_token
def add_site():
    """
    The add sites route adds an site.

    The app route itself contains:
        site_name - The name of the site.
        state     - The state that site is in.
        county    - The county that site is in.
        town      - The town that site is in.
        street    - The street that site is on.
        zipcode   - The zipcode of the site.
        lat       - The latitude of the site.
        long      - The longitude of the site.
    """
    args = json.loads(request.data.decode())
    site_name = args["site_name"]
    state = args["state"]
    county = args["county"]
    town = args["town"]
    street = args["street"]
    zipcode = args["zipcode"]
    lat = args["lat"]
    long_f = args["long"]

    sites.add(site_name, state, county, town, street, zipcode, lat, long_f)
    return jsonify()


@APP.route("/sites/update", methods=["POST"])
@auth.verify_token
def update_site():
    """
    The update sites route updates an existing site.

    The app route itself contains:
        site_id   - The ID of the site to update.
        site_name - The name of the site.
        state     - The state that site is in.
        county    - The county that site is in.
        town      - The town that site is in.
        street    - The street that site is on.
        zipcode   - The zipcode of the site.
        lat       - The latitude of the site.
        long      - The longitude of the site.
    """
    args = json.loads(request.data.decode())
    site_id = args["site_id"]
    site_name = args["site_name"]
    state = args["state"]
    county = args["county"]
    town = args["town"]
    street = args["street"]
    zipcode = args["zipcode"]
    lat = args["lat"]
    long_f = args["long"]

    sites.update(site_id, site_name, state, county, town, street, zipcode, lat, long_f)
    return jsonify()


@APP.route("/sites/remove", methods=["POST"])
@auth.verify_token
def remove_site():
    """
    The remove sites route removes an existing site.

    The app route itself contains:
        site_id - The ID of the site to remove.
    """
    args = json.loads(request.data.decode())
    site_id = args["site_id"]

    sites.remove(site_id)
    return jsonify()


@APP.route("/events")
def get_events():
    """
    The events route returns all the events for a given year and season.

    The app route itself contains:
        volunteer_year   - The year in question.
        volunteer_season - The season in question.

    Returns:
        A json list of all the events.
    """
    volunteer_year = request.args.get("volunteer_year", type=int)
    volunteer_season = request.args.get("volunteer_season", type=str)

    return jsonify(events=events.get(volunteer_year, volunteer_season))


@APP.route("/events/add", methods=["POST"])
@auth.verify_token
def add_event():
    """
    The add events route adds an event.

    The app route itself contains:
        updated_by       - The user making the update.
        site_id          - The ID of the site where the event took place.
        volunteer_year   - The year of event.
        volunteer_season - The season of the event.
        volunteer_cnt    - The count of volunteers at the event.
        trashbag_cnt     - The count of trashbags collected.
        trash_weight     - The weight of the trashbags.
        walking_distance - The total distance walked of the volunteers.
    """
    args = json.loads(request.data.decode())
    updated_by = args["updated_by"]
    site_id = args["site_id"]
    volunteer_year = args["volunteer_year"]
    volunteer_season = args["volunteer_season"]
    volunteer_cnt = args["volunteer_cnt"]
    trashbag_cnt = args["trashbag_cnt"]
    trash_weight = args["trash_weight"]
    walking_distance = args["walking_distance"]

    events.add(
        updated_by,
        site_id,
        volunteer_year,
        volunteer_season,
        volunteer_cnt,
        trashbag_cnt,
        trash_weight,
        walking_distance,
    )
    return jsonify()


@APP.route("/events/update", methods=["POST"])
@auth.verify_token
def update_event():
    """
    The update events route updates an existing event.

    The app route itself contains:
        event_id         - The ID of the event to update.
        updated_by       - The user making the update.
        site_id          - The ID of the site where the event took place.
        volunteer_year   - The year of event.
        volunteer_season - The season of the event.
        volunteer_cnt    - The count of volunteers at the event.
        trashbag_cnt     - The count of trashbags collected.
        trash_weight     - The weight of the trashbags.
        walking_distance - The total distance walked of the volunteers.
    """
    args = json.loads(request.data.decode())
    event_id = args["event_id"]
    updated_by = args["updated_by"]
    site_id = args["site_id"]
    volunteer_year = args["volunteer_year"]
    volunteer_season = args["volunteer_season"]
    volunteer_cnt = args["volunteer_cnt"]
    trashbag_cnt = args["trashbag_cnt"]
    trash_weight = args["trash_weight"]
    walking_distance = args["walking_distance"]

    events.update(
        event_id,
        updated_by,
        site_id,
        volunteer_year,
        volunteer_season,
        volunteer_cnt,
        trashbag_cnt,
        trash_weight,
        walking_distance,
    )
    return jsonify()


@APP.route("/events/remove", methods=["POST"])
@auth.verify_token
def remove_event():
    """
    The remove events route removes an existing event.

    The app route itself contains:
        event_id - The ID of the event to remove.
    """
    args = json.loads(request.data.decode())
    event_id = args["event_id"]

    events.remove(event_id)
    return jsonify()


@APP.route("/event-items")
def get_event_items():
    """
    The event items route returns all the event items for a given event.

    The app route itself contains:
        event_id - The ID of the event to look up items for.

    Returns:
        A json list of all the event items.
    """
    event_id = request.args.get("event_id", type=int)

    return jsonify(event_items=event_items.get(event_id))


@APP.route("/event-items/add", methods=["POST"])
@auth.verify_token
def add_event_item():
    """
    The add event items route adds an event.

    The app route itself contains:
        event_id   - The ID of the event.
        item_id    - The ID of the item collected.
        quantity   - The quantity of the item collected.
        updated_by - The user making the update.
    """
    args = json.loads(request.data.decode())
    event_id = args["event_id"]
    item_id = args["item_id"]
    quantity = args["quantity"]
    updated_by = args["updated_by"]

    event_items.add(event_id, item_id, quantity, updated_by)
    return jsonify()


@APP.route("/event-items/update", methods=["POST"])
@auth.verify_token
def update_event_item():
    """
    The update event items route updates an existing event item.

    The app route itself contains:
        record_id  - The ID of the event item.
        event_id   - The ID of the event.
        item_id    - The ID of the item collected.
        quantity   - The quantity of the item collected.
        updated_by - The user making the update.
    """
    args = json.loads(request.data.decode())
    record_id = args["record_id"]
    event_id = args["event_id"]
    item_id = args["item_id"]
    quantity = args["quantity"]
    updated_by = args["updated_by"]

    event_items.update(record_id, event_id, item_id, quantity, updated_by)
    return jsonify()


@APP.route("/event-items/remove", methods=["POST"])
@auth.verify_token
def remove_event_item():
    """
    The remove event items route removes an existing event item.

    The app route itself contains:
        record_id - The ID of the event item to remove.
    """
    args = json.loads(request.data.decode())
    record_id = args["record_id"]

    event_items.remove(record_id)
    return jsonify()
