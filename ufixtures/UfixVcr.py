import vcr
import re
from typing import List, Dict


class UfixVcr(object):
    def __init__(self, cassette_dir: str, **kwargs):
        '''
        Instantiate a vcrpy cassette.
        :param cassette_dir: str. Cassette output dir
        :param kwargs: Dict. Kwargs to pass to the vcr object
        '''
        self.settings = {
            'serializer': 'yaml',
            'cassette_library_dir': cassette_dir,
            'record_mode': 'once'
        }
        self.settings.update(**kwargs)

    def sanitize(self, attributes: List = None, targets: List = None) -> vcr.VCR:
        '''
        Sanitizes all parts of request and response
        :param attributes: List. Keys in a request or response. Accepts regex strings
        :param targets: List. Values in a equest or response. Accepts regex strings
        :return:
        '''
        self.settings.update({
            'before_record_request': self._request_sanitizer_factory(attributes, targets),
            'before_record_response': self._response_sanitizer_factory(attributes, targets)
        })
        return vcr.VCR(**self.settings)

    def _request_sanitizer_factory(self, attributes: List = None, targets: List = None):
        def _sanitize(request):
            if request is None:
                return None
            parsed_request = request._to_dict()
            updated_parsed_request = self._dict_sanitizer(parsed_request, attributes, targets)
            updated_request = request._from_dict(updated_parsed_request)
            return updated_request

        return _sanitize

    def _response_sanitizer_factory(self, attributes: List = None, targets: List = None):
        def _sanitize(response):
            if response is None:
                return None
            updated_parsed_response = self._dict_sanitizer(response, attributes, targets)
            return updated_parsed_response

        return _sanitize

    def _dict_sanitizer(self, unsanitized: Dict, attributes: List = None, targets: List = None) -> Dict:
        none_placeholder = ['RandomStringThatIsVeryUnlikelyToExist']
        attributes = attributes if attributes is not None else none_placeholder
        targets = targets if targets is not None else none_placeholder
        attribute_regexes = [re.compile(s) for s in attributes]
        target_regexes = [re.compile(s) for s in targets]
        sanitized = self._unpacker(unsanitized, attribute_regexes, target_regexes)
        return sanitized

    def _unpacker(self, hash_type, attributes, targets):
        for i in hash_type:
            if isinstance(hash_type[i], dict):
                hash_type.update({i: self._unpacker(hash_type[i], attributes, targets)})
            else:
                try:
                    hash_type[i] = 'OBSCURED' if any([x.search(i) for x in attributes]) else hash_type[i]
                    for target in targets:
                        hash_type[i] = target.sub('OBSCURED', hash_type[i])
                except TypeError:
                    continue
        return hash_type
