#!/usr/bin/python3
"""
Views index, contains status and stat endpoints.
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    stats = {
        "Amenity": storage.count('Amenity'),
        "City": storage.count('City'),
        "Place": storage.count('Place'),
        "Review": storage.count('Review'),
        "State": storage.count('State'),
        "User": storage.count('User')
    }
    return jsonify(stats)
