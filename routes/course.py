"""Routes for the course resource.
"""

from run import app
from flask import request
from http import HTTPStatus
import data
from . import validate_data
from datetime import datetime

dataget = data.load_data()


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    if id not in dataget:
        response = {'message': 'Course {} does not exist'.format(
            id)}, HTTPStatus.NOT_FOUND
    else:
        response = {'data': dataget[id]}, HTTPStatus.OK
    return response


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    page_size = int(request.args.get('page_size', 5))
    page_number = int(request.args.get('page_number', 1))
    skip = max((page_number-1)*page_size, 0)
    title_words = request.args.get("title_words", None)
    data = [v for v in dataget.values()]
    if not title_words:
        metadata = {
            "page_count": int(len(data)/page_size),
            "page_number": page_number,
            "page_size": page_size,
            "record_count": len(data)
        }
        response = {"data": data[skip:skip+page_size],
                    "metadata": metadata}, HTTPStatus.OK
    else:
        search_title = title_words.split(',')
        filter_by_title = []
        for course in data:
            for x in search_title:
                if x.lower() in course['title'].lower():
                    filter_by_title.append(course)
        response = {"data": filter_by_title, "metadata": {
            "record_count": len(filter_by_title)}}, HTTPStatus.OK

    return response


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    # YOUR CODE HERE
    create_course = request.get_json()
    validation = validate_data.validate(create_course)
    if 'error' in validation:
        response = validation, HTTPStatus.BAD_REQUEST
    else:
        id = max(list(dataget))+1
        create_course['id'] = id
        create_course['date_created'] = datetime.now()
        dataget[id] = create_course
        dataget[id]['date_updated'] = datetime.now()
        response = {'data': dataget[id]}, HTTPStatus.CREATED
    return response


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    if id in dataget:
        update_course = request.get_json()
        validation = validate_data.validate(update_course)
        if 'error' in validation:
            response = validation, HTTPStatus.BAD_REQUEST
        else:
            if update_course['id'] != dataget[id]['id']:
                response = {
                    "message": "The id does match the payload"}, HTTPStatus.BAD_REQUEST
            else:
                update_course['date_created'] = dataget[id]['date_created']
                dataget[id] = update_course
                dataget[id]['date_updated'] = datetime.now()
                updated_data = dataget[id]
                del updated_data['date_created']
                response = {'data': updated_data}, HTTPStatus.OK
    else:
        response = {
            "message": "The id {} does exits".format(id)}, HTTPStatus.NOT_FOUND
    return response


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    if id in dataget:
        del dataget[id]
        response = {
            "message": "The specified course was deleted"}, HTTPStatus.OK
    else:
        response = {"messge": "Course {} does not exist".format(
            id)}, HTTPStatus.NOT_FOUND
    return response
