#!/usr/bin/python3
"""Handles RESTfull for 'State' Object"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from datetime import datetime
import uuid

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves list of all states"""
    all_states = storage.all(State).values()
    state_list = [state.to_dict() for state in all_states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Gets a single state that marches state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes state the matches state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State object"""
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    
    data = request.get_json()
    state_id = str(uuid.uuid4())
    created_at = datetime.now()
    updated_at = datetime.now()
    name = data['name']
    
    new_state = State(id=state_id, created_at=created_at, updated_at=updated_at, name=name)
    storage.new(new_state)
    storage.save()
    
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    if not request.json:
        abort(400, "Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    # Update the 'updated_at' timestamp
    state.updated_at = datetime.now()

    storage.save()
    return jsonify(state.to_dict()), 200
