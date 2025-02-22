import cv2
import os
from ffpyplayer.player import MediaPlayer

class AlertViewer:
    def __init__(self, alert_video_path="assets/alert_video.mp4", encrypted_file_path="D:/testingfiles/text1.txt"):
        # Check if the video file exists
        if not os.path.exists(alert_video_path):
            print(f"Error: Video file not found at '{alert_video_path}'.")
            raise FileNotFoundError(f"Video file not found at '{alert_video_path}'.")
        
        self.alert_video_path = alert_video_path
        self.encrypted_file_path = encrypted_file_path

    def show_alert_video(self):
        """Display the alert video with sound in fullscreen mode."""
        try:
            cap = cv2.VideoCapture(self.alert_video_path)
            player = MediaPlayer(self.alert_video_path)  # Initialize audio playback

            if not cap.isOpened():
                print(f"Error: Unable to open video file '{self.alert_video_path}'.")
                return
            else:
                print("Video file opened successfully!")

            # Set the window properties for fullscreen mode
            cv2.namedWindow("Alert", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Alert", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            # Loop through the video frames
            while cap.isOpened():
                ret, frame = cap.read()
                audio_frame, val = player.get_frame()  # Get audio frame
                
                if not ret:
                    print("End of video reached.")
                    break

                cv2.imshow("Alert", frame)

                if val != 'eof' and audio_frame is not None:
                    img, t = audio_frame

                # Wait for the 'q' key to exit
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    print("Alert interrupted by user.")
                    break

            cap.release()
            cv2.destroyAllWindows()
            player.close()  # Close the audio player

        except Exception as e:
            print(f"Error displaying alert video: {e}")

# Usage example
if __name__ == "__main__":
    viewer = AlertViewer("assets/alert_video.mp4")
    viewer.show_alert_video()
