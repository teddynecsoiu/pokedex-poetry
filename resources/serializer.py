import json
import logging

from flask_restful import abort
from marshmallow import Schema, fields, EXCLUDE, ValidationError


class PokemonSpeciesSchema(Schema):
    url = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class PokemonSchema(Schema):
    species = fields.Nested(
        PokemonSpeciesSchema,
        required=True
    )

    class Meta:
        unknown = EXCLUDE


class PokemonFlavorLanguageSchema(Schema):
    name = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class PokemonFlavorDescrSchema(Schema):
    flavor_text = fields.Str(required=True)
    language = fields.Nested(
        PokemonFlavorLanguageSchema,
        required=True)

    class Meta:
        unknown = EXCLUDE


class PokemonFamilySchema(Schema):
    flavor_text_entries = fields.List(
        fields.Nested(
            PokemonFlavorDescrSchema,
            required=True),
        required=True
    )

    class Meta:
        unknown = EXCLUDE


class TranslatedSchema(Schema):
    translated = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class TranslatedDescrSchema(Schema):
    contents = fields.Nested(
        TranslatedSchema,
        required=True
    )

    class Meta:
        unknown = EXCLUDE


def validate_pokemon(pokemon_req):
    '''
    Validate dictionaly agains PokemonSchema
    by deserializing using Marshmallow.

    Based on schema configuration, uknown properties
    are removed leaving only a validated dictionaly.
    '''
    try:
        return PokemonSchema().load(pokemon_req.json())
    except ValidationError as error:
        logging.error('PokemonSchema validation failed!', error)

        # This erorr is a internal issue, so it should not
        # be surfaced to the user.
        abort(500)


def validate_family(pokemon_family_req):
    '''
    Validate dictionaly agains PokemonFamilySchema
    by deserializing using Marshmallow.

    Based on schema configuration, uknown properties
    are removed leaving only a validated dictionaly.
    '''
    try:
        return PokemonFamilySchema().load(pokemon_family_req.json())
    except ValidationError as error:
        logging.error('PokemonFamilySchema validation failed!')

        # This erorr is a internal issue, so it should not
        # be surfaced to the user.
        abort(500)


def validate_translation(pokemon_translation_req):
    '''
    Validate dictionaly agains TranslatedDescrSchema
    by deserializing using Marshmallow.

    Based on schema configuration, uknown properties
    are removed leaving only a validated dictionaly.
    '''
    try:
        return TranslatedDescrSchema().load(pokemon_translation_req.json())
    except ValidationError as error:
        logging.error('TranslatedDescrSchema validation failed!')

        # This erorr is a internal issue, so it should not
        # be surfaced to the user.
        abort(500)
