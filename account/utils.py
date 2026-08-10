import logging
from datetime import timedelta
from typing import Any, Dict, List, Optional

import jwt
import requests
from jwt import PyJWKClient
from PIL import Image
from django.conf import settings
from django.utils import timezone
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

logger = logging.getLogger(__name__)

# Cached JWKS client for Apple's signing keys (fetches/refreshes keys as needed).
_apple_jwk_client = PyJWKClient("https://appleid.apple.com/auth/keys")


def _allowed_audiences(setting_name: str) -> List[str]:
    """Comma-separated client IDs configured in settings/.env, e.g. web,ios,android."""
    raw = getattr(settings, setting_name, "") or ""
    return [aud.strip() for aud in raw.split(",") if aud.strip()]


def get_otp_expiry(minutes: int = 30) -> timezone.datetime:
    return timezone.now() + timedelta(minutes=minutes)


def validate_image(image: Any) -> None:
    max_size = 3 * 1024 * 1024
    allowed_formats = {"JPEG", "PNG", "GIF"}
    if image.size > max_size:
        raise ValueError("Image too large (max 3MB)")
    try:
        img = Image.open(image)
        img.verify()
        if img.format not in allowed_formats:
            raise ValueError(f"Unsupported image format: {img.format}")
    except (OSError, ValueError) as e:
        raise ValueError(f"Invalid image file: {e}")


def decode_apple_token(identity_token: str) -> Optional[Dict[str, str]]:
    """Verify an Apple `identity_token` against Apple's public keys and return profile data.
    """
    try:
        allowed_audiences = _allowed_audiences("APPLE_CLIENT_ID")
        signing_key = _apple_jwk_client.get_signing_key_from_jwt(identity_token)
        decoded = jwt.decode(
            identity_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=allowed_audiences or None,
            issuer="https://appleid.apple.com",
            options={"verify_aud": bool(allowed_audiences)},
        )
        email = decoded.get("email")
        if not email:
            return None
        return {"email": email, "full_name": decoded.get("name", email.split("@")[0]), "profile_pic_url": None}
    except Exception:
        logger.exception("Failed to verify Apple identity token")
        return None


def decode_google_token(id_token: str) -> Optional[Dict[str, str]]:
    """Verify a Google `id_token` signature/issuer/audience and return profile data.
    """
    try:
        allowed_audiences = _allowed_audiences("GOOGLE_CLIENT_ID")
        idinfo = google_id_token.verify_oauth2_token(id_token, google_requests.Request())
        if idinfo.get("iss") not in ("accounts.google.com", "https://accounts.google.com"):
            return None
        if allowed_audiences and idinfo.get("aud") not in allowed_audiences:
            logger.warning("Rejected Google token for unrecognized audience: %s", idinfo.get("aud"))
            return None
        email = idinfo.get("email")
        if not email or not idinfo.get("email_verified", False):
            return None
        return {"email": email, "full_name": idinfo.get("name", ""), "profile_pic_url": idinfo.get("picture")}
    except Exception:
        logger.exception("Failed to verify Google id token")
        return None


def decode_facebook_token(access_token: str) -> Optional[Dict[str, Any]]:
    try:
        data = requests.get(
            f"https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}", timeout=3
        ).json()
        if "error" in data:
            return None
        return data
    except Exception:
        return None


def decode_microsoft_token(access_token: str) -> Optional[Dict[str, str]]:
    try:
        res = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=3
        ).json()
        email = res.get("mail") or res.get("userPrincipalName")
        if not email:
            return None
        return {"email": email, "full_name": res.get("displayName", ""), "profile_pic_url": None}
    except Exception:
        return None
