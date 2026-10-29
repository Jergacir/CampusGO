import cloudinary
import cloudinary.uploader

from config import Config


def _configure():
    values = (
        Config.CLOUDINARY_CLOUD_NAME,
        Config.CLOUDINARY_API_KEY,
        Config.CLOUDINARY_API_SECRET,
    )
    if not all(values):
        raise RuntimeError(
            "Faltan CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY o "
            "CLOUDINARY_API_SECRET"
        )

    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
        secure=True,
    )


def subir_imagen(archivo, carpeta, public_id):
    _configure()
    resultado = cloudinary.uploader.upload(
        archivo,
        folder=carpeta,
        public_id=public_id,
        resource_type="image",
        overwrite=True,
    )
    return {
        "url": resultado["secure_url"],
        "public_id": resultado["public_id"],
    }


def eliminar_imagen(public_id):
    if not public_id:
        return

    _configure()
    cloudinary.uploader.destroy(public_id, resource_type="image")
