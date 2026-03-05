import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from django.core.files import File
from django.core.files.storage import default_storage


@dataclass
class MediaImportResult:
    storage_name: str | None
    status: str
    source: str = ""


class MediaImporter:
    STATUS_IMPORTED = "imported"
    STATUS_REUSED = "reused"
    STATUS_MISSING = "missing"
    STATUS_EMPTY = "empty"

    def __init__(self, frontend_dir: Path):
        self.frontend_dir = Path(frontend_dir).resolve()
        self.public_dir = self.frontend_dir / "public"
        self.assets_dir = self.frontend_dir / "assets"

        self._path_cache: dict[str, str] = {}
        self._checksum_cache: dict[str, str] = {}

    def import_image(self, src_path: str, upload_subdir: str) -> MediaImportResult:
        raw_path = (src_path or "").strip()
        if not raw_path:
            return MediaImportResult(storage_name=None, status=self.STATUS_EMPTY)

        source = self._resolve_source_path(raw_path)
        if not source:
            return MediaImportResult(storage_name=None, status=self.STATUS_MISSING, source=raw_path)

        source_key = str(source.resolve()).lower()
        cached_path = self._path_cache.get(source_key)
        if cached_path and default_storage.exists(cached_path):
            return MediaImportResult(storage_name=cached_path, status=self.STATUS_REUSED, source=source_key)

        checksum = self._sha256(source)
        checksum_cached = self._checksum_cache.get(checksum)
        if checksum_cached and default_storage.exists(checksum_cached):
            self._path_cache[source_key] = checksum_cached
            return MediaImportResult(storage_name=checksum_cached, status=self.STATUS_REUSED, source=source_key)

        storage_name, was_existing = self._save_file(source, upload_subdir, checksum)
        self._path_cache[source_key] = storage_name
        self._checksum_cache[checksum] = storage_name
        status = self.STATUS_REUSED if was_existing else self.STATUS_IMPORTED
        return MediaImportResult(storage_name=storage_name, status=status, source=source_key)

    def _resolve_source_path(self, raw_path: str) -> Path | None:
        parsed = urlparse(raw_path)
        if parsed.scheme in {"http", "https", "data"}:
            return None

        normalized = self._normalize_path(parsed.path or raw_path)
        if not normalized:
            return None

        direct_candidate = Path(normalized)
        if direct_candidate.is_absolute() and direct_candidate.exists():
            return direct_candidate

        candidates = [
            self.frontend_dir / normalized,
            self.public_dir / normalized,
            self.assets_dir / normalized,
        ]

        if normalized.startswith("public/"):
            candidates.append(self.frontend_dir / normalized)
        if normalized.startswith("assets/"):
            candidates.append(self.frontend_dir / normalized)
        if normalized.startswith("images/"):
            candidates.append(self.public_dir / normalized)

        for candidate in candidates:
            if candidate.exists() and candidate.is_file():
                return candidate
        return None

    def _normalize_path(self, value: str) -> str:
        normalized = (value or "").strip().replace("\\", "/")
        normalized = re.sub(r"^[./]+", "", normalized)
        normalized = re.sub(r"^[@~]/", "", normalized)
        normalized = normalized.lstrip("/")
        return normalized

    def _save_file(self, source_path: Path, upload_subdir: str, checksum: str) -> tuple[str, bool]:
        safe_subdir = self._normalize_upload_subdir(upload_subdir)
        safe_name = self._build_target_filename(source_path.name, checksum)
        target_name = f"{safe_subdir}/{safe_name}" if safe_subdir else safe_name

        if default_storage.exists(target_name):
            return target_name, True

        with source_path.open("rb") as source_handle:
            django_file = File(source_handle, name=safe_name)
            storage_name = default_storage.save(target_name, django_file)
        return storage_name, False

    def _normalize_upload_subdir(self, upload_subdir: str) -> str:
        parts = []
        for part in (upload_subdir or "").replace("\\", "/").split("/"):
            chunk = part.strip()
            if not chunk or chunk in {".", ".."}:
                continue
            parts.append(chunk)
        return "/".join(parts)

    def _build_target_filename(self, original_name: str, checksum: str) -> str:
        name = Path(original_name).stem
        extension = Path(original_name).suffix.lower() or ".bin"
        safe_name = re.sub(r"[^A-Za-z0-9_-]+", "-", name).strip("-").lower() or "image"
        return f"{safe_name}-{checksum[:10]}{extension}"

    def _sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as source_handle:
            for chunk in iter(lambda: source_handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
