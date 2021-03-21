import pytest
import requests

baseurl = "http://localhost:5000"


def test_get_specific_course():
    id = '2'
    response = requests.get(baseurl+"/course/"+id)
    assert response.status_code == 200


def test_get_specific_course_not_found():
    id = '300'
    response = requests.get(baseurl+"/course/"+id)
    assert response.status_code == 404


def test_get_course_by_page():
    response = requests.get(baseurl+"/course?page_size=6&page_number=2")
    assert response.status_code == 200


def test_get_course_page_by_title():
    response = requests.get(baseurl+"/course?title-words=Illustrated")
    assert response.status_code == 200


def test_add_course():
    data = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "price": 25,
        "title": "Blah blah blah",
        "on_discount": False,
        "description": "New description"
    }
    response = requests.post(baseurl+"/course", json=data)
    assert response.status_code == 201


def test_add_course_error():
    data = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "price": '25',
        "title": "Blah blah blah",
        "on_discount": False,
        "description": "New description"
    }
    response = requests.post(baseurl+"/course", json=data)
    assert response.status_code == 400


def test_update_course():
    id = "200"
    data = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "id": 200,
        "price": 25,
        "title": "Blah blah blah updated",
        "on_discount": False,
        "description": "New description"
    }

    response = requests.put(baseurl+"/course/"+id, json=data)
    assert response.status_code == 200


def test_update_course_error():
    id = "300"
    data = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "id": 300,
        "price": 25,
        "title": "Blah blah blah updated",
        "on_discount": False,
        "description": "New description"
    }

    response = requests.put(baseurl+"/course/"+id, json=data)
    assert response.status_code == 404


def test_update_course_payload_error():
    id = "200"
    data = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "id": 201,
        "price": 25,
        "title": "Blah blah blah updated",
        "on_discount": False,
        "description": "New description"
    }

    response = requests.put(baseurl+"/course/"+id, json=data)
    assert response.status_code == 400


def test_del_favourite():
    id = "120"
    response = requests.delete(baseurl+"/course/" + id)
    assert response.status_code == 200


def test_del_favourite_error():
    id = "300"
    response = requests.delete(baseurl+"/course/" + id)
    assert response.status_code == 404
