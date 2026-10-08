import unittest
from unittest.mock import Mock, patch

import requests
from toutatis import core


class ProfileErrorsTest(unittest.TestCase):
    @patch.object(core.requests, 'get')
    def test_profile_errors_have_consistent_shape(self, get):
        for status, payload in [(404, {}), (429, {}), (401, {}),
                                (403, {}), (200, {}),
                                (200, {'data': {'user': None}}), (200, [])]:
            with self.subTest(status=status, payload=payload):
                get.return_value = Mock(status_code=status)
                get.return_value.json.return_value = payload
                result = core.getInfo('example', 'dummy-session')
                self.assertIsNone(result['user'])
                self.assertTrue(result['error'])

    @patch.object(core.requests, 'get')
    def test_network_failure(self, get):
        get.side_effect = requests.exceptions.Timeout()
        self.assertTrue(core.getInfo('example', 'dummy-session')['error'])

    @patch.object(core.requests, 'get')
    def test_invalid_json(self, get):
        get.return_value = Mock(status_code=200)
        get.return_value.json.side_effect = ValueError('invalid JSON')
        self.assertTrue(core.getInfo('example', 'dummy-session')['error'])
        self.assertTrue(core.getInfo('123', 'dummy-session', 'id')['error'])

    @patch.object(core.requests, 'get')
    def test_success(self, get):
        profile = Mock(status_code=200)
        profile.json.return_value = {'data': {'user': {'id': '123'}}}
        info = Mock(status_code=200)
        info.json.return_value = {'user': {'username': 'example'}}
        get.side_effect = [profile, info]
        self.assertEqual(core.getInfo('example', 'dummy-session'),
                         {'user': {'username': 'example', 'userID': '123'},
                          'error': None})

    @patch('sys.argv', ['toutatis', '-u', 'example', '-s', 'dummy-session'])
    @patch.object(core, 'getInfo')
    def test_cli_exits_cleanly_on_lookup_error(self, get_info):
        get_info.return_value = {'user': None, 'error': 'Rate limit'}
        with self.assertRaises(SystemExit) as result:
            core.main()
        self.assertEqual(result.exception.code, 'Rate limit')
