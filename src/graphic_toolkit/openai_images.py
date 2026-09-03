from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .manifest import write_manifest

IMAGES_GENERATIONS_URL = "https://api.openai.com/v1/images/generations"
DEFAULT_IMAGE_MODEL = "gpt-image-2"


class ImageGenerationError(RuntimeError):
    """Raised when the Images API cannot produce a usable PNG response."""


def generate_image(
    *,
    prompt: str,
    out_dir: str | Path,
    api_key: str | None = None,
    filename: str = "generated.png",
    model: str = DEFAULT_IMAGE_MODEL,
    size: str = "1024x1024",
    quality: str = "medium",
    background: str = "transparent",
    timeout_seconds: int = 120,
) -> dict[str, Any]:
    """Request one PNG image and write a manifest without retaining the prompt."""
    secret = api_key or os.environ.get("OPENAI_API_KEY")
    if not secret:
        raise ImageGenerationError("OPENAI_API_KEY is not configured")
    if not prompt.strip():
        raise ValueError("prompt must not be empty")

    output_name = Path(filename).name
    if output_name != filename or not output_name.lower().endswith(".png"):
        raise ValueError("filename must be a PNG file name without path components")

    request_body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "background": background,
            "output_format": "png",
        }
    ).encode("utf-8")
    request = Request(
        IMAGES_GENERATIONS_URL,
        data=request_body,
        headers={
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        raise ImageGenerationError(f"OpenAI image generation failed with HTTP {error.code}") from error
    except URLError as error:
        raise ImageGenerationError("OpenAI image generation could not reach the service") from error
    except json.JSONDecodeError as error:
        raise ImageGenerationError("OpenAI image generation returned invalid JSON") from error

    results = payload.get("data") or []
    encoded_image = results[0].get("b64_json") if results else None
    if not encoded_image:
        raise ImageGenerationError("OpenAI image generation returned no base64 image")

    destination = Path(out_dir)
    destination.mkdir(parents=True, exist_ok=True)
    image_path = destination / output_name
    image_path.write_bytes(base64.b64decode(encoded_image, validate=True))
    manifest_path = write_manifest(
        destination / "manifest.json",
        {
            "command": "openai-generate",
            "provider": "openai",
            "model": model,
            "size": size,
            "quality": quality,
            "background": background,
            "outputs": {"image": image_path.name},
            "usage": payload.get("usage"),
        },
    )
    return {"image": image_path, "manifest": manifest_path}

