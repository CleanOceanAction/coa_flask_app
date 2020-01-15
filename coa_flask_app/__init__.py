"""
The main entrance to the flask app.

This includes the setting up of flask as well as all of the routes for
the application.
"""


from datetime import datetime

from flask import jsonify, request, session, url_for, Flask
from flask_cors import CORS

from coa_flask_app import contribution, site


APP = Flask(__name__)
CORS(APP)


@APP.route('/')
def index():
    """
    Index holds the main page for the REST API.

    This is mainly designed to send over a list of valid routes.

    Returns:
        The json list of valid routes.
    """
    return jsonify([str(rule) for rule in APP.url_map.iter_rules()])


@APP.route('/locations')
def all_locations_list():
    """
    The locations route returns all the locations.

    Returns:
        A json list of all the locations.
    """
    return jsonify(locations=site.all_locations_list())


@APP.route('/dirtydozen')
def dirty_dozen():
    """
    The dirty dozen route is designed to give the UI the data
    for a dirty dozen.

    The app route itself contains:
        locationCategory - Default of site.
        locationName     - Default of the common location.
        startDate        - The old start date for historical reasons.
        endDate          - Now.

    Returns:
        The dirty dozen for the requested category, name, and date range.
    """
    location_category = request.args.get('locationCategory',
                                         default='site',
                                         type=str)
    location_category = 'site_name' if location_category == 'site' else location_category

    location_name = request.args.get('locationName',
                                     default='Union Beach',
                                     type=str)
    start_date = request.args.get('startDate',
                                  default='2016-1-1',
                                  type=str)
    end_date = request.args.get('endDate',
                                default=datetime.now().strftime('%Y-%m-%d'),
                                type=str)

    return jsonify(dirtydozen=site.dirty_dozen(location_category,
                                               location_name,
                                               start_date,
                                               end_date))


@APP.route('/breakdown')
def breakdown():
    """
    The breakdown route is designed to give the UI the data
    for a breakdown.

    The app route itself contains:
        locationCategory - Default of site.
        locationName     - Default of the common location.
        startDate        - The old start date for historical reasons.
        endDate          - Now.

    Returns:
        The breakdown for the requested category, name, and date range.
    """
    location_category = request.args.get('locationCategory',
                                         default='site',
                                         type=str)
    location_category = 'site_name' if location_category == 'site' else location_category

    location_name = request.args.get('locationName',
                                     default='Union Beach',
                                     type=str)
    start_date = request.args.get('startDate',
                                  default='2016-1-1',
                                  type=str)
    end_date = request.args.get('endDate',
                                default=datetime.now().strftime('%Y-%m-%d'),
                                type=str)

    return jsonify(data=site.breakdown(location_category,
                                       location_name,
                                       start_date,
                                       end_date))


@APP.route('/validdaterange')
def valid_date_range():
    """
    The valid date range route is designed to give the UI a valid date
    range.

    The app route itself contains:
        locationCategory - Default of site.
        locationName     - Default of the common location.

    Returns:
        The valid date range for the requested category and name.
    """
    location_category = request.args.get('locationCategory',
                                         default='site',
                                         type=str)
    location_category = 'site_name' if location_category == 'site' else location_category

    location_name = request.args.get('locationName',
                                     default='Union Beach',
                                     type=str)

    return jsonify(validDateRange=site.valid_date_range(location_category,
                                                        location_name))


@APP.route('/locationsHierarchy')
def locations_hierarchy():
    """
    The locations hierarchy route returns the all the locations in a hierarchy.

    Returns:
        A json list of the locations hierarchy.
    """
    return jsonify(locationsHierarchy=site.locations_hierarchy())


@APP.route('/getTLs')
def get_tls():
    """
    The get tls route returns the all the team leads for the input drop down.

    Returns:
        A json list of the team leads.
    """
    return jsonify(getTLs=contribution.get_tls())


@APP.route('/getTrashItems')
def get_trash_items():
    """
    The get trash items route returns the all the trash items for the input
    drop down.

    Returns:
        A json list of the trash items.
    """
    return jsonify(getTrashItems=contribution.get_trash_items())


@APP.route('/saveUserInfo', methods=['POST'])
def save_user_info():
    """
    A post request to store user info in the database.

    Returns:
        An empty JSON on success, and error response otherwise.
    """
    # TODO: Why are we passing the values in like this,
    # why don't we do this smarter?
    userinfo = request.form.items()[0][0].split('||')
    updater = userinfo[0]
    eventcode = userinfo[1]
    if not updater or not eventcode:
        error = jsonify(error='Bad user input')
        error.status_code = 400
        return error

    # TODO: Is sessions really the best way to do this when it comes to
    # REACT. I feel like this might be best done with cookies instead.
    session['updater'] = updater
    session['eventcode'] = eventcode
    return jsonify({})


@APP.route('/insertContribution', methods=['POST'])
def insert_contribution():
    """
    A post request to insert a contribution into the database.

    Returns:
        An empty JSON on success, and error response otherwise.
    """
    contribution.insert_contribution(request.form.items()[0][0])
    return jsonify({})

@APP.route('/correct')
def totalCorrect(data_dict):
    """
    This function double checks that the total of the rows are correct
    """
    for r in range(0,data_dict.shape[0]):
        rowSeries = data_dict.iloc[r]
        total = 0
        print(rowSeries.values)
        i=0
        while i < len(rowSeries.values)-1:
            if(np.isnan(rowSeries.values[i])):
                total += 0
            else:
                total = total + rowSeries.values[i]
            i+=1
        print (total)
        print(rowSeries.values[i])
        if(rowSeries.values[i] != total):
            print("ERROR: In row", r, "your total is incorrect!")
        else:
            print("Everything is all right!")
for sheetname in data_dict: #this traverses through the multiple sheets
     Total = totalCorrect(data_dict[sheetname])
     print (Total)

@APP.route('/repetition')
def repetitionOfItems(df):
    """
    This fucntion checks if items are repeated
    """
    temp = df[["Material","Category","Item Name"]]
    return temp[temp.duplicated(keep=False)]
for sheetname in data_dict: #this traverses through the multiple sheets
    repition = repetitionOfItems(data_dict2[sheetname])
    if repition.empty != True:
        print ("The following items are repeated in" ,(sheetname), ":",repition)

@APP.route('/negative')
def checkNegative(data):
    """
    This function checks if there is a negative number
    """
    problems=[]
    for r in range (0, data.shape[0]):
        rowSeries = data.iloc[r]
        for c in rowSeries.values:
            if c < 0:
                problems.append([r,c])
    return problems

for sheetname in data_dict:
    these_problems=checkNegative(data_dict[sheetname])
    for rc in these_problems:
        r=rc[0]
        c=rc[1]
        print("A value", c, "in row", r, "in sheet", sheetname ,"is negative")

@APP.route('/decimal')
def checkDecimal(data_dict):
    """
    This function checks if there are any decimals
    """
    decimal =[]
    for r in range (0, data_dict.shape[0]):
        rowSeries = data_dict.iloc[r]
        for c in rowSeries.values:
            if (pd.isnull(c) == False):
                cFloat = c
                if float(cFloat).is_integer() == False:
                    decimal.append([r,cFloat])
    return decimal

for sheetname in data_dict:
    these_decimal=checkDecimal(data_dict[sheetname])
    for rcFloat in these_decimal:
        r=rcFloat[0]
        cFloat=rcFloat[1]
        print("A value", cFloat, "in row", r+11, "in sheet", sheetname ,"is a decimal")
