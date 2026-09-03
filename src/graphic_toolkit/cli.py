from __future__ import annotations

import argparse
import json
from pathlib import Path

from .brand_pack import build_brand_pack
from .favicon import build_favicon_pack
from .openai_images import ImageGenerationError, generate_image


def _default_output(command: str) -> Path:
    return Path.cwd() / "graphic-toolkit-output" / command


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="graphic-toolkit")
    subcommands = parser.add_subparsers(dest="command", required=True)

    favicon = subcommands.add_parser("favicon-pack", help="Create favicon assets from a raster source image")
    favicon.add_argument("source", help="Source image path (for example PNG, JPEG, or WebP)")
    favicon.add_argument("--out", type=Path, default=_default_output("favicon-pack"), help="Output directory")
    favicon.add_argument("--pad-ratio", type=float, default=0.12, help="Transparent padding ratio")

    brand = subcommands.add_parser("brand-pack", help="Create brand and social assets from a raster source image")
    brand.add_argument("source", help="Source image path (for example PNG, JPEG, or WebP)")
    brand.add_argument("--out", type=Path, default=_default_output("brand-pack"), help="Output directory")
    brand.add_argument("--pad-ratio", type=float, default=0.08, help="Transparent padding ratio")
    brand.add_argument("--background", default="#FFFFFF", help="Background color for JPEG output")

    generated = subcommands.add_parser("openai-generate", help="Generate one PNG through the OpenAI Images API")
    generated.add_argument("prompt", help="Image-generation prompt")
    generated.add_argument("--out", type=Path, default=_default_output("openai-generate"), help="Output directory")
    generated.add_argument("--filename", default="generated.png", help="PNG output file name")
    generated.add_argument("--model", default="gpt-image-2", help="OpenAI image model")
    generated.add_argument("--size", default="1024x1024", help="Generation size")
    generated.add_argument("--quality", default="medium", help="Generation quality")
    generated.add_argument("--background", default="transparent", help="Background mode")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "favicon-pack":
            result = build_favicon_pack(args.source, args.out, pad_ratio=args.pad_ratio)
            print(json.dumps({"manifest": str(result.manifest)}, ensure_ascii=False))
            return 0
        if args.command == "brand-pack":
            result = build_brand_pack(
                args.source,
                args.out,
                pad_ratio=args.pad_ratio,
                background=args.background,
            )
            print(json.dumps({"manifest": str(result.manifest)}, ensure_ascii=False))
            return 0
        if args.command == "openai-generate":
            result = generate_image(
                prompt=args.prompt,
                out_dir=args.out,
                filename=args.filename,
                model=args.model,
                size=args.size,
                quality=args.quality,
                background=args.background,
            )
            print(json.dumps({"image": str(result["image"]), "manifest": str(result["manifest"])}, ensure_ascii=False))
            return 0
    except (ImageGenerationError, OSError, ValueError) as error:
        parser.error(str(error))

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

