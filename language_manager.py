import os
import yaml

class LanguageManager:
    def __init__(self, default_language='en_US'):
        self.default_language = default_language
        self.current_language = default_language
        self.languages = {}
        self.language_dir = 'language'
        self.load_languages()

    def load_languages(self):
        """Load all language files from the language directory."""
        if not os.path.exists(self.language_dir):
            os.makedirs(self.language_dir)

        for file_name in os.listdir(self.language_dir):
            if file_name.endswith('.yml'):
                with open(os.path.join(self.language_dir, file_name), 'r', encoding='utf-8') as file:
                    lang_data = yaml.safe_load(file)
                    lang_code = file_name.split('.')[0]  # Extract language code from file name
                    self.languages[lang_code] = lang_data

    def create_language_file(self, key, fallback_message):
        """Create the default language file if it doesn't exist."""
        file_path = f'{self.language_dir}/{self.default_language}.yml'
        if not os.path.exists(file_path):
            lang_info = {
                'language': self.default_language,
                'version': '1.0',
                key: fallback_message
            }
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(lang_info, file, allow_unicode=True)
            self.languages[self.default_language] = lang_info
        else:
            self.load_languages()

    def get_message(self, key, fallback_message, language=None):
        """Retrieve message in the desired language or use fallback."""
        language = language or self.current_language

        if self.default_language not in self.languages:
            self.create_language_file(key, fallback_message)

        if language in self.languages:
            if key not in self.languages[language]:
                self.languages[self.default_language][key] = fallback_message
                self.update_language_file(self.default_language, key, fallback_message)
            return self.languages[language].get(key, fallback_message)
        else:
            return self.languages[self.default_language].get(key, fallback_message)

    def update_language_file(self, language_code, key, message):
        """Update an existing language file with new keys."""
        file_path = f'{self.language_dir}/{language_code}.yml'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                lang_data = yaml.safe_load(file)
                lang_data[key] = message

            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(lang_data, file, allow_unicode=True)

    def set_language(self, language_code):
        """Change the current language."""
        self.current_language = language_code


# Example usage
language_manager = LanguageManager(default_language='de_DE')

print(language_manager.get_message('welcome.message', 'Hallo, willkommen in diesem Programm!'))

language_manager.set_language('en_US')
print(language_manager.get_message('welcome.message', 'Welcome to this program!'))

print(language_manager.get_message('welcome.message', 'Hallo, willkommen in diesem Programm!', 'de_DE'))
