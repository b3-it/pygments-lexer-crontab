import re

from pygments.lexer import RegexLexer, bygroups, using
from pygments.token import (
    Text, Comment, Name, Keyword, Number, Operator, String, Punctuation
)


class CronFieldLexer(RegexLexer):
    """
    Lexer for a single cron time field (e.g., "*/5,1-10/2,jan,fri").
    Decomposed into:
    - Numbers
    - Month and weekday names (jan, feb, ... / sun, mon, ...)
    - Operators (*, /, -)
    - List separators (,)
    """
    name = "CronField"
    flags = re.IGNORECASE

    tokens = {
        "root": [
            # bekannte Monatsnamen
            (r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b",
             Name.Constant),

            # bekannte Wochentagsnamen
            (r"\b(sun|mon|tue|wed|thu|fri|sat)\b",
             Name.Constant),

            # Zahlen
            (r"\d+", Number),

            # Operatoren in Feldern
            (r"[\*/-]", Operator),

            # Listen-Trenner
            (r",", Punctuation),

            # sonstige Wörter (falls jemand etwas exotisches reinschreibt)
            (r"[A-Za-z_][A-Za-z0-9_]*", Name),

            # alles andere als neutraler Text
            (r".", Text),
        ],
    }


class CrontabLexer(RegexLexer):
    """
    Lexer for crontab files.

    Supports:
    - Comments (# ...)
    - Environment lines (FOO=bar)
    - User crontabs with 5 time fields + command
	- System-wide crontabs (/etc/crontab, /etc/cron.d/*) with:
		Minute Hour Day Month Weekday USER Command
	- @ directives (@reboot, @daily, ...)
		- Time fields with:
			* Numbers, *, ranges (1-5), lists (1,2,3), steps (*/5)
			* Month names (jan–dec) and weekday names (sun–sat)
    """

    name = "Crontab"
    aliases = ["crontab"]
    filenames = ["crontab", "cron.*", "crontab.*", "/etc/crontab"]
    mimetypes = ["text/x-crontab"]

    tokens = {
        "root": [
            # Leerzeilen
            (r"\s+\n", Text),

            # Kommentarzeilen
            (r"\s*#.*\n", Comment),

            # Environment-Zeilen: FOO=bar
            (
                r"^(\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*)(=)(\s*)(.*?)(\n)",
                bygroups(Text, Name.Variable, Text, Operator, Text, String, Text),
            ),

            # @-Direktiven: @reboot, @yearly, @daily, ...
            (
                r"^(\s*)(@\w+)(\s+)(.+?)(\n)",
                bygroups(Text, Keyword, Text, String, Text),
            ),

            # ------------------------------------------------------------
            # Systemweite Crontabs: 5 Zeitfelder + USER + Kommando
            # Minute Hour DayOfMonth Month DayOfWeek User Command
            # ------------------------------------------------------------
            (
                r"^(\s*)"                                    # 1: leading space
                r"([^\s]+)(\s+)"                             # 2-3: minute
                r"([^\s]+)(\s+)"                             # 4-5: hour
                r"([^\s]+)(\s+)"                             # 6-7: day of month
                r"([^\s]+)(\s+)"                             # 8-9: month
                r"([^\s]+)(\s+)"                             # 10-11: day of week
                r"([^\s]+)(\s+)"                             # 12-13: user
                r"(.*?)(\n)",                                # 14-15: command
                bygroups(
                    Text,
                    using(CronFieldLexer), Text,   # minute
                    using(CronFieldLexer), Text,   # hour
                    using(CronFieldLexer), Text,   # day of month
                    using(CronFieldLexer), Text,   # month
                    using(CronFieldLexer), Text,   # day of week
                    Name.Builtin, Text,           # user
                    String, Text                  # command
                ),
            ),

            # ------------------------------------------------------------
            # Benutzer-Crontabs: 5 Zeitfelder + Kommando
            # Minute Hour DayOfMonth Month DayOfWeek Command
            # ------------------------------------------------------------
            (
                r"^(\s*)"                                    # 1: leading space
                r"([^\s]+)(\s+)"                             # 2-3: minute
                r"([^\s]+)(\s+)"                             # 4-5: hour
                r"([^\s]+)(\s+)"                             # 6-7: day of month
                r"([^\s]+)(\s+)"                             # 8-9: month
                r"([^\s]+)(\s+)"                             # 10-11: day of week
                r"(.*?)(\n)",                                # 12-13: command
                bygroups(
                    Text,
                    using(CronFieldLexer), Text,   # minute
                    using(CronFieldLexer), Text,   # hour
                    using(CronFieldLexer), Text,   # day of month
                    using(CronFieldLexer), Text,   # month
                    using(CronFieldLexer), Text,   # day of week
                    String, Text                   # command
                ),
            ),

            # Fallback: alles andere als normaler Text
            (r".+?\n", Text),
        ],
    }

