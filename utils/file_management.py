from moviepy.editor import VideoFileClip
from PIL import Image
import cv2


def resize_image(image, interpolation=cv2.INTER_AREA):
    """
    Resizes the image by verifying image width and height values to upscale
    or downscale to 1280x720.
    """

    # This code does not take into account the exact values of width and height of the image
    # and because of this some images with ideal height but very low widths in comparison
    # should be distorted any way. The ideal should be taking the width and height values and
    # scale based on the difference from 1280x720. Below is another solution but cropping sides
    # of the image, what causes loss of meaning in images with text.

    # Cropping solution:
    # import numpy as np
    # img = cv2.imread(image)
    # h, w = img.shape[:2]
    # min_size = np.amin([h,w])

    # # Centralize and crop
    # crop_img = img[int(h/2-min_size/2):int(h/2+min_size/2), int(w/2-min_size/2):int(w/2+min_size/2)]
    # resized = cv2.resize(crop_img, (size, size), interpolation=interpolation)

    img = cv2.imread(image)
    h, w = img.shape[:2]

    if w > 1280 and h > 720:
        resized = cv2.resize(
            img, (1280, 720), fx=0.8, fy=0.8, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if w < 1280 and h < 720:
        resized = cv2.resize(
            img, (1280, 720), fx=1.2, fy=1.2, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if w < 1280 and h == 720:
        resized = cv2.resize(
            img, (1280, 720), fx=1.2, fy=1.0, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if w > 1280 and h == 720:
        resized = cv2.resize(
            img, (1280, 720), fx=0.8, fy=1.0, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if h > 720 and w < 1280:
        resized = cv2.resize(
            img, (1280, 720), fx=1.2, fy=0.8, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if h < 720 and w > 1280:
        resized = cv2.resize(
            img, (1280, 720), fx=0.8, fy=1.2, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if h > 720 and w == 1280:
        resized = cv2.resize(
            img, (1280, 720), fx=1.0, fy=0.8, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized
    if h < 720 and w == 1280:
        resized = cv2.resize(
            img, (1280, 720), fx=1.0, fy=1.2, interpolation=interpolation
        )
        cv2.imwrite("./media/resized_img.jpg", resized)
        return resized

    # resized = cv2.resize(img, (1280, 720), interpolation=interpolation)
    cv2.imwrite("./media/resized_img.jpg", img)
    cv2.destroyAllWindows()    

    return img


def subclip_video(video):
    clip = VideoFileClip(video)
    clip = clip.subclip(0, 10)
    clip.write_videofile("./media/subclip_video.mp4")

    clip = cv2.VideoCapture("./media/subclip_video.mp4")
    cv2.destroyAllWindows()    

    return clip


def get_thumbnail(self, media):
    img = Image.open(media)
    img.thumbnail((240, 240))
    img.save(f"/media/{media.name}-thumb", "jpeg")