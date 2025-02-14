#!/usr/bin/python3
"""
Comprehensive unit tests for the BaseModel class.
Tests cover initialization, method functionality, edge cases,
and storage interactions.
"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from unittest.mock import patch
import json
import os


class TestBaseModel(unittest.TestCase):
    """Comprehensive test cases for the BaseModel class."""

    def setUp(self):
        """Set up test cases."""
        self.base_model = BaseModel()
        # Ensure clean test environment
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_init_no_args(self):
        """Test initialization without arguments."""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_init_with_dict(self):
        """Test initialization with dictionary."""
        test_dict = {
            'id': '123',
            'created_at': '2024-01-01T00:00:00',
            'updated_at': '2024-01-01T00:00:00',
            'name': 'test_model'
        }
        model = BaseModel(**test_dict)
        self.assertEqual(model.id, '123')
        self.assertEqual(model.name, 'test_model')
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_str_representation(self):
        """Test string representation of the model."""
        model_str = str(self.base_model)
        self.assertIn("[BaseModel]", model_str)
        self.assertIn(self.base_model.id, model_str)

    def test_save_method(self):
        """Test save method updates the updated_at attribute."""
        old_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(old_updated_at, self.base_model.updated_at)

    def test_to_dict_method(self):
        """Test conversion to dictionary."""
        model_dict = self.base_model.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        self.assertEqual(model_dict['id'], self.base_model.id)

    def test_from_dict_datetime_conversion(self):
        """Test datetime string conversion when creating from dictionary."""
        test_dict = {
            'id': '123',
            'created_at': '2024-01-01T00:00:00',
            'updated_at': '2024-01-01T00:00:00'
        }
        model = BaseModel(**test_dict)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    @patch('models.storage')
    def test_save_storage_interaction(self, mock_storage):
        """Test interaction with storage during save."""
        self.base_model.save()
        mock_storage.save.assert_called_once()

    def test_invalid_datetime_format(self):
        """Test handling of invalid datetime format."""
        test_dict = {
            'id': '123',
            'created_at': 'invalid_datetime',
            'updated_at': '2024-01-01T00:00:00'
        }
        with self.assertRaises(ValueError):
            BaseModel(**test_dict)

    def test_extra_attributes(self):
        """Test handling of extra attributes."""
        self.base_model.extra_attr = "extra"
        model_dict = self.base_model.to_dict()
        self.assertIn('extra_attr', model_dict)
        self.assertEqual(model_dict['extra_attr'], 'extra')


if __name__ == '__main__':
    unittest.main()
