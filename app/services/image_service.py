from app.extensions import db
from app.models.product_image import ProductImage

MAX_IMAGES = 5


class ImageError(Exception):
    pass


def save_images(product_id: int, paths: list[str]) -> list[ProductImage]:
    existing_count = ProductImage.query.filter_by(product_id=product_id).count()

    if existing_count + len(paths) > MAX_IMAGES:
        raise ImageError(f"A product can have at most {MAX_IMAGES} images")

    if not paths:
        raise ImageError("At least one image is required")

    images = []
    for i, path in enumerate(paths):
        image = ProductImage(
            product_id=product_id,
            path=path,
            position=existing_count + i + 1,
        )
        db.session.add(image)
        images.append(image)

    db.session.commit()
    return images


def delete_image(image_id: int) -> None:
    image = ProductImage.query.get(image_id)
    if not image:
        raise ImageError(f"Image {image_id} not found")

    product_id = image.product_id
    db.session.delete(image)
    db.session.commit()

    remaining = ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.position).all()
    for i, img in enumerate(remaining):
        img.position = i + 1
    db.session.commit()


def reorder_images(product_id: int, ordered_image_ids: list[int]) -> None:
    images = ProductImage.query.filter_by(product_id=product_id).all()
    image_map = {img.id: img for img in images}

    if set(ordered_image_ids) != set(image_map.keys()):
        raise ImageError("Order list must contain exactly the product's existing image ids")

    for position, image_id in enumerate(ordered_image_ids, start=1):
        image_map[image_id].position = position

    db.session.commit()


def list_images(product_id: int) -> list[ProductImage]:
    return ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.position).all()