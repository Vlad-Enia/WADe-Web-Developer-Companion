from flask import Flask, request, make_response, jsonify, abort
from hashlib import sha256


def get_preferences_for_user(collection, username):
    return collection.find_one({'owner_username': username}) 

def update_preferences_for_user(collection, username, updated_preferences, updated_topics):
    return collection.find_one_and_update({"owner_username": username}, {'$set': {'origins': updated_preferences}, '$set': {'topics': updated_topics}}, new=True)
