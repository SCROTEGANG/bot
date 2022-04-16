from datetime import timedelta
import re

PRONOUNS = [
    "they/them",
    "she/her",
    "he/him",
    "they/she",
    "they/he",
]

PRONOUN_RE = re.compile(r"\w+\/\w+")


def delta_to_human(td: timedelta) -> str:
    if td.total_seconds() == 0:
        return "0 seconds"

    s = ""
    hours = td.seconds//3600
    minutes = (td.seconds//60) % 60

    if td.days > 0:
        if td.days == 1:
            s = "1 day"
        else:
            s = f"{td.days} days"

    if hours > 0:
        if td.days > 0:
            s = s + ", "

        if hours == 1:
            s = s + "1 hour"
        else:
            s = s + f"{hours} hours"

    if minutes > 0:
        if hours > 0 or td.days > 0:
            s = s + ", "

        if minutes == 1:
            s = s + "1 minute"
        else:
            s = s + f"{minutes} minutes"

    if s == "":
        if td.seconds > 0:
            if td.seconds == 1:
                s = "1 second"
            else:
                s = f"{td.seconds} seconds"

    return s
