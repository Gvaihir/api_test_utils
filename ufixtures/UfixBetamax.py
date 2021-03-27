from betamax.cassette import cassette
from betamax import Betamax
from betamax_serializers import pretty_json
import os
from typing import Dict, Callable
from requests import Session


class UfixBetamax(object):
    def __init__(self, session: Session, cassette_dir: str):

        self.vcr = Betamax(session)
        self.vcr.register_serializer(pretty_json.PrettyJSONSerializer)
        if not os.path.exists(cassette_dir):
            os.makedirs(cassette_dir)
        with self.vcr.configure() as config:
            config.cassette_library_dir = cassette_dir
            config.default_cassette_options['serialize_with'] = 'prettyjson'

    def sanitize(self, target_field: str):
        with self.vcr.configure() as config:
            config.before_record(callback=self._sanitizer_factory(target_field))
        return self.vcr

    def _sanitizer_factory(self, target_field: str) -> Callable:
        def _sanitize_token(interaction: Dict, current_cassette: cassette) -> None:
            if interaction.data['response']['status']['code'] != 200:
                return
            headers = interaction.data['request']['headers']
            to_obscure = headers.get(target_field)[0]
            if to_obscure is None:
                return
            current_cassette.placeholders.append(
                cassette.Placeholder(placeholder='<OBSCURED>', replace=to_obscure)
            )

        return _sanitize_token
