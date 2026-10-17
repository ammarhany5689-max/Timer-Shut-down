from tkinter import *
from tkinter import messagebox
import time
import subprocess
import re
import winsound

root = Tk()
root.title("Timer Shut down")
root.configure(bg="#C89058")
root.geometry("400x400")
root.resizable(False, False)

hours = 0
minutes = 0
seconds = 0
timer_id = None
running = False

# ---------------- Timer functions ----------------

def update_label():
    label.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")



def countdown():
    global hours, minutes, seconds, timer_id, running

    timer_id = None

    if not running:
        return

    if hours == 0 and minutes == 0 and seconds == 0:
        running = False
        update_label()

        answer = messagebox.askyesno(
            "Shut down",
            "Time is up! Do you want to shut down the computer?"
        )

        if answer:
            import subprocess
            subprocess.Popen(["shutdown", "/s", "/t", "60"])

            messagebox.showinfo(
                "Shut down",
                "Computer will shut down in 60 seconds.\n"
                "To cancel, run: shutdown /a"
            )
        return

    if seconds > 0:
        seconds -= 1
    elif minutes > 0:
        minutes -= 1
        seconds = 59
    elif hours > 0:
        hours -= 1
        minutes = 59
        seconds = 59

    update_label()
    timer_id = root.after(1000, countdown)

import re

def parse_time(text):
    text = text.lower().strip()

    pattern = r"(\d+(?::\d+)?)\s*(h|m|s)"
    matches = re.findall(pattern, text)

    if not matches:
        raise ValueError("Invalid time")

    remaining = re.sub(pattern, "", text)
    remaining = remaining.replace("and", "").replace(" ", "")

    if remaining:
        raise ValueError("Invalid time")

    total_seconds = 0

    for value, unit in matches:
        if ":" in value:
            first, second = map(int, value.split(":"))

            if unit == "h":
                total_seconds += first * 3600 + second * 60
            elif unit == "m":
                total_seconds += first * 60 + second
            else:
                raise ValueError("Invalid seconds format")

        else:
            number = int(value)

            if unit == "h":
                total_seconds += number * 3600
            elif unit == "m":
                total_seconds += number * 60
            elif unit == "s":
                total_seconds += number

    if total_seconds <= 0:
        raise ValueError("Time must be positive")

    return total_seconds



def start_timer():
    global hours, minutes, seconds, running

    if running:
        return

    try:
        total = parse_time(entry.get())

        hours = total // 3600
        minutes = (total % 3600) // 60
        seconds = total % 60

    except ValueError:
        messagebox.showerror(
            "Error",
            "Examples: 1h, 1m, 1s, 1h and 30m"
        )
        return

    running = True
    countdown()


def stop_timer():
    global running, timer_id

    running = False

    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None


def save_timer():
    with open("timer.txt", "w", encoding="utf-8") as file:
        file.write(f"{hours:02}:{minutes:02}:{seconds:02}")

    messagebox.showinfo("Save", "Timer saved to timer.txt")


def exit_app():
    stop_timer()
    root.destroy()


def select_time(value):
    global hours, minutes, seconds

    stop_timer()

    try:
        parsed = time.strptime(value, "%I:%M %p")
        now = time.localtime()

        target = time.struct_time((
            now.tm_year, now.tm_mon, now.tm_mday,
            parsed.tm_hour, parsed.tm_min, 0,
            now.tm_wday, now.tm_yday, now.tm_isdst
        ))

        current_seconds = (
            now.tm_hour * 3600 + now.tm_min * 60 + now.tm_sec
        )
        target_seconds = (
            target.tm_hour * 3600 + target.tm_min * 60
        )

        difference = target_seconds - current_seconds

        if difference <= 0:
            difference += 24 * 3600

        hours = difference // 3600
        minutes = (difference % 3600) // 60
        seconds = difference % 60

        entry.delete(0, END)
        entry.insert(0, str(difference))
        update_label()

    except ValueError:
        messagebox.showerror("Error", "Invalid time.")

def sound_start():
    winsound.PlaySound("start.wav", winsound.SND_FILENAME)

def sound_stop():
    winsound.PlaySound("stop.wav", winsound.SND_FILENAME)

def sound_save():
    winsound.PlaySound("save.wav", winsound.SND_FILENAME)

def sound_exit():
    winsound.PlaySound("exit.wav", winsound.SND_FILENAME)

# ---------------- Time selection window ----------------

import winsound

sound_enabled = True

def toggle_sound():
    global sound_enabled

    sound_enabled = not sound_enabled

    if not sound_enabled:
        winsound.PlaySound(None, 0)
        sound_button.config(text="Sound OFF")
    else:
        sound_button.config(text="Sound ON")


# ---------------- Main interface ----------------

Label(
    root,
    text="Timer Shut down",
    font=("Arial", 20, "bold"),
    fg="#360802",
    bg="#C89058"
).pack(pady=5)

entry = Entry(root, width=20, justify=LEFT)
entry.pack(pady=5)
entry.insert(0, "10s")

label = Label(
    root,
    text="00:00:00",
    font=("Arial", 30, "bold"),
    bg="#C89058",
    fg="#5E1E21"
)
label.pack(pady=10)

Button(
    root, text="Start", width=25,
    bg="#6B6B02", fg="white",
    command=lambda: (sound_start(), start_timer())
).place(x=1, y=340)

Button(
    root, text="Stop", width=25,
    bg="#6B6B02", fg="white",
    command=lambda: (sound_stop(), stop_timer())
).place(x=200, y=340)

sound_button = Button(
    root,
    text="Sound ON",
    width=25,
    bg="#267326",
    fg="white",
    command=toggle_sound
)
sound_button.place(x=100, y=300)


Button(
    root, text="Save", width=25,
    bg="#6B6B02", fg="white",
    command=lambda: (sound_save(), save_timer())
).place(x=200, y=370)

Button(
    root, text="Exit", width=25,
    bg="#6B6B02", fg="white",
    command=lambda: (sound_exit(), exit_app())
).place(x=1, y=370)

root.mainloop()