from django.core.files.uploadedfile import InMemoryUploadedFile
from moviepy.editor import VideoFileClip
from io import BytesIO
import numpy as np
import sys
import cv2


def resize_image(image, interpolation=cv2.INTER_AREA):
    """
    Resizes the image by verifying image width and height values to upscale
    or downscale to 1280x720.
    """

    # This code does not take into account images with text. So they will be
    # cropped and will loss their meaning. An ideal solution would scale the 
    # image based on the width and height, calculating the difference between
    # ideal format (1280x720).

    img = cv2.imread(image)

    h, w = img.shape[:2]
    min_size = np.amin([h, w])
    crop_img = img[
        int(h / 2 - min_size / 2) : int(h / 2 + min_size / 2),
        int(w / 2 - min_size / 2) : int(w / 2 + min_size / 2),
    ]

    resized = cv2.resize(crop_img, (240, 240), interpolation=cv2.INTER_AREA)

    _, buf = cv2.imencode(".jpg", resized)
    cv2.destroyAllWindows()

    image_io = BytesIO(buf.tobytes())
    image_content = InMemoryUploadedFile(
        image_io,
        "FileField",
        None,
        "JPG",
        sys.getsizeof(image_io),
        None,
    )

    return image_content


def subclip_video(video):
    clip = VideoFileClip(video)
    clip = clip.subclip(0, 10)
    clip.save_frame("./media/video_frame.jpeg", t=5)
    middle_frame = get_thumbnail("./media/video_frame.jpeg")
    clip.write_videofile("./media/subclip_video.mp4")
    clip = cv2.VideoCapture("./media/subclip_video.mp4")
    cv2.destroyAllWindows()

    _, frame = clip.read()
    video_io = BytesIO(frame.tobytes())
    video_content = InMemoryUploadedFile(
        video_io,
        "FileField",
        None,
        "MP4",
        sys.getsizeof(video_io),
        None,
    )

    return (
        video_content,
        middle_frame,
    )


def get_thumbnail(image):
    img = cv2.imread(image)

    h, w = img.shape[:2]
    min_size = np.amin([h, w])
    crop_img = img[
        int(h / 2 - min_size / 2) : int(h / 2 + min_size / 2),
        int(w / 2 - min_size / 2) : int(w / 2 + min_size / 2),
    ]
    thumbnail = cv2.resize(crop_img, (240, 240), interpolation=cv2.INTER_AREA)
    _, buf = cv2.imencode(".jpeg", thumbnail)

    cv2.destroyAllWindows()

    thumb_io = BytesIO(buf.tobytes())
    thumb_content = InMemoryUploadedFile(
        thumb_io,
        "ImageField",
        None,
        "JPEG",
        sys.getsizeof(thumb_io),
        None,
    )

    return thumb_content
