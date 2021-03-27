from unittest import TestCase
import os
from ufixtures.UfixVcr import *
import boto3
import yaml

curr_dir = os.path.dirname(os.path.realpath(__file__))


class TestUfixVcr(TestCase):
    def setUp(self) -> None:
        self.ufixtures = UfixVcr(os.path.join(curr_dir, 'fixtures/cassettes'))

    def test__sanitizer_factories(self):
        session = boto3.Session(profile_name='gvaihir')
        s3 = session.resource('s3')
        s3_obj = s3.Object('ucsf-genomics-prod-project-data', 'anton/scito/mock/fastq/config_test.ini')
        with self.ufixtures.vcr.use_cassette('UfixVcr__sanitizer_factory.yml',
                                             before_record_request=self.ufixtures._request_sanitizer_factory(['X-Amz', 'Author', 'User'],['anton']),
                                             before_record_response=self.ufixtures._response_sanitizer_factory(['x-amz'],['kms'])
                                             ):
            content_length = s3_obj.content_length
        with open(os.path.join(curr_dir, 'fixtures/cassettes/UfixVcr__sanitizer_factory.yml'), 'r') as f:
            fixture = yaml.safe_load(f)
            self.assertTrue(isinstance(fixture, dict))
            self.assertEqual(fixture['interactions'][0]['request']['headers']['X-Amz-Date'][0], 'OBSCURED')
            self.assertTrue("OBSCURED" in fixture['interactions'][0]['request']['uri'])
            self.assertFalse("anton" in fixture['interactions'][0]['request']['uri'])

    def test_sanitize(self):
        session = boto3.Session(profile_name='gvaihir')
        s3 = session.resource('s3')
        s3_obj = s3.Object('ucsf-genomics-prod-project-data', 'anton/scito/mock/fastq/config_test.ini')
        vcr = self.ufixtures.sanitize(attributes=['(?i)X-Amz', 'Author', 'User'],
                                      targets=['anton'])
        with vcr.use_cassette('UfixVcr_sanitize.yml'):
            content_length = s3_obj.content_length
        with open(os.path.join(curr_dir, 'fixtures/cassettes/UfixVcr_sanitize.yml'), 'r') as f:
            fixture = yaml.safe_load(f)
            self.assertTrue(isinstance(fixture, dict))
            self.assertEqual(fixture['interactions'][0]['request']['headers']['X-Amz-Date'][0], 'OBSCURED')
            self.assertTrue("OBSCURED" in fixture['interactions'][0]['request']['uri'])
            self.assertFalse("anton" in fixture['interactions'][0]['request']['uri'])

