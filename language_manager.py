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
                'language_name': 'LANGUAGE_NAME',  # Placeholder for language name
                'version': '1.0',
                key: fallback_message
            }
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(lang_info, file, allow_unicode=True)
            self.languages[self.default_language] = lang_info
        else:
            self.load_languages()

    def get_message(self, key, fallback_message=None, language=None):
        """Retrieve message in the desired language or use fallback. Format variables dynamically."""
        language = language or self.current_language

        if self.default_language not in self.languages:
            if fallback_message is None:
                raise ValueError(f"Message key '{key}' not found and no fallback message provided.")
            self.create_language_file(key, fallback_message)

        # Check if the message exists in the requested language
        if language in self.languages:
            if key not in self.languages[language]:
                if fallback_message is None:
                    raise ValueError(f"Message key '{key}' not found and no fallback message provided.")
                # Add missing keys to the default language file at the end
                self.languages[self.default_language][key] = fallback_message
                self.append_to_language_file(self.default_language, key, fallback_message)
            message = self.languages[language].get(key, fallback_message)
        else:
            if fallback_message is None:
                raise ValueError(f"Message key '{key}' not found and no fallback message provided.")
            message = self.languages[self.default_language].get(key, fallback_message)

        # Replace placeholders using local and global variables (i.e., variables in the current context)
        try:
            message = message.format(**{k: v for k, v in {**globals(), **locals()}.items() if k != 'self'})
        except KeyError as e:
            raise ValueError(f"Missing key for message formatting: {e}")

        return message

    def append_to_language_file(self, language_code, key, message):
        """Append a new key to the existing language file."""
        file_path = f'{self.language_dir}/{language_code}.yml'
        if os.path.exists(file_path):
            with open(file_path, 'a', encoding='utf-8') as file:  # 'a' mode appends to the file
                yaml.dump({key: message}, file, allow_unicode=True)

    def set_language(self, language_code):
        """Change the current language."""
        self.current_language = language_code

    def get_available_languages(self):
        """Return a list of available languages and their full names."""
        available_languages = []
        for lang_code, lang_data in self.languages.items():
            language_name = lang_data.get('language_name', 'UNKNOWN')
            available_languages.append((lang_code, language_name))
        return available_languages

    def get_language_names(self):
        """Return a list of the full names of the available languages."""
        language_names = []
        for lang_data in self.languages.values():
            language_name = lang_data.get('language_name', 'UNKNOWN')
            language_names.append(language_name)
        return language_names