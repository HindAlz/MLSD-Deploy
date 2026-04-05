from urllib.parse import urlparse
import re
import snscrape.modules.twitter as sntwitter


def extract_x_username(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if host not in {"x.com", "www.x.com", "twitter.com", "www.twitter.com"}:
        raise ValueError("Only X/Twitter profile URLs are supported")

    if not path:
        raise ValueError("Invalid profile URL")

    username = path.split("/")[0]

    if username.lower() in {"home", "explore", "search", "i", "settings"}:
        raise ValueError("URL does not look like a profile URL")

    if not re.fullmatch(r"[A-Za-z0-9_]{1,15}", username):
        raise ValueError("Invalid X/Twitter username")

    return username


def fetch_x_profile_from_url(url: str) -> dict:
    username = extract_x_username(url)

    scraper = sntwitter.TwitterUserScraper(username)
    user = next(scraper.get_items(), None)

    if user is None:
        raise ValueError("Profile not found or could not be fetched")

    # Map scraped fields into your model schema
    return {
        "username_raw": getattr(user, "username", "") or "",
        "fullname_raw": getattr(user, "displayname", "") or "",
        "bio_raw": getattr(user, "description", "") or "",
        "profile pic": int(bool(getattr(user, "profileImageUrl", None))),
        "external URL": int(bool(getattr(user, "link", None))),
        "private": int(bool(getattr(user, "protected", False))),
        "#posts": int(getattr(user, "statusesCount", 0) or 0),
        "#followers": int(getattr(user, "followersCount", 0) or 0),
        "#follows": int(getattr(user, "friendsCount", 0) or 0),
    }