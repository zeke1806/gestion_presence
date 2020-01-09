from PIL import Image


def rotate_image(file):
    image = Image.open(file)

    try:
        # Grab orientation value.
        image_exif = image._getexif()
        image_orientation = image_exif[274]

        # Rotate depending on orientation.
        if image_orientation == 2:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if image_orientation == 3:
            image = image.transpose(Image.ROTATE_180)
        if image_orientation == 4:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        if image_orientation == 5:
            image = image.transpose(
                Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
        if image_orientation == 6:
            image = image.transpose(Image.ROTATE_270)
        if image_orientation == 7:
            image = image.transpose(
                Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
        if image_orientation == 8:
            image = image.transpose(Image.ROTATE_90)
        return image
    except:
        pass

    # image.thumbnail(ownphotos.settings.FULLPHOTO_SIZE, PIL.Image.ANTIALIAS)
    '''image_io = BytesIO()
    image.save(image_io,format="JPEG")
    self.image.save(self.image_hash+'.jpg', ContentFile(image_io.getvalue()))
    image_io.close() '''
