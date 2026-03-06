from pathlib import Path

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError

ALLOWED_IMAGE_EXTENSIONS = {
    "svg",
    "png",
    "jpg",
    "jpeg",
    "webp",
    "gif",
    "bmp",
    "avif",
}


def _looks_like_svg(content: bytes) -> bool:
    if not content:
        return False

    payload = content.lstrip()
    if payload.startswith(b"\xef\xbb\xbf"):
        payload = payload[3:].lstrip()

    return b"<svg" in payload.lower()


def validate_image_or_svg(uploaded_file) -> None:
    extension = Path(uploaded_file.name or "").suffix.lower().lstrip(".")
    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationError(
            "Allowed formats: SVG, PNG, JPG, JPEG, WEBP, GIF, BMP, AVIF."
        )

    uploaded_file.seek(0)

    if extension == "svg":
        head = uploaded_file.read(4096)
        uploaded_file.seek(0)

        if not _looks_like_svg(head):
            raise ValidationError("Uploaded SVG is corrupted or invalid.")
        return

    try:
        image = Image.open(uploaded_file)
        image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise ValidationError("Uploaded file is not a valid image.") from exc
    finally:
        uploaded_file.seek(0)
