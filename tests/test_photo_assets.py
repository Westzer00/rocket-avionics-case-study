from pathlib import Path
from PIL import Image


PHOTOS = Path(__file__).resolve().parents[1] / "assets" / "photos"


def test_all_photo_assets_are_valid_webp():
    photos = sorted(PHOTOS.glob("*.webp"))
    assert len(photos) >= 4, "Expected actual assembly and flight photos"
    for photo in photos:
        with Image.open(photo) as img:
            assert img.format == "WEBP", photo.name
            width, height = img.size
            print(f"{photo.name}: {width}x{height}")
            assert width >= 200 and height >= 200, f"Unusually small photo: {photo.name}"
            img.verify()
