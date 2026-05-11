

import cv2
import numpy as np
import pyautogui
import threading
import time
import os


class ScreenRecorder:
    def __init__(self, filename="test_execution.mp4", fps=10):
        self.filename = filename
        self.fps = fps
        self.recording = False
        self.out = None

    def start(self):
        # width, height = pyautogui.size()
        # self.video_size = (width, height)
        width, height = pyautogui.size()

        taskbar_height = 50
        self.region = (0, 0, width, height - taskbar_height)
        self.video_size = (width, height - taskbar_height)

        # ✅ Use AVI (100% reliable)
        fourcc = cv2.VideoWriter_fourcc(*"avc1")   # ✅ REAL MP4
        self.raw_file = self.filename  

        self.out = cv2.VideoWriter(self.raw_file,fourcc,self.fps,self.video_size)

        # 🔴 CRITICAL CHECK
        if not self.out.isOpened():
            print("❌ VideoWriter failed to open")
            return

        print("✅ VideoWriter started")

        self.recording = True

        def record():
            frame_count = 0

            while self.recording:
                img = pyautogui.screenshot()
                frame = np.array(img)

                if frame is None or frame.size == 0:
                    print("❌ Empty frame")
                    continue

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # ✅ EXACT SIZE MATCH
                frame = cv2.resize(frame, self.video_size)

                self.out.write(frame)
                frame_count += 1

                time.sleep(1 / self.fps)

            print(f"🎥 Total frames recorded: {frame_count}")

        self.thread = threading.Thread(target=record, daemon=True)
        self.thread.start()

    def stop(self):
        self.recording = False

        if hasattr(self, "thread"):
            self.thread.join()

        if self.out:
            self.out.release()

        time.sleep(2)

        try:
            if os.path.exists(self.raw_file):
                os.rename(self.raw_file, self.final_file)
                print("✅ Video saved:", self.final_file)
        except Exception as e:
            print("❌ Rename failed:", e)

        return True