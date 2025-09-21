#!/usr/bin/env python3
"""Unit tests for utils.py functions"""

import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test access_nested_map function"""

    def test_access_nested_map(self):
        """Test access_nested_map returns expected value"""
        self.assertEqual(access_nested_map({"a": 1}, ("a",)), 1)

    def test_access_nested_map_exception(self):
        """Test access_nested_map raises KeyError with correct key"""
        with self.assertRaises(KeyError) as context:
            access_nested_map({}, ("a",))
        self.assertEqual(str(context.exception), "'a'")


class TestGetJson(unittest.TestCase):
    """Test get_json function"""

    def test_get_json(self):
        """Test get_json returns expected dictionary"""
        test_url = "http://example.com"
        test_payload = {"payload": True}
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch("utils.requests.get", return_value=mock_response) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test memoize decorator"""

    def test_memoize(self):
        """Test memoized property calls method only once"""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()
        with patch.object(obj, "a_method", wraps=obj.a_method) as mock_method:
            result1 = obj.a_property
            result2 = obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
