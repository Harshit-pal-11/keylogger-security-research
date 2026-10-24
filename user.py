"""Visible, local-only keyboard event demo for a controlled lab."""

import json
from datetime import datetime, timezone
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


LOG_DIR = Path(__file__).parent / "logs"


class KeyboardDemo:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Keyboard Event Demo")
        self.root.geometry("680x480")
        self.recording = False
        self.log_file = None
        self.log_path: Path | None = None

        tk.Label(
            root,
            text="Keyboard Event Demo — local and visible",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(16, 4))
        tk.Label(
            root,
            text="Use dummy text only. Events are recorded only while this window is visibly recording.",
            wraplength=620,
        ).pack(pady=(0, 12))

        self.input_box = tk.Text(root, height=12, wrap="word", font=("Consolas", 11))
        self.input_box.pack(fill="both", expand=True, padx=16)
        self.input_box.insert("1.0", "Click here and type sample text for your demo.\n")
        self.input_box.bind("<KeyPress>", self.on_key_press)

        controls = tk.Frame(root)
        controls.pack(fill="x", padx=16, pady=12)
        self.record_button = tk.Button(controls, text="Start recording", command=self.toggle_recording)
        self.record_button.pack(side="left")
        tk.Button(controls, text="Clear text", command=self.clear_text).pack(side="left", padx=8)
        self.status = tk.Label(controls, text="Status: stopped", anchor="w")
        self.status.pack(side="left", padx=12)

        self.log_location = tk.Label(root, text="Log file: none", anchor="w", wraplength=640)
        self.log_location.pack(fill="x", padx=16, pady=(0, 14))
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def toggle_recording(self) -> None:
        if self.recording:
            self.stop_recording()
            return
        if not messagebox.askyesno(
            "Start local demo recording?",
            "This demo records key events typed in its text box to a local file.\n\n"
            "Use dummy text only. Continue?",
        ):
            return
        LOG_DIR.mkdir(exist_ok=True)
        filename = datetime.now().strftime("session-%Y%m%d-%H%M%S.jsonl")
        self.log_path = LOG_DIR / filename
        self.log_file = self.log_path.open("a", encoding="utf-8")
        self.recording = True
        self.record_button.config(text="Stop recording")
        self.status.config(text="Status: recording in this window")
        self.log_location.config(text=f"Log file: {self.log_path}")

    def stop_recording(self) -> None:
        self.recording = False
        if self.log_file is not None:
            self.log_file.close()
            self.log_file = None
        self.record_button.config(text="Start recording")
        self.status.config(text="Status: stopped")

    def on_key_press(self, event: tk.Event) -> None:
        if not self.recording or self.log_file is None:
            return
        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "keysym": event.keysym,
            "character": event.char,
        }
        self.log_file.write(json.dumps(record, ensure_ascii=False) + "\n")
        self.log_file.flush()

    def clear_text(self) -> None:
        self.input_box.delete("1.0", "end")
        self.input_box.focus_set()

    def close(self) -> None:
        self.stop_recording()
        self.root.destroy()


def main() -> None:
    root = tk.Tk()
    KeyboardDemo(root)
    root.mainloop()


if __name__ == "__main__":
    main()
