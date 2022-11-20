#!/usr/bin/python3
"""  place RestFul API """
from flask import Blueprint, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
import json


def init_places_reviews():
    from api.v1.views import app_views

    @app_views.route(
                    '/places/<place_id>/reviews',
                    methods=['GET'], strict_slashes=False)
    def get_reviews_by_place(place_id=None):
        """ Get reviews by place """
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        reviews = []
        for review in place.reviews:
            reviews.append(review.to_dict())
        return jsonify(reviews)

    @app_views.route(
                    '/reviews/<review_id>',
                    methods=['GET'],
                    strict_slashes=False)
    def get_review(review_id=None):
        '''get review by id'''
        review = storage.get("Review", review_id)
        if review is None:
            abort(404)
        return jsonify(review.to_dict())

    @app_views.route(
                    '/reviews/<review_id>',
                    methods=['DELETE'],
                    strict_slashes=False)
    def delete_review(review_id=None):
        '''delete a place by id'''
        review = storage.get("Review", review_id)
        if review is None:
            abort(404)
        storage.delete(review)
        return jsonify({}), 200

    @app_views.route(
                    'places/<place_id>/reviews',
                    methods=['POST'], strict_slashes=False)
    def new_review(place_id=None):
        '''create a new review'''
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        if 'user_id' not in request.json:
            return jsonify({"error": "Missing user_id"}), 400
        user = storage.get("User", request.json['user_id'])
        if user is None:
            abort(404)
        if 'text' not in request.json:
            return jsonify({"error": "Missing text"}), 400
        review = Review(**request.json)
        review.place_id = place_id
        storage.new(review)
        return jsonify(storage.get("Review", review.id).to_dict()), 201

    @app_views.route(
                    '/reviews/<review_id>',
                    methods=['PUT'],
                    strict_slashes=False
                    )
    def update_review(review_id=None):
        '''update a place'''
        review = storage.get("Review", review_id)
        if review is None:
            abort(404)
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400

        for key, value in request.json.items():
            if (
                key == 'id' or key == 'user_id' or
                key == 'place_id'
            ):
                pass
            else:
                setattr(review, key, value)
        storage.save()
        return jsonify(storage.get("Review", review.id).to_dict()), 200
