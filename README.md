# FHEM Client

If you want a very simple client for your FHEM installation which reads some values
and outputs them in a formatted way, this is for you. Basically this is how it works:

1. Checkout this project to your computer (or just copy `main.py` and `config-template.ini`).
2. Copy `config-template.ini` to `config.ini` and edit it so it contains your FHEM login data,
   the requests you want the script to make and the formatted output containing the values.
3. Call `main.py` with at least Python 3.2 installed.

## Example

When using the formatted output from `config-template.ini`, this is what the script could print
(given FHEM has the configured devices and parameters):

```
Temperature: 23.5 °C
Humidity: 47 %
```

## Notes regarding the output configured in `config.ini`

- If you want a single percent sign (`%`), you have to write a double percent sign (`%%`).
- If you want multiline output, you have to indent the second to the last line by 4 spaces each.
- You can include Python snippets inside the curly braces if you want (example in `config-template.ini`).
