import json
import logging
import pytz
from datetime import timedelta, datetime
from urllib.parse import urljoin

import requests
from flask import make_response
from flask_restful import Resource, abort

from config import ClientsConfig
from common import util
from .serializer import validate_pokemon, validate_family, validate_translation


class Pokemon(Resource):
    def __init__(self, **kwargs):
        self.cache = kwargs['cache']

    def get(self, pokemon_name):
        '''
        Return the first engligh Pokemon description from
        Pokeapi and translate it using Funtranslation into
        a Shakespearean style of narration.

        Rate limiting information is found custom headers
        `X-RateLimit-Pokeapi-Limit`, `X-RateLimit-Funtranslations-Limit`, and
        `X-RateLimit-Funtranslations-Remaining`.

        If a request failed before reaching Funtranslation,
        only `X-RateLimit-Funtranslations-Limit` will be present.
        '''

        # TODO: this should be refactored in more granular components

        # Check cache first
        if self.cache.get(pokemon_name) is not None:
            description_obj = json.loads(self.cache.get(pokemon_name))
            resp = make_response({
                'pokemon': pokemon_name,
                'description': description_obj['description']})
            resp.headers.extend({
                'Last-Modified': description_obj['created_at'],
                'Expires': description_obj['expires_at']
            })

            return resp

        pokemon_url = urljoin(
            ClientsConfig.POKEAPI_URL,
            pokemon_name,
            allow_fragments=True)

        # Get Pokemon family
        pokemon_req = util.check_pokeapi_request(pokemon_url)
        util.check_response(pokemon_req, api_name='Pokeapi')
        pokemon_body = validate_pokemon(pokemon_req)
        pokemon_family_url = pokemon_body['species']['url']

        # Get Pokemon description
        pokemon_family_req = util.check_pokeapi_request(pokemon_family_url)
        util.check_response(pokemon_family_req, api_name='Pokeapi')
        pokemon_family_body = validate_family(pokemon_family_req)
        pokemon_description = util.extract_description(pokemon_family_body)

        # Get translated description
        pokemon_translation_req = util.check_funtranslation_request(
            ClientsConfig.FUNTRANSLATION_URL,
            ClientsConfig.FUNTRANSLATION_KEY,
            pokemon_description
        )
        util.check_response(pokemon_translation_req, api_name='Funtranslation')
        pokemon_traslate_body = validate_translation(pokemon_translation_req)

        # Set cache
        util.set_description_cache(
            self.cache, pokemon_name, pokemon_traslate_body)

        headers = util.get_limit_header(pokemon_translation_req)
        resp = make_response({
            'pokemon': pokemon_name,
            'description': pokemon_traslate_body['contents']['translated']})
        resp.headers.extend(headers)
        return resp
