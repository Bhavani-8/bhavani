

import cv2
import numpy as np
import pyautogui
import threading
import time
import os
import ctypes


class ScreenRecorder:
    def __init__(self, filename="test_execution.mp4", fps=10):
        self.filename = filename
        self.fps = fps
        self.recording = False
        self.out = None

    def start(self):
       
        user32 = ctypes.windll.user32

        width = user32.GetSystemMetrics(0)          # Screen width
        height = user32.GetSystemMetrics(1)         # Screen height
        work_height = user32.GetSystemMetrics(17)   # Height excluding taskbar

        self.video_size = (width, work_height)
        fourcc = cv2.VideoWriter_fourcc(*"avc1")   
        self.raw_file = self.filename  

        self.out = cv2.VideoWriter(self.raw_file,fourcc,self.fps,self.video_size)

        
        if not self.out.isOpened():
            print("❌ VideoWriter failed to open")
            return

        # print("✅ VideoWriter started")

        self.recording = True

        def record():
            frame_count = 0

            while self.recording:
                img = pyautogui.screenshot()
                frame = np.array(img)

                # Remove the taskbar from the bottom
                frame = frame[:self.video_size[1], :, :]

                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                self.out.write(frame)
                frame_count += 1

                time.sleep(1 / self.fps)

            

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
            pass

        return True