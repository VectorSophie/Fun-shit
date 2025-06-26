from pynput import keyboard
import time
from collections import defaultdict

class KeyboardStats:
    def __init__(self):
        self.key_counts = defaultdict(int)
        self.start_time = None
        self.end_time = None
        self.total_keys = 0

    def on_press(self, key):
        if self.start_time is None:
            self.start_time = time.time()
        
        try:
            k = key.char.lower()
        except AttributeError:
            k = str(key).replace('Key.', '')
        
        self.key_counts[k] += 1
        self.total_keys += 1

        print(f"Pressed: {k}")

    def on_release(self, key):
        if key == keyboard.Key.esc:
            self.end_time = time.time()
            return False

    def print_stats(self):
        duration = self.end_time - self.start_time if self.end_time and self.start_time else 0
        print("\n--- Keyboard Stats ---")
        print(f"Total keys pressed: {self.total_keys}")
        print(f"Session duration: {duration:.2f} seconds")
        if duration > 0:
            print(f"Average keys per second: {self.total_keys/duration:.2f}")
        else:
            print("Average keys per second: N/A")
        if self.key_counts:
            most_frequent = max(self.key_counts, key=self.key_counts.get)
            print(f"Most frequent key: '{most_frequent}' pressed {self.key_counts[most_frequent]} times")
        print("Key frequencies:")
        for key, count in sorted(self.key_counts.items(), key=lambda item: item[1], reverse=True):
            print(f"  {key}: {count}")

def main():
    stats = KeyboardStats()
    print("Start. (press ESC to show stats)")

    with keyboard.Listener(on_press=stats.on_press, on_release=stats.on_release) as listener:
        listener.join()

    stats.print_stats()

if __name__ == "__main__":
    main()
