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
    image_name = image[11:-5] if image[-5:] == ".jpeg" else image[11:-4]
    h, w = img.shape[:2]
    min_size = np.amin([h, w])
    crop_img = img[
        int(h / 2 - min_size / 2) : int(h / 2 + min_size / 2),
        int(w / 2 - min_size / 2) : int(w / 2 + min_size / 2),
    ]

    resized = cv2.resize(crop_img, (1280, 720), interpolation=cv2.INTER_AREA)

    _, buf = cv2.imencode(".jpg", resized)
    cv2.destroyAllWindows()

    image_io = BytesIO(buf.tobytes())
    image_content = InMemoryUploadedFile(
        image_io,
        "FileField",
        f"{image_name}.jpg",
        "JPG",
        sys.getsizeof(image_io),
        None,
    )

    return (
        image_content,
        image_content.content_type,
    )


def subclip_video(video):

    clip = VideoFileClip(video)
    sub_clip = clip.subclip(0, 10)
    video_name = clip.filename[11:-4]
    sub_clip.save_frame(f"./media/{video_name}_middle_frame.jpeg", t=5)
    middle_frame = get_thumbnail(f"/app/media/{video_name}_middle_frame.jpeg")
    sub_clip.write_videofile(f"./media/{video_name}_subclip.mp4")
    sub_clip_capture = cv2.VideoCapture(f"/app/media/{video_name}_subclip.mp4")
    cv2.destroyAllWindows()

    frames = []
    grabbed = True

    while grabbed:
        grabbed, img = sub_clip_capture.read()
        if grabbed:
            frames.append(img)
    video = np.stack(frames, axis=0)

    video_io = BytesIO(video.tobytes())
    video_content = InMemoryUploadedFile(
        video_io,
        "FileField",
        f"{video_name}_subclip.mp4",
        "MP4",
        sys.getsizeof(video_io),
        None,
    )

    return (
        video_content,
        middle_frame,
        video_content.content_type,
    )


def get_thumbnail(image):
    img = cv2.imread(image)
    image_name = (
        f"{image[11:-5]}_thumb" if image[-5:] == ".jpeg" else f"{image[11:-4]}_thumb"
    )
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
        f"{image_name}.jpeg",
        "JPEG",
        sys.getsizeof(thumb_io),
        None,
    )

    return thumb_content
