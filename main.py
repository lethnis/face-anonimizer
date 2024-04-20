import os
import sys
from pathlib import Path
import cv2
import mediapipe as mp
from mediapipe import tasks
from mediapipe.tasks.python import vision


def main():
    """Blurs faces on images and videos. Originally files comes from 'assets' folder.
    You can specify a single file or a folder in arguments, e.g.
    python main.py path/to/file"""

    # get images and videos paths from arguments
    images, videos = parse_args()

    # make output dir if it is does not exist
    os.makedirs("output", exist_ok=True)

    # process images and videos if there is any
    if images:
        process_images(images)

    if videos:
        process_videos(videos)

    print("Results saved to the 'output' directory.")


def process_images(images_paths: list):
    """Blurs faces on images.

    Args:
        images_paths (list): list of images paths.
    """

    # create the model options
    options = vision.FaceDetectorOptions(
        base_options=tasks.BaseOptions(model_asset_path="blaze_face_short_range.tflite"),
        running_mode=vision.RunningMode.IMAGE,
    )

    # initialize the model
    with vision.FaceDetector.create_from_options(options) as detector:
        for image_path in images_paths:
            # read image and change format to mp.Image
            img = cv2.imread(image_path)
            mp_img = mp.Image(mp.ImageFormat.SRGB, img)
            # run model to detect faces
            result = detector.detect(mp_img)
            # blur all faces found
            img = blur_one_image(img, result.detections)
            # save image to the output directory
            cv2.imwrite(f"output/{Path(image_path).name}", img)


def process_videos(videos_paths: list):
    """Blur faces on all videos.

    Args:
        videos_paths (list): list of video paths
    """

    # create model options
    options = vision.FaceDetectorOptions(
        base_options=tasks.BaseOptions(model_asset_path="blaze_face_short_range.tflite"),
        running_mode=vision.RunningMode.VIDEO,
    )

    # for every video we create separate model, so it would work with timestamps
    for video_path in videos_paths:

        # initialize the model
        with vision.FaceDetector.create_from_options(options) as detector:

            # start reading video, get first frame
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()

            # get original video properties to create VideoWriter
            w, h, _ = frame.shape
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            fourcc = cv2.VideoWriter.fourcc(*"mp4v")

            # create VideoWriter, specify save path and properties
            writer = cv2.VideoWriter(f"output/{Path(video_path).name}", fourcc, fps, (h, w))

            # while we have frames to read
            while ret:
                # change frame to mp.Image type
                mp_frame = mp.Image(mp.ImageFormat.SRGB, frame)
                # detect faces with provided timestamps, to properly read video
                result = detector.detect_for_video(mp_frame, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
                # save blurred frame
                writer.write(blur_one_image(frame, result.detections))
                # read next frame
                ret, frame = cap.read()

            # release memory
            cap.release()
            writer.release()


def blur_one_image(image, detections):
    """Blur faces on a single image/frame.

    Args:
        image (np.array): image from cv2
        detections (DetectionResult.detections): list of all detections from FaceDetector

    Returns:
        np.array: image with blurred faces.
    """

    # for every detection/face on an image
    for detection in detections:
        # get bbox coordinates
        x = detection.bounding_box.origin_x
        y = detection.bounding_box.origin_y
        w = detection.bounding_box.width
        h = detection.bounding_box.height

        # apply a little expansion to coordinates
        x1 = max(0, x - 20)
        x2 = x1 + w + 40
        y1 = max(0, y - 20)
        y2 = y1 + h + 40

        # blur face on that coordinates
        image[y1:y2, x1:x2] = cv2.blur(image[y1:y2, x1:x2], ksize=(30, 30))

    return image


def parse_args():

    MESSAGE = """Face anonimizer. Usage:
    Please provide a path to a folder or an image/video file.
    Results will be saved to the 'output' directory."""

    base_dir = "assets"

    if len(sys.argv) == 2:
        base_dir = sys.argv[1]

    assert len(sys.argv) <= 2, f"Too many arguments. \n\n{MESSAGE}"

    assert os.path.exists(base_dir), f"Couldn't find '{base_dir}'. \n\n{MESSAGE}"

    return split_images_videos(base_dir)


def get_paths(base_dir):
    """Get all paths to files in base folder and all subfolders."""

    paths = []

    # if provided path is directory we search inside it
    if os.path.isdir(base_dir):
        # for every file and folder in base dir
        for i in os.listdir(base_dir):
            # update path so it will be full
            new_path = os.path.join(base_dir, i)
            # check if new path is a file or a folder
            if os.path.isdir(new_path):
                paths.extend(get_paths(new_path))
            else:
                paths.append(new_path)

    # Else path is a file, just add it to the resulting list
    else:
        paths.append(base_dir)

    return paths


def split_images_videos(base_dir):
    """Take all paths and extract only image and video formats."""

    paths = get_paths(base_dir)

    images, videos = [], []

    for path in paths:
        if any([path.endswith(i) for i in [".png", ".jpg", "jpeg"]]):
            images.append(path)
        elif any([path.endswith(i) for i in [".mp4", ".avi"]]):
            videos.append(path)

    return images, videos


if __name__ == "__main__":
    main()
