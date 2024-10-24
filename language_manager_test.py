import unittest
import os
import yaml
from language_manager import LanguageManager


class TestLanguageManager(unittest.TestCase):
    def setUp(self):
        """Set up the test environment by initializing the LanguageManager"""
        self.language_manager = LanguageManager(default_language='en_US')
        # Ensure the language directory is cleaned before each test
        self.clean_language_dir()

    def tearDown(self):
        """Clean up after tests."""
        self.clean_language_dir()

    def clean_language_dir(self):
        """Remove all language files"""
        if os.path.exists(self.language_manager.language_dir):
            for file_name in os.listdir(self.language_manager.language_dir):
                os.remove(os.path.join(self.language_manager.language_dir, file_name))

    def test_create_language_file(self):
        """Test if a new language file is created correctly with default values"""
        key = 'welcome.message'
        fallback_message = 'Welcome to the program!'

        # Call the method to create the language file
        self.language_manager.create_language_file(key, fallback_message)

        # Check if the file was created
        file_path = f'{self.language_manager.language_dir}/{self.language_manager.default_language}.yml'
        self.assertTrue(os.path.exists(file_path))

        # Load the file and verify its contents
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            self.assertEqual(data[key], fallback_message)
            self.assertEqual(data['language_name'], 'LANGUAGE_NAME')

    def test_get_message_with_fallback(self):
        """Test retrieving a message with a fallback if the message doesn't exist"""
        message = self.language_manager.get_message('welcome.message', 'Welcome to the program!')
        self.assertEqual(message, 'Welcome to the program!')

    def test_get_message_with_formatting(self):
        """Test message retrieval with placeholder formatting"""
        key = 'greeting.message'
        fallback_message = 'Hello {name}, welcome to the game!'
        message = self.language_manager.get_message(key, fallback_message, name="Philipp")
        self.assertEqual(message, 'Hello Philipp, welcome to the game!')

    def test_set_language(self):
        """Test set the language"""
        self.language_manager.set_language('de_DE')
        self.assertEqual(self.language_manager.current_language, 'de_DE')

    def test_append_to_language_file(self):
        """Test appending new keys to an existing language file."""
        key = 'new.message'
        message = 'This is a new message.'

        self.language_manager.create_language_file(key, message)
        self.language_manager.append_to_language_file(self.language_manager.default_language, 'another.message',
                                                      'Another message')

        file_path = f'{self.language_manager.language_dir}/{self.language_manager.default_language}.yml'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            self.assertIn('another.message', data)
            self.assertEqual(data['another.message'], 'Another message')

    def test_get_available_languages(self):
        """Test retrieving available languages."""
        self.language_manager.create_language_file('welcome.message', 'Welcome!')
        available_languages = self.language_manager.get_available_languages()
        self.assertIn(('en_US', 'LANGUAGE_NAME'), available_languages)

    def test_get_language_names(self):
        """Test retrieving language names."""
        self.language_manager.create_language_file('welcome.message', 'Welcome!')
        language_names = self.language_manager.get_language_names()
        self.assertIn('LANGUAGE_NAME', language_names)


if __name__ == '__main__':
    unittest.main()
