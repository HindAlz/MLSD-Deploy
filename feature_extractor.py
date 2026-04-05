import re


def count_digits(text: str) -> int:
    return sum(ch.isdigit() for ch in (text or ""))


def word_count(text: str) -> int:
    text = (text or "").strip()
    return len(text.split()) if text else 0


def normalize_name(text: str) -> str:
    text = (text or "").lower().strip()
    return re.sub(r"[^a-z0-9]", "", text)


def extract_features_from_x_profile(profile: dict) -> dict:
    username = profile.get("username_raw", "") or ""
    fullname = profile.get("fullname_raw", "") or ""
    bio = profile.get("bio_raw", "") or ""

    return {
        "profile pic": int(profile.get("profile pic", 0)),
        "nums/length username": count_digits(username),
        "fullname words": word_count(fullname),
        "nums/length fullname": count_digits(fullname),
        "name==username": int(normalize_name(fullname) == normalize_name(username)),
        "description length": len(bio.strip()),
        "external URL": int(profile.get("external URL", 0)),
        "private": int(profile.get("private", 0)),
        "#posts": int(profile.get("#posts", 0)),
        "#followers": int(profile.get("#followers", 0)),
        "#follows": int(profile.get("#follows", 0)),
    }