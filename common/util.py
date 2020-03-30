import logging
from flask import make_response
from flask_restful import abort

from config import ClientsConfig


def first(iterable, default=None, condition=lambda x: True):
    '''
    Returns the first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, returns the first item of
    the iterable.

    If the `default` argument is given and the iterable is empty,
    or if it has no items matching the condition, the `default` argument
    is returned if it matches the condition.

    The `default` argument being None is the same as it not being given.

    Raises `StopIteration` if no item satisfying the condition is found
    and default is not given or doesn't satisfy the condition.

    >>> first( (1,2,3), condition=lambda x: x % 2 == 0)
    2
    >>> first(range(3, 100))
    3
    >>> first( () )
    Traceback (most recent call last):
    ...
    StopIteration
    >>> first([], default=1)
    1
    >>> first([], default=1, condition=lambda x: x % 2 == 0)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> first([1,3,5], default=1, condition=lambda x: x % 2 == 0)
    Traceback (most recent call last):
    ...
    StopIteration
    '''

    try:
        return next(x for x in iterable if condition(x))
    except StopIteration:
        if default is not None and condition(default):
            return default
        else:
            raise


def extract_description(body):
    '''
    Extract the first english description from a nested dictionary.
    '''
    def pokemon_en_condition(x): return x['language']['name'] == 'en'
    first_en_description = first(
        body.get('flavor_text_entries'),
        condition=pokemon_en_condition)

    # Some strings contains newline artefacts thoughout it
    pokemon_description = first_en_description['flavor_text'].replace(
        '\n', ' ')
    return pokemon_description


def get_limit_header(req):
    '''
    Return a dictionary with custom rate limit header values
    for requests coming from either Funtranslation or Pokeapi.

    Requests URLs are checked agains config client URLs.
    '''
    headers = {}

    # Pokeapi does not set any rate limition information on the response
    # so the value must be kept in sync manually
    if ClientsConfig.POKEAPI_URL in req.url:
        headers['X-RateLimit-Pokeapi-Limit'] = '100 per IP address per minute'

    if ClientsConfig.FUNTRANSLATION_URL in req.url:
        headers['X-RateLimit-Pokeapi-Limit'] = '100 per IP address per minute'
        headers['X-RateLimit-Funtranslations-Limit'] = req.headers.get(
            'X-RateLimit-Limit')
        headers['X-RateLimit-Funtranslations-Remaining'] = req.headers.get(
            'X-RateLimit-Remaining')

    return headers


def check_response(req, api_name):
    '''
    Handle and log all non 200 requests.
    '''

    headers = get_limit_header(req)
    if req.status_code == 404:
        resp = make_response('', req.status_code)
        resp.headers.extend(headers)
        abort(resp)
    elif req.status_code == 429:
        logging.info(
            "To many requests! {} API limit reached!".format(api_name))
        resp = make_response('', req.status_code)
        resp.headers.extend(headers)
        abort(resp)
    elif req.status_code != 200:
        logging.error(
            "Unhandled response from Pokeapi API! status={}".format(
                req.status_code))
        resp = make_response('', 500)
        resp.headers.extend(headers)
        abort(resp)
    else:
        pass


class MockCache:
    '''
    Simple disctionaly store that is meant to replicate
    methods provided by Redis.

    Should be used for testing purposes only when
    needing to test the api and a mock cache is required.
    '''

    store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = value
        return True

    def expire(self, *unused):
        return True
