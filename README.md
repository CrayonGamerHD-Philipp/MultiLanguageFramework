
# MultiLanguageFramework

**MultiLanguageFramework** is a Python framework that allows you to manage multi-language messages using YAML configuration files. It dynamically creates and updates language files and enables switching between languages or setting defaults.

## Features

- **Automatic YAML language file creation**: Automatically generates and manages language files in `.yml` format.
- **Dynamic language switching**: Change the current language at runtime with a simple method.
- **Message key management**: Retrieve messages using keys, with fallback support if translations are missing.
- **Language-specific retrieval**: Optionally retrieve messages in specific languages, regardless of the current global language.
- **Persistent storage**: Translations are stored in `.yml` files, which can be modified and extended easily.
- **Language name in YAML files**: Each language file contains the full name of the language (e.g., "GERMAN"). When creating new files, "LANGUAGE_NAME" is used as a placeholder for the full language name.

## Installation

Install the package directly from this GitHub repository:

```bash
pip install git+https://github.com/CrayonGamerHD-Philipp/MultiLanguageFramework.git
```

Ensure that all dependencies are installed automatically.

## Usage

### Initialize the Language Manager

```python
from language_manager import LanguageManager

# Initialize with a default language (e.g. 'de_DE')
language_manager = LanguageManager(default_language='de_DE')
```

### Retrieving Messages

Retrieve a message by specifying its key and a fallback message:

```python
print(language_manager.get_message('welcome.message', 'Hallo, willkommen in diesem Programm!'))
```

### Switching Languages

You can change the current language for all subsequent messages using `set_language`.

```python
language_manager.set_language('en_US')
print(language_manager.get_message('welcome.message', 'Welcome to this program!'))
```

### Language-Specific Retrieval

Retrieve a message in a specific language without changing the global language setting:

```python
print(language_manager.get_message('welcome.message', 'Hallo, willkommen in diesem Programm!', 'de_DE'))
```

### Retrieving Messages with Placeholders

You can use placeholders like {name} in your messages, and the placeholders will be replaced by variables from the current scope. For example:

```python
name = "Philipp"
print(language_manager.get_message('welcome.message', 'Hallo {name}, willkommen in diesem Programm!'))
```

### Retrieving Messages Without Fallback

You can now retrieve a message without specifying a fallback message. If the key does not exist in the language file and no fallback is provided, the system will raise an error. This is useful when you want to enforce that all messages must exist in the language files.

#### Example:

```python
message = language_manager.get_message('welcome.message')
```

If the key `'welcome.message'` does not exist, an error will be raised:

```
ValueError: Message key 'welcome.message' not found and no fallback message provided.
```

### File Structure

Language files are stored in the `language` directory. These are created automatically the first time a message key is accessed, and they are named using the language code (e.g. `de_DE.yml`, `en_US.yml`).

Each language file also contains the full name of the language (e.g., "GERMAN").

Example structure of a `de_DE.yml` file:

```yaml
language: de_DE
language_name: "GERMAN"
version: 1.0
welcome.message: "Hallo, willkommen in diesem Programm!"
```

### Listing Available Languages

You can retrieve a list of available languages and their full names using the following methods:

```python
# List of available languages and their names
available_languages = language_manager.get_available_languages()
print(available_languages)  # [('de_DE', 'GERMAN'), ('en_US', 'ENGLISH')]

# List of full language names
language_names = language_manager.get_language_names()
print(language_names)  # ['GERMAN', 'ENGLISH']
```

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or additional features. All contributions are welcome!

## License

This project is licensed under the MIT License.
