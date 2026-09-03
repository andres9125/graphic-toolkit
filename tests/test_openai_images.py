from __future__ import annotations

import base64
import json
import unittest
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock, patch

from PIL import Image

from graphic_toolkit.openai_images import DEFAULT_IMAGE_MODEL, generate_image


def png_bytes() -> bytes:
    buffer = BytesIO()
    Image.new("RGBA", (2, 2), (0, 0, 0, 0)).save(buffer, format="PNG")
    return buffer.getvalue()


class OpenAIImageTests(unittest.TestCase):
    @patch("graphic_toolkit.openai_images.urlopen")
    def test_generation_uses_the_images_endpoint_without_recording_prompt(self, mocked_urlopen: MagicMock) -> None:
        encoded = base64.b64encode(png_bytes()).decode("ascii")
        response = MagicMock()
        response.read.return_value = json.dumps({"data": [{"b64_json": encoded}], "usage": {"total_tokens": 1}}).encode("utf-8")
        response.__enter__.return_value = response
        mocked_urlopen.return_value = response

        with TemporaryDirectory() as temporary:
            result = generate_image(
                prompt="Sensitive-looking prompt text must not be written to disk",
                out_dir=Path(temporary) / "generated",
                api_key="test-key",
            )
            manifest = result["manifest"].read_text(encoding="utf-8")
            self.assertTrue(result["image"].exists())
            self.assertNotIn("Sensitive-looking", manifest)
            self.assertNotIn("test-key", manifest)

        request = mocked_urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://api.openai.com/v1/images/generations")
        self.assertEqual(json.loads(request.data.decode("utf-8"))["model"], DEFAULT_IMAGE_MODEL)


if __name__ == "__main__":
    unittest.main()
