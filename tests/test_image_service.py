import pytest
from app.services.category_service import create_category
from app.services.product_service import create_product
from app.services.image_service import (
    save_images, delete_image, reorder_images, list_images, ImageError, MAX_IMAGES,
)


@pytest.fixture
def product(db_session):
    category = create_category("Parfum")
    return create_product({"name": "Test", "price": 100, "category_id": category.id})


def test_save_images(db_session, product):
    images = save_images(product.id, ["a.jpg", "b.jpg"])
    assert len(images) == 2
    assert images[0].position == 1
    assert images[1].position == 2


def test_save_images_exceeds_max_raises(db_session, product):
    save_images(product.id, ["a.jpg", "b.jpg", "c.jpg", "d.jpg", "e.jpg"])
    with pytest.raises(ImageError):
        save_images(product.id, ["f.jpg"])


def test_save_images_empty_raises(db_session, product):
    with pytest.raises(ImageError):
        save_images(product.id, [])


def test_delete_image_reindexes_positions(db_session, product):
    images = save_images(product.id, ["a.jpg", "b.jpg", "c.jpg"])
    delete_image(images[0].id)
    remaining = list_images(product.id)
    assert [img.position for img in remaining] == [1, 2]


def test_reorder_images(db_session, product):
    images = save_images(product.id, ["a.jpg", "b.jpg"])
    reorder_images(product.id, [images[1].id, images[0].id])
    ordered = list_images(product.id)
    assert ordered[0].id == images[1].id
    assert ordered[0].position == 1