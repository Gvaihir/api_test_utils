import vcr
import re
from typing import List

class UfixVcr(object):
    def __init__(self, cassette_dir: str, **kwargs):
        settings = {
            'serializer': 'yaml',
            'cassette_library_dir': cassette_dir,
            'record_mode': 'once'
        }
        settings.update(**kwargs)
        self.vcr = vcr.VCR(**settings)

    def sanitize(self, headers: List, replacement: str='OBSCURED by Ufixtures') -> vcr.VCR:
        settings = self.vcr.get_merged_config(**{'filter_headers': [(x, replacement) for x in headers]})
        return vcr.VCR(**settings)


    def _request_sanitizer_factory(self, attributes: List, targets: List):
        def _sanitize(request):
            if request == None:
                return None
            parsed_request = request._to_dict()
            attribute_regexes = [re.compile(s) for s in attributes]
            target_regexes = [re.compile(s) for s in targets]
            updated_parsed_request = self._unpacker(parsed_request, attribute_regexes, target_regexes)
            updated_request = request._from_dict(updated_parsed_request)
            return updated_request
        return _sanitize


    def _response_sanitizer_factory(self, attributes: List, targets: List):
        def _sanitize(response):
            if response == None:
                return None
            attribute_regexes = [re.compile(s) for s in attributes]
            target_regexes = [re.compile(s) for s in targets]
            updated_parsed_response = self._unpacker(response, attribute_regexes, target_regexes)
            return updated_parsed_response
        return _sanitize


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


