# Crontab Lexer for Pygments

This project provides a custom **Pygments lexer** for highlighting Unix crontab files, including:

- User crontabs (`crontab -e`)
- System-wide crontabs (`/etc/crontab`, `/etc/cron.d/*`)
- `@`-directives (`@reboot`, `@daily`, etc.)
- Extended parsing for:
  - Minutes, hours, days, months, weekdays
  - Ranges, lists, steps, and wildcards
  - Month and weekday names (`jan`, `feb`, `mon`, `sun`, …)

## Features

- Full syntax highlighting support for all crontab formats
- Proper tokenization of time fields (including ranges and names)
- Works in MediaWiki with the `SyntaxHighlight` extension
- Distributed as a Python package with Pygments plugin entry point

---

# Installation on Ubuntu 22.04

Follow these steps to install and activate the custom lexer.

## 1. Clone the repository

```bash
git clone https://github.com/b3-it/pygements-lexer-crontab
cd pygements-lexer-crontab
```

## 2. (Recommended) Use a Python virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## 3. Install the lexer package

```bash
pip install .
```

or for development mode:

```bash
pip install -e .
```

## 4. Test the lexer using pygmentize

```bash
pygmentize -L lexers | grep -i crontab
```

You should see:

```
* crontab:
    Crontab
```

Test syntax highlighting:

```bash
pygmentize -l crontab -f terminal256 -O style=monokai tests/test.cron
```

---

# Using the Lexer in MediaWiki

MediaWiki does **not automatically** detect new Pygments lexers.  
You must point MediaWiki to your `pygmentize` binary and refresh the lexer list.

## 1. Edit `LocalSettings.php`

```php
$wgPygmentizePath = '/full/path/to/pygmentize';
```

Example:

```php
$wgPygmentizePath = '/home/username/crontab-lexer/.venv/bin/pygmentize';
```

## 2. Regenerate the MediaWiki lexer list

This step is required once after installation:

```bash
cd path/to/mediawiki/extension/syntaxhighlight
php maintenance/updateLexerList.php
```

After this, the `crontab` language becomes available in `<syntaxhighlight>`.

## 3. Usage example in MediaWiki

```wiki
<syntaxhighlight lang="crontab">
*/5 * * * * /usr/local/bin/backup.sh
</syntaxhighlight>
```

---

# Uninstallation

From your environment:

```bash
pip uninstall crontab-lexer
```

If you want to remove the lexer from MediaWiki:

1. Remove or comment out `$wgPygmentizePath`.
2. Regenerate the lexer list again:

```bash
cd path/to/mediawiki/extension/syntaxhighlight
php maintenance/updateLexerList.php
```

---

# License

MIT License.
