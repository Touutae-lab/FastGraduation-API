import re
from typing import Any, Dict, List, Literal, Tuple, Union


def _check_language(
    txt: (str or int), lang: Union[Literal["th"], Literal["en"], Literal["dt"]]
) -> bool:
    regex = {
        "en": re.compile("^[a-zA-Z]+$", re.IGNORECASE),  # create regex object
        "th": re.compile("^[ก-ฮ]+$", re.IGNORECASE),
        "dt": re.compile("^[0-9]+$", re.IGNORECASE),
    }

    match_result = regex[lang].findall(txt)
    if match_result == []:
        return False
    return match_result[0] == txt


def _check_digit(value: int, key) -> bool:
    check = {
        "year": len(str(value)) == 4,
        "term": 0 <= value <= 1,
        "credit": 1 <= value <= 4,
        "course": len(str(value)) == 6,
    }
    if key in check:
        return check[key]


def validate(listlang: List[str], data: Dict[str, Any]) -> Tuple[bool, str]:
    # msg=""
    missing_msg = "Missing value %s"

    field_label = {
        "fname_en": "First Name (English)",
        "lname_en": "Last Name (English)",
        "mname_en": "Mid Name (English)",
        "course_name_en": "Course Name (English)",
        "description_en": "Description (English)",
        "fname_th": "First Name (Thai)",
        "mname_th": "Min Name (Thai)",
        "lname_th": "Last Name (Thai)",
        "course_name_th": "Course Name (Thai)",
        "description_th": "Description (Thai)",
        "name_th": "Name (Thai)",
        "name_en": "Name (English)",
    }
    digit_label = {
        "year_start": "start year ",
        "year_end": "end year ",
        "cousre_id_pre": "precousre id",
        # "pregroup_id":"pregroup id ",
        "credit_": "credit",
        "course_id": "course id ",
        "Term_one": "term one",
        "Term_two": "term two",
        "Term_summer": " term summer",
    }

    # check null and language
    for field in listlang:
        fieldval = data.get(field)

        if field in field_label:
            if fieldval is None:
                return False, missing_msg % field_label[field]
            if field[-2:] in {"th", "en"}:
                if not _check_language(fieldval, field[-2:]):
                    return False, ("Invalid language: " + field_label[field])
            continue
        elif field in digit_label:
            filed_key = field.split("_")
            if fieldval is None:
                return False, missing_msg % digit_label[field]
            if type(fieldval) != int:
                return False, ("Invalid language: " + digit_label[field])
            if not _check_digit(fieldval, filed_key[0]):
                return False, ("Invalid language: " + digit_label[field])
            continue

    return True, "success"
