import io
from typing import Tuple
from PIL import Image, ImageOps


TARGET_RES = (1024, 1024)


def load_and_preprocess_image(
    path: str, target_res: Tuple[int, int] = TARGET_RES
) -> Image:
    image = Image.open(path)
    image = pad_to_square(image)
    image = image.convert("RGB")
    image = image.resize(target_res)
    return image


def load_and_preprocess_mask(
    path: str, target_res: Tuple[int, int] = TARGET_RES
) -> Image:
    mask = load_and_preprocess_image(path, target_res=target_res)
    mask = mask.convert("L")
    mask = mask.point(lambda x: 255 if x > 128 else 0, mode="1")
    return mask


def image_to_bytes(image: Image) -> bytes:
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)
    return image_bytes.getvalue()


def pad_to_square(image: Image, fill: Tuple[int, int, int] = (0, 0, 0)) -> Image:
    """Makes an image square by adding a border of color `fill`"""
    width, height = image.size
    max_dim = max(width, height)
    padding = (
        (max_dim - width) // 2,  # left
        (max_dim - height) // 2,  # top
        (max_dim - width + 1) // 2,  # right
        (max_dim - height + 1) // 2,  # bottom
    )
    return ImageOps.expand(image, padding, fill)
