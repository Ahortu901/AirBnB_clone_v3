#!/usr/bin/python3
""" Module for storing amenities endpoints. """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from os import getenv as env
from models import storage


# All amenitites by place route. - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route("/places/<place_id>/amenities")
def return_list_all_amenities_by_place(place_id):
    """ Returns reviews by place id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_amenities = place.amenities
    list_of_json_amenities = []
    for amenity in list_amenities:
        list_of_json_amenities.append(amenity.to_dict())
    return(jsonify(list_of_json_amenities))


# DELETE Route, spaced out due to pep8 style.
route = "/places/<place_id>/amenities/<amenity_id>"


# Amenity by id in place route. - - - - - - - - - - - - - - - - - - - - - - - |
@app_views.route(route, methods=["DELETE"])
def delete_place_amenity_obj(place_id, amenity_id):
    """ Deletes an amenity on a place. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    # if env("HBNB_TYPE_STORAGE") == "db":
    if amenity not in place.amenities:
        return(404)
    place.amenities.remove(amenity)
    place.save()
    return({})
    # else:
    #     if hasattr(place, "amenity_ids"):
    #         if amenity.id in place.amenity_ids:
    #             place.amenity_ids.remove(amenity.id)
    #             place.save()
    #             return({})
    #     return(404)


# POST Route, spaced out due to pep8 style.
route = "/places/<place_id>/amenities/<amenity_id>"


# POST Amenity by id into place. - - - - - - - - - - - - - - - - - - - - - - -|
@app_views.route(route, methods=["POST"])
def add_amenity_to_place(place_id, amenity_id):
    """ Adds an amenity to the given place. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    # if env("HBNB_TYPE_STORAGE") == "db":
    if amenity in place.amenities:
        return(amenity.to_dict())
    place.amenities.append(amenity)
    place.save()
    return(amenity.to_dict(), 201)
    # else:
    #     if hasattr(place, "amenity_ids"):
    #         if amenity.id in place.amenity_ids:
    #             return(amenity.to_dict())
    #     setattr(place, "amenity_ids", [])
    #     place.amenity_ids.append(amenity.id)
    #     place.save()
    #     return(amenity.to_dict(), 201)
