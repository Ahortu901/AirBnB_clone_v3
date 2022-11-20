#!/usr/bin/python3
""" Module for storing indeces for the route to places. """
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models import storage


@app_views.route("/cities/<city_id>/places", methods=["GET"])
def return_list_all_places_by_city(city_id):
    """ Returns places by city id. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = city.places
    list_of_json_places = []
    for place in list_places:
        list_of_json_places.append(place.to_dict())
    return(jsonify(list_of_json_places))


@app_views.route("/places/<place_id>", methods=["GET"])
def return_place_by_id(place_id):
    """ Returns place by id. """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return(jsonify(place.to_dict()))


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place_obj(place_id):
    """ Deletes a place object by id. """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return({})
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place_obj(city_id):
    """ Creates a new place linked to a City. """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data.keys():
        abort(400, 'Missing name')
    if 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    if storage.get(City, city_id) is None:
        abort(404)
    if storage.get(User, data['user_id']) is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"])
def update_place_obj(place_id):
    """ Updates a place by its id. """
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    place = storage.get(Place, place_id)
    if place:
        for key, value in data.items():
            if key not in ignored_keys:
                setattr(place, key, value)
                place.save()
        return(jsonify(place.to_dict()))
    abort(404)


@app_views.route("/places_search", methods=["POST"])
def search_places_obj():
    """Retrieves all Place objects depending of JSON in the body of request."""
    has_states_values = 0
    has_cities_values = 0
    has_amenities_values = 0
    result_list = []
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if bool(data) is False:
        for place in storage.all(Place).values():
            result_list.append(place.to_dict())
        return jsonify(result_list)
    else:
        if "states" in data and len(data["states"]) != 0:
            has_states_values = 1
        if "cities" in data and len(data["cities"]) != 0:
            has_cities_values = 1
        if "amenities" in data and len(data["amenities"]) != 0:
            has_amenities_values = 1
        if has_states_values == 0 and has_cities_values == 0:
            for place in storage.all(Place).values():
                result_list.append(place)
        elif has_states_values != 0 and has_cities_values == 0:
            for value in data["states"]:
                state = storage.get(State, value)
                cities = state.cities
                for city in cities:
                    places = city.places
                    for place in places:
                        result_list.append(place)
        elif has_states_values == 0 and has_cities_values != 0:
            for city_id in data["cities"]:
                city = storage.get(City, city_id)
                places = city.places
                for place in places:
                    result_list.append(place)
        elif has_states_values != 0 and has_cities_values != 0:
            cities_list = []
            for value in data["states"]:
                state = storage.get(State, value)
                cities = state.cities
                for city in cities:
                    cities_list.append(city)
            for city_id in data["cities"]:
                city = storage.get(City, city_id)
                if city not in cities_list:
                    cities_list.append(city)
            for city in cities_list:
                places = city.places
                for place in places:
                    result_list.append(place)
        # Filter for amenities
        result = []
        amenity_list = []
        if has_amenities_values != 0:
            for amenity_id in data["amenities"]:
                amenity = storage.get(Amenity, amenity_id)
                amenity_list.append(amenity)
        for place in result_list:
            result.append(place.to_dict())
            if has_amenities_values != 0:
                amenities = place.amenities
                for amenity in amenity_list:
                    if amenity not in amenities:
                        result.pop()
                        break
        return jsonify(result)
