# DeepL Translator Script

This Python script allows you to translate the content of a source file into a specified language using the DeepL API. The script can be invoked via the command line with the required arguments.

## Requirements

- `Python 3.x`
- `deepl` library (install via `pip install deepl`)
- `PySide6` library (install via `pip install PySide6`)
- `json` (part of the standard library, no installation required)
- `argparse` (part of the standard library, no installation required)

## Usage

You can run the script from the command line as follows:

```bash
python translate.py <target_lang> <base_file> <auth_key>
```

The script will:
------
- Automatically translate all the file
- Open a graphic interface to correct in needed any translation
- Save the result in a `translated.json` file, ready to be used

## Arguments

- `<target_lang>`: The target language to which you want to translate (e.g., ES for Spanish, FR for French, DE for German, EN for English, IT for Italian, etc.).
- `<base_file>`: The source file in i18n-JSON format containing the text to translate (provide the relative path).
- `<auth_key>`: Your API key for accessing the DeepL API.

## Example

To translate a file named text_to_translate.json into French using your DeepL API key, you would run:

```bash
python translate.py FR text_to_translate.json your_deepL_api_key_here
```

## License

This project is licensed under the MIT License.