import os
import cloudinary
import cloudinary.uploader
from app.extensions import db
from app.models.product_image import ProductImage

MAX_IMAGES = 5

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)


class ImageError(Exception):
    pass


def upload_to_cloudinary(file) -> str:
    try:
        result = cloudinary.uploader.upload(file, folder="marketoff")
        return result["secure_url"]
    except Exception as e:
        raise ImageError(f"Cloudinary руу хуулахад алдаа гарлаа: {str(e)}")


def save_images(product_id: int, paths: list[str]) -> list[ProductImage]:
    try:
        # Хэрэв ирсэн зургийн зам байхгүй бол алдаа заалгүй шууд хоосон жагсаалт буцаана
        if not paths:
            return []

        existing_count = ProductImage.query.filter_by(product_id=product_id).count()

        if existing_count + len(paths) > MAX_IMAGES:
            raise ImageError(f"Бүтээгдэхүүнд хамгийн ихдээ {MAX_IMAGES} зураг оруулж болно")

        images = []
        for i, path in enumerate(paths):
            image = ProductImage(
                product_id=product_id,
                path=path,  # Cloudinary-ийн бүтэн secure_url хадгалагдана
                position=existing_count + i + 1,
            )
            db.session.add(image)
            images.append(image)

        db.session.commit()
        return images
    except Exception as e:
        db.session.rollback()  # Алдаа гарвал өгөгдлийн сангийн сессийг цэвэрлэнэ
        if not isinstance(e, ImageError):
            raise ImageError(f"Зураг хадгалахад алдаа гарлаа: {str(e)}")
        raise e


def delete_image(image_id: int) -> None:
    try:
        image = ProductImage.query.get(image_id)
        if not image:
            raise ImageError(f"Зураг {image_id} олдсонгүй")

        product_id = image.product_id
        db.session.delete(image)
        db.session.commit()

        remaining = ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.position).all()
        for i, img in enumerate(remaining):
            img.position = i + 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ImageError(f"Зураг устгахад алдаа гарлаа: {str(e)}")


def reorder_images(product_id: int, ordered_image_ids: list[int]) -> None:
    try:
        images = ProductImage.query.filter_by(product_id=product_id).all()
        image_map = {img.id: img for img in images}

        if set(ordered_image_ids) != set(image_map.keys()):
            raise ImageError("Эрэмбийн жагсаалт зөрүүтэй байна")

        for position, image_id in enumerate(ordered_image_ids, start=1):
            image_map[image_id].position = position

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise ImageError(f"Зургийн эрэмбэ өөрчлөхөд алдаа гарлаа: {str(e)}")


def list_images(product_id: int) -> list[ProductImage]:
    return ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.position).all()
