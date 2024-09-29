import rclpy
from rclpy.node import Node
import tkinter as tk
from threading import Thread
import pygame  # Import the pygame library for handling sound playback
from pathlib import Path
import time  # Import time for handling delays between beeps

class NoiseNode(Node):
    def __init__(self):
        super().__init__('noise_node')
        pygame.init()  # Initialize the pygame

        base_path = Path(__file__).resolve().parent
        print(base_path)
        sound_file_NU = base_path / "alerts" / "beep-01a.wav"
        sound_file_U = base_path / "alerts" / "beep-09.wav"
        
        self.sounds = {
            '1': pygame.mixer.Sound(str(sound_file_NU)),
            '2': pygame.mixer.Sound(str(sound_file_U)),
            
        }

        # Start the GUI in a separate thread
        self.gui_thread = Thread(target=self.start_gui, daemon=True)
        self.gui_thread.start()

    def start_gui(self):
        self.root = tk.Tk()
        self.root.title("ROS2 Noise Interface")

        # Create label and entry for text input
        tk.Label(self.root, text="Enter or click a drawer number (1-2):").pack(padx=20, pady=10)
        self.entry = tk.Entry(self.root)
        self.entry.pack(padx=20, pady=10)
        self.entry.bind("<Return>", self.on_enter)

        # Create buttons for direct selection
        button_frame = tk.Frame(self.root)
        button_frame.pack(padx=20, pady=10)
        button_name = {}
        button_name[1]='Slow Beep(NU)'
        button_name[2] ='Fast Beep(U)'
        for number in range(1, 3):
            
            button = tk.Button(button_frame, text=button_name[number], 
                               command=lambda num=str(number): self.button_click(num))
            button.pack(side=tk.LEFT, padx=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_enter(self, event):
        self.process_input()

    def button_click(self, number):
        self.process_input(number)

    def process_input(self, number=None):
        if number is None:
            number = self.entry.get()
        if number == '1':
            self.play_beeps('1', interval=1.5, volume=0.5)
        elif number == '2':
            self.play_beeps('2', interval=1.0, volume=1.0)
        else:
            self.get_logger().info("Invalid drawer number")

    def play_beeps(self, sound_key, interval, volume):
        sound = self.sounds.get(sound_key)
        if sound:
            for _ in range(3):
                sound.set_volume(volume)
                sound.play()
                time.sleep(interval)

    def on_close(self):
        self.destroy_node()
        pygame.quit()  # Ensure pygame exits cleanly
        self.root.quit()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    noise_node = NoiseNode()
    rclpy.spin(noise_node)
    noise_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
