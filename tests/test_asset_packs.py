from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from graphic_toolkit.brand_pack import build_brand_pack
from graphic_toolkit.favicon import build_favicon_pack
from graphic_toolkit.image_ops import UnsupportedImageFormatError, load_image


def make_source(path: Path) -> None:
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    drawing = ImageDraw.Draw(image)
    drawing.rounded_rectangle((32, 32, 224, 224), radius=48, fill=(27, 75, 138, 255))
    drawing.ellipse((88, 88, 168, 168), fill=(255, 255, 255, 255))
    image.save(path, format="PNG")


class AssetPackTests(unittest.TestCase):
    def test_favicon_pack_writes_expected_assets_and_safe_manifest(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "sample-mark.png"
            make_source(source)

            result = build_favicon_pack(source, root / "favicon")

            self.assertTrue((result.out_dir / "favicon-512.png").exists())
            self.assertTrue((result.out_dir / "favicon-180.png").exists())
            self.assertTrue((result.out_dir / "apple-touch-icon.png").exists())
            self.assertTrue((result.out_dir / "favicon.ico").exists())
            manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
            self.assertEqual(manifest["source"], "sample-mark.png")
            self.assertNotIn(str(root), result.manifest.read_text(encoding="utf-8"))

    def test_brand_pack_writes_expected_assets(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "sample-mark.png"
            make_source(source)

            result = build_brand_pack(source, root / "brand", background="#112233")

            self.assertTrue((result.out_dir / "brand-square-1024.png").exists())
            self.assertTrue((result.out_dir / "brand-square-512.png").exists())
            self.assertTrue((result.out_dir / "brand-social-1200x630.jpg").exists())
            self.assertTrue((result.out_dir / "brand-preview-transparent.png").exists())
            with Image.open(result.out_dir / "brand-social-1200x630.jpg") as social_card:
                self.assertEqual(social_card.size, (1200, 630))

    def test_svg_is_rejected_with_actionable_guidance(self) -> None:
        with TemporaryDirectory() as temporary:
            source = Path(temporary) / "sample.svg"
            source.write_text("<svg />", encoding="utf-8")

            with self.assertRaises(UnsupportedImageFormatError):
                load_image(source)


if __name__ == "__main__":
    unittest.main()

