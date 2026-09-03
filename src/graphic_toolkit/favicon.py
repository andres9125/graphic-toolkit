from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .image_ops import fit_to_square_canvas, load_image, save_ico, save_png
from .manifest import write_manifest


@dataclass(frozen=True)
class FaviconPackResult:
    out_dir: Path
    manifest: Path


def build_favicon_pack(source: str | Path, out_dir: str | Path, *, pad_ratio: float = 0.12) -> FaviconPackResult:
    """Create web and Apple icon files from one raster image."""
    source_path = Path(source)
    destination = Path(out_dir)
    image = load_image(source_path)

    icon_512 = fit_to_square_canvas(image, 512, pad_ratio)
    icon_180 = fit_to_square_canvas(image, 180, min(0.2, pad_ratio + 0.02))
    outputs = {
        "favicon_512": save_png(icon_512, destination / "favicon-512.png").name,
        "favicon_180": save_png(fit_to_square_canvas(image, 180, pad_ratio), destination / "favicon-180.png").name,
        "apple_touch_icon": save_png(icon_180, destination / "apple-touch-icon.png").name,
        "favicon_ico": save_ico(icon_512, destination / "favicon.ico").name,
    }
    manifest = write_manifest(
        destination / "manifest.json",
        {
            "command": "favicon-pack",
            "source": source_path.name,
            "pad_ratio": pad_ratio,
            "outputs": outputs,
        },
    )
    return FaviconPackResult(out_dir=destination, manifest=manifest)

