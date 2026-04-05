FEATURE_COLUMNS = [
    "profile pic",
    "nums/length username",
    "fullname words",
    "nums/length fullname",
    "name==username",
    "description length",
    "external URL",
    "private",
    "#posts",
    "#followers",
    "#follows",
]

def validate_manual_features(features: dict) -> dict:
    missing = [col for col in FEATURE_COLUMNS if col not in features]
    if missing:
        raise ValueError(f"Missing feature(s): {missing}")

    cleaned = {}
    for col in FEATURE_COLUMNS:
        try:
            cleaned[col] = int(features[col])
        except Exception:
            raise ValueError(f"Invalid value for '{col}'")

    return cleaned