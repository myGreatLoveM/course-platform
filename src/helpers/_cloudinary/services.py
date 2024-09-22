

def get_cloudinary_image_object(instance, 
                                field_name="image",
                                as_html=False,
                                width=1200):
    if not hasattr(instance, field_name):
        return ""
    img_obj = getattr(instance, field_name)
    if not img_obj:
        return ""
    image_options = {
        "width": width
    }
    if as_html:
        return img_obj.image(**image_options)
    url = img_obj.build_url(**image_options)
    return url