from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps


class UnsupportedImageFormatError(ValueError):
    """Raised when an input needs an image decoder not shipped by this package."""


def load_image(path: str | Path) -> Image.Image:
    """Load a raster image as RGBA without retaining an open file handle."""
    source = Path(path)
    if source.suffix.lower() in {".svg", ".svgz"}:
        raise UnsupportedImageFormatError(
            "SVG input is not supported. Convert the asset to PNG, JPEG, or WebP first."
        )

    with Image.open(source) as opened:
        if getattr(opened, "n_frames", 1) > 1:
            opened.seek(0)
        return opened.convert("RGBA")


def trim_transparent_bounds(image: Image.Image) -> Image.Image:
    """Remove transparent outer pixels while preserving a fully transparent image."""
    bounds = image.getbbox()
    return image.copy() if bounds is None else image.crop(bounds)


def fit_to_square_canvas(image: Image.Image, size: int, pad_ratio: float) -> Image.Image:
    """Center an image on a transparent square canvas using proportional padding."""
    if size <= 0:
        raise ValueError("size must be positive")
    if not 0 <= pad_ratio < 0.5:
        raise ValueError("pad_ratio must be between 0 and 0.5")

    trimmed = trim_transparent_bounds(image)
    target = max(1, int(size * (1 - pad_ratio * 2)))
    resized = ImageOps.contain(trimmed, (target, target), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
    return canvas


def flatten_on_background(image: Image.Image, color: str) -> Image.Image:
    """Render an RGBA image onto a solid background for JPEG output."""
    background = Image.new("RGBA", image.size, color)
    background.alpha_composite(image)
    return background.convert("RGB")


def save_png(image: Image.Image, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="PNG", optimize=True)
    return destination


def save_jpeg(image: Image.Image, path: str | Path, *, background: str, quality: int = 92) -> Path:
    if not 1 <= quality <= 95:
        raise ValueError("quality must be between 1 and 95")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    flatten_on_background(image, background).save(
        destination,
        format="JPEG",
        quality=quality,
        optimize=True,
    )
    return destination


def save_ico(image: Image.Image, path: str | Path) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    return destination

