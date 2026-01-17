import tkinter as tk
from tkinter import messagebox
import time
import threading
import pygame
import os
import sys
import ctypes

INTERVAL = 360

def resource_path(relative_path):
    if getattr(sys, "_MEIPASS", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".") 
    return os.path.join(base_path, relative_path)

class EnkepalinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("엔케팔린 알리미")
        self.root.geometry("230x250")
        self.root.resizable(False, False)

        pygame.mixer.init()
        self.alarm_file = resource_path("araya_alarm.wav")

        self.running = False
        self.current = 0
        self.target = 0
        self.elapsed = 0

        font_label = ("맑은 고딕", 11)
        font_status = ("맑은 고딕", 12, "bold")

        tk.Label(root, text="현재 엔케팔린", font=font_label)\
            .grid(row=0, column=0, padx=20, pady=15, sticky="e")
        self.current_entry = tk.Entry(root, width=10)
        self.current_entry.grid(row=0, column=1)

        tk.Label(root, text="목표 엔케팔린", font=font_label)\
            .grid(row=1, column=0, padx=20, pady=10, sticky="e")
        self.target_entry = tk.Entry(root, width=10)
        self.target_entry.grid(row=1, column=1)

        self.status_label = tk.Label(root, text="대기 중", font=font_status, fg="blue")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.timer_label = tk.Label(root, text="다음 증가까지: 06:00", fg="gray")
        self.timer_label.grid(row=3, column=0, columnspan=2)

        btn_frame = tk.Frame(root)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(btn_frame, text="시작", width=10, height=2,
                  command=self.start).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="중지", width=10, height=2,
                  command=self.stop).grid(row=0, column=1, padx=5)

    def start(self):
        try:
            self.current = int(self.current_entry.get())
            self.target = int(self.target_entry.get())
        except ValueError:
            messagebox.showerror("입력 오류", "숫자를 입력해주세요.")
            return

        self.running = True
        self.elapsed = 0
        self.status_label.config(text=f"현재 엔케팔린: {self.current}", fg="green")

        threading.Thread(target=self.run_timer, daemon=True).start()
        self.update_clock()

    def stop(self):
        self.running = False
        pygame.mixer.music.stop()
        self.status_label.config(text="중지됨", fg="red")

    def run_timer(self):
        while self.running and self.current < self.target:
            time.sleep(1)
            self.elapsed += 1

            if self.elapsed >= INTERVAL:
                self.current += 1
                self.elapsed = 0
                self.root.after(0, self.update_status)

        if self.current >= self.target and self.running:
            self.root.after(0, self.alarm)

    def update_clock(self):
        if not self.running:
            return
        remain = INTERVAL - self.elapsed
        self.timer_label.config(
            text=f"다음 증가까지: {remain//60:02d}:{remain%60:02d}"
        )
        self.root.after(1000, self.update_clock)

    def update_status(self):
        self.status_label.config(
            text=f"현재 엔케팔린: {self.current} / 목표: {self.target}", fg="green"
        )

    def alarm(self):
        self.running = False
        self.play_alarm()
        messagebox.showinfo("목표 달성", f"엔케팔린 {self.target}이 모두 회복되었습니다🎉")
        self.status_label.config(text="완료", fg="blue")

    def play_alarm(self):
        try:
            pygame.mixer.music.load(self.alarm_file)
            pygame.mixer.music.play()
        except Exception as e:
            print("알람 재생 오류:", e)

if __name__ == "__main__":
    my_app_id = 'mycompany.enkephalin.alarm.1.0' 
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    root = tk.Tk()

    try:
        icon_path = resource_path("enkephalin_icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            print("아이콘 파일 없음:", icon_path)
    except Exception as e:
        print("아이콘 로드 실패:", e)

    app = EnkepalinApp(root)
    root.mainloop()