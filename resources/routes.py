import json
import logging
from urllib.parse import urljoin 

import requests
from flask import make_response 
from flask_restful import Resource, abort

from config import ClientsConfig
from common.util import first, extract_description, check_response, get_limit_header
from .serializer import validate_pokemon, validate_family, validate_translation

pokemon_api_url = ClientsConfig.POKEAPI_URL
funtranslation_api_url = ClientsConfig.FUNTRANSLATION_URL
funtranslation_api_key = ClientsConfig.FUNTRANSLATION_KEY

class Pokemon(Resource):
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

        pokemon_url = urljoin(pokemon_api_url,pokemon_name, allow_fragments=True)

        # Get Pokemon family
        pokemon_req = requests.get(pokemon_url)
        check_response(pokemon_req, api_name='Pokeapi')
        pokemon_body = validate_pokemon(pokemon_req)
        pokemon_family_url = pokemon_body['species']['url']

        # Get Pokemon description
        pokemon_family_req = requests.get(pokemon_family_url)
        check_response(pokemon_family_req, api_name='Pokeapi')
        pokemon_family_body = validate_family(pokemon_family_req)
        pokemon_description = extract_description(pokemon_family_body)

        # Get translated description
        payload = {'text': pokemon_description}
        headers = {'x-funtranslations-api-secret': funtranslation_api_key}
        pokemon_translation_req = requests.post(
            funtranslation_api_url, data=json.dumps(payload), headers=headers)
        check_response(pokemon_translation_req,api_name='Funtranslation')
        pokemon_traslate_body = validate_translation(pokemon_translation_req)

        headers = get_limit_header(pokemon_translation_req)
        resp = make_response({
            'pokemon': pokemon_name, 
            'description': pokemon_traslate_body['contents']['translated']})
        resp.headers.extend(headers)
        return resp
