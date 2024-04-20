import cv2
import mediapipe as mp
from mediapipe import tasks
from mediapipe.tasks.python import vision

from main import blur_one_image


def main():
    """Blurs faces on a webcam stream."""

    # initialize reading from webcam
    cap = cv2.VideoCapture(0)

    # specify model path and running mode for the model
    options = vision.FaceDetectorOptions(
        base_options=tasks.BaseOptions(model_asset_path="blaze_face_short_range.tflite"),
        running_mode=vision.RunningMode.VIDEO,
    )

    with vision.FaceDetector.create_from_options(options) as detector:

        print("Press 'q' to quit.")

        while True:
            # read next frame
            ret, frame = cap.read()
            # cast np.Image format
            mp_frame = mp.Image(mp.ImageFormat.SRGB, frame)
            # detect faces, needed timestamp from openCV
            result = detector.detect_for_video(mp_frame, int(cap.get(cv2.CAP_PROP_POS_MSEC)))
            # blur original frame with results from mp_frame
            frame = blur_one_image(frame, result.detections)

            # show frame after reading qr-code information
            cv2.imshow("webcam", frame)
            # if 'q' were pressed we quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # release memory
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
