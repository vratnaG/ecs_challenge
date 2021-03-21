"""Routines associated with the application data.
"""
import json
courses = {}


def load_data():
    """Load the data from the json file.
    """
    f = open('./json/course.json',)
    data = json.load(f)
    for course in data:
        courses[course['id']] = course
    return courses
