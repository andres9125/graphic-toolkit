from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from .image_ops import fit_to_square_canvas, load_image, save_jpeg, save_png
from .manifest import write_manifest


@dataclass(frozen=True)
class BrandPackResult:
    out_dir: Path
    manifest: Path


def build_brand_pack(
    source: str | Path,
    out_dir: str | Path,
    *,
    pad_ratio: float = 0.08,
    background: str = "#FFFFFF",
) -> BrandPackResult:
    """Create square brand assets and a 1200x630 social card."""
    source_path = Path(source)
    destination = Path(out_dir)
    image = load_image(source_path)

    square_1024 = fit_to_square_canvas(image, 1024, pad_ratio)
    square_512 = fit_to_square_canvas(image, 512, pad_ratio)
    social_mark = fit_to_square_canvas(image, 630, 0.1)
    social_card = Image.new("RGBA", (1200, 630), background)
    social_card.alpha_composite(social_mark, ((1200 - social_mark.width) // 2, 0))

    outputs = {
        "square_1024": save_png(square_1024, destination / "brand-square-1024.png").name,
        "square_512": save_png(square_512, destination / "brand-square-512.png").name,
        "social_card": save_jpeg(social_card, destination / "brand-social-1200x630.jpg", background=background).name,
        "transparent_preview": save_png(image, destination / "brand-preview-transparent.png").name,
    }
    manifest = write_manifest(
        destination / "manifest.json",
        {
            "command": "brand-pack",
            "source": source_path.name,
            "pad_ratio": pad_ratio,
            "background": background,
            "outputs": outputs,
        },
    )
    return BrandPackResult(out_dir=destination, manifest=manifest)

