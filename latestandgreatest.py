import random
import tkinter as tk
from tkinter import messagebox
import json
import os
import winsound  # Windows-only sound

TROPHY_FILE = "trophies.json"

def play_sound(name):
    """
    Simple sound helper using winsound.
    Expects .wav files in the same folder as the script.
    """
    filename = None
    if name == "correct":
        filename = "correct.wav"
    elif name == "win":
        filename = "win.wav"
    if filename is None:
        return

    flags = winsound.SND_ASYNC | winsound.SND_FILENAME
    try:
        winsound.PlaySound(filename, flags)
    except RuntimeError:
        # Ignore sound errors so the game keeps running
        pass

class NumberGuessingGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Start in fullscreen
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.difficulty = None
        self.max_number = None
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 0

        # Trophy counters (loaded from file)
        self.bronze_trophies = 0
        self.silver_trophies = 0
        self.gold_trophies = 0
        self.platinum_trophies = 0
        self.load_trophies()

        # Effect state
        self.effect_mode = "none"  # "fire", "snow", or "none"
        self.effect_items = []
        self.effect_running = False

        # Base container
        self.base = tk.Frame(self.root, bg="black")
        self.base.pack(fill="both", expand=True)

        # Background canvas for effects (fills whole window)
        self.effect_canvas = tk.Canvas(self.base, bg="black", highlightthickness=0)
        self.effect_canvas.pack(fill="both", expand=True)

        # Foreground frame for UI, placed on top using place()
        self.content_frame = tk.Frame(self.base, bg="black")
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.root.bind("<Configure>", self.on_resize)

        self.show_difficulty_screen()

    # ---------- Trophy persistence ----------
    def load_trophies(self):
        if os.path.exists(TROPHY_FILE):
            try:
                with open(TROPHY_FILE, "r") as f:
                    data = json.load(f)
                self.bronze_trophies = data.get("bronze", 0)
                self.silver_trophies = data.get("silver", 0)
                self.gold_trophies = data.get("gold", 0)
                self.platinum_trophies = data.get("platinum", 0)
            except (json.JSONDecodeError, OSError):
                self.bronze_trophies = 0
                self.silver_trophies = 0
                self.gold_trophies = 0
                self.platinum_trophies = 0

    def save_trophies(self):
        data = {
            "bronze": self.bronze_trophies,
            "silver": self.silver_trophies,
            "gold": self.gold_trophies,
            "platinum": self.platinum_trophies,
        }
        try:
            with open(TROPHY_FILE, "w") as f:
                json.dump(data, f)
        except OSError:
            pass

    def reset_trophies(self):
        if messagebox.askyesno("Reset trophies", "Are you sure you want to reset all trophies?"):
            self.bronze_trophies = 0
            self.silver_trophies = 0
            self.gold_trophies = 0
            self.platinum_trophies = 0
            if os.path.exists(TROPHY_FILE):
                try:
                    os.remove(TROPHY_FILE)
                except OSError:
                    pass
            self.save_trophies()
            self.show_difficulty_screen()

    # ---------- Layout / UI ----------
    def on_resize(self, event):
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")

    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fullscreen)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_difficulty_screen(self):
        self.stop_effect()
        self.effect_canvas.config(bg="black")
        self.clear_content()

        title = tk.Label(self.content_frame, text="WELCOME TO THE NUMBER GUESSING GAME!",
                         font=("Arial", 24, "bold"), bg="black", fg="white")
        title.pack(pady=(0, 10))

        subtitle = tk.Label(self.content_frame, text="Choose your difficulty level:",
                            font=("Arial", 16), bg="black", fg="white")
        subtitle.pack(pady=(0, 5))

        hint = tk.Label(self.content_frame, text="Press Esc to toggle fullscreen",
                        font=("Arial", 10), fg="gray", bg="black")
        hint.pack(pady=(0, 15))

        # Trophy display on main menu
        trophies_frame = tk.Frame(self.content_frame, bg="black")
        trophies_frame.pack(pady=(0, 10))

        bronze_label = tk.Label(
            trophies_frame,
            text=f"🥉 Bronze (Easy): {self.bronze_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#cd7f32"
        )
        silver_label = tk.Label(
            trophies_frame,
            text=f"🥈 Silver (Medium): {self.silver_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#c0c0c0"
        )
        gold_label = tk.Label(
            trophies_frame,
            text=f"🥇 Gold (Hard): {self.gold_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#ffd700"
        )
        platinum_label = tk.Label(
            trophies_frame,
            text=f"🏆 Platinum (Platinum): {self.platinum_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#e5e4e2"
        )

        bronze_label.grid(row=0, column=0, padx=10)
        silver_label.grid(row=0, column=1, padx=10)
        gold_label.grid(row=0, column=2, padx=10)
        platinum_label.grid(row=0, column=3, padx=10)

        # Difficulty buttons
        btn_style = {"width": 30, "height": 2, "font": ("Arial", 14)}

        btn_easy = tk.Button(self.content_frame, text="Easy (1-25, 20 attempts)",
                             command=lambda: self.start_game("easy", 25, 20), **btn_style)
        btn_medium = tk.Button(self.content_frame, text="Medium (1-50, 10 attempts)",
                               command=lambda: self.start_game("medium", 50, 10), **btn_style)
        btn_hard = tk.Button(self.content_frame, text="Hard (1-100, 5 attempts)",
                             command=lambda: self.start_game("hard", 100, 5), **btn_style)

        # Platinum button (locked until at least 1 Gold trophy)
        if self.gold_trophies > 0:
            platinum_text = "Platinum (??? mode)"
            platinum_state = "normal"
            platinum_fg = "white"
        else:
            platinum_text = "Platinum (locked)"
            platinum_state = "disabled"
            platinum_fg = "gray"

        btn_platinum = tk.Button(
            self.content_frame,
            text=platinum_text,
            state=platinum_state,
            fg=platinum_fg,
            command=lambda: self.start_game("platinum", 1000, 100),
            **btn_style
        )

        btn_easy.pack(pady=3)
        btn_medium.pack(pady=3)
        btn_hard.pack(pady=3)
        btn_platinum.pack(pady=3)

        # Control buttons: trophies menu, reset, exit
        control_frame = tk.Frame(self.content_frame, bg="black")
        control_frame.pack(pady=(10, 0))

        btn_trophies = tk.Button(control_frame, text="Trophies",
                                 font=("Arial", 12),
                                 width=18, command=self.open_trophies_menu)
        btn_reset = tk.Button(control_frame, text="Reset trophies",
                              font=("Arial", 12),
                              width=18, command=self.reset_trophies)
        btn_exit = tk.Button(control_frame, text="Exit",
                             font=("Arial", 12),
                             width=18, command=self.root.quit)

        btn_trophies.grid(row=0, column=0, padx=5)
        btn_reset.grid(row=0, column=1, padx=5)
        btn_exit.grid(row=0, column=2, padx=5)

    # ---------- Trophies menu ----------
    def open_trophies_menu(self):
        win = tk.Toplevel(self.root)
        win.title("Trophies")
        win.configure(bg="black")
        win.geometry("520x340")

        title = tk.Label(win, text="TROPHIES", font=("Arial", 20, "bold"),
                         bg="black", fg="white")
        title.pack(pady=(10, 5))

        subtitle = tk.Label(win, text="Click a trophy to see its range and attempts.",
                            font=("Arial", 12), bg="black", fg="gray")
        subtitle.pack(pady=(0, 10))

        # Counts display
        counts_frame = tk.Frame(win, bg="black")
        counts_frame.pack(pady=(0, 10))

        lbl_bronze = tk.Label(
            counts_frame,
            text=f"🥉 Bronze unlocked: {self.bronze_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#cd7f32"
        )
        lbl_silver = tk.Label(
            counts_frame,
            text=f"🥈 Silver unlocked: {self.silver_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#c0c0c0"
        )
        lbl_gold = tk.Label(
            counts_frame,
            text=f"🥇 Gold unlocked: {self.gold_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#ffd700"
        )
        lbl_platinum = tk.Label(
            counts_frame,
            text=f"🏆 Platinum unlocked: {self.platinum_trophies}",
            font=("Arial", 12),
            bg="black",
            fg="#e5e4e2"
        )

        lbl_bronze.grid(row=0, column=0, padx=10, pady=2, sticky="w")
        lbl_silver.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        lbl_gold.grid(row=2, column=0, padx=10, pady=2, sticky="w")
        lbl_platinum.grid(row=3, column=0, padx=10, pady=2, sticky="w")

        # Buttons to show range/attempts
        frame = tk.Frame(win, bg="black")
        frame.pack(pady=10)

        btn_style = {"width": 18, "height": 2, "font": ("Arial", 12)}

        btn_bronze = tk.Button(frame, text="🥉 Bronze info", command=self.show_bronze_info, **btn_style)
        btn_silver = tk.Button(frame, text="🥈 Silver info", command=self.show_silver_info, **btn_style)
        btn_gold = tk.Button(frame, text="🥇 Gold info", command=self.show_gold_info, **btn_style)
        btn_platinum = tk.Button(frame, text="🏆 Platinum info", command=self.show_platinum_info, **btn_style)

        btn_bronze.grid(row=0, column=0, padx=8, pady=5)
        btn_silver.grid(row=0, column=1, padx=8, pady=5)
        btn_gold.grid(row=1, column=0, padx=8, pady=5)
        btn_platinum.grid(row=1, column=1, padx=8, pady=5)

    def show_bronze_info(self):
        messagebox.showinfo(
            "Bronze Trophy (Easy)",
            "Easy mode:\nNumber range: 1–25\nAttempts: 20"
        )

    def show_silver_info(self):
        messagebox.showinfo(
            "Silver Trophy (Medium)",
            "Medium mode:\nNumber range: 1–50\nAttempts: 10"
        )

    def show_gold_info(self):
        messagebox.showinfo(
            "Gold Trophy (Hard)",
            "Hard mode:\nNumber range: 1–100\nAttempts: 5"
        )

    def show_platinum_info(self):
        messagebox.showinfo(
            "Platinum Trophy (Platinum)",
            "Platinum mode:\nNumber range: 1–1000\nAttempts: 100"
        )

    # ---------- Game logic ----------
    def get_hint(self, guess, secret, max_range):
        difference = abs(guess - secret)
        range_10_percent = max_range * 0.1
        range_20_percent = max_range * 0.2

        if difference == 0:
            return "🎯 PERFECT! You got it!", "none"
        elif difference <= range_10_percent:
            return "🔥 VERY HOT! You're extremely close!", "fire"
        elif difference <= range_20_percent:
            return "🌡️ HOT! You're getting close!", "fire"
        elif difference <= range_20_percent * 2:
            return "🌤️ WARM! You're on the right track!", "none"
        elif difference <= range_20_percent * 3:
            return "❄️ COLD! You're not very close.", "snow"
        else:
            return "🧊 VERY COLD! You're far away!", "snow"

    def start_game(self, difficulty, max_number, max_attempts):
        self.difficulty = difficulty
        self.max_number = max_number
        self.max_attempts = max_attempts

        # Secret number is a multiple of 10 within the range
        lowest = 10
        highest = (max_number // 10) * 10
        self.secret_number = random.randrange(lowest, highest + 1, 10)

        self.attempts = 0
        self.show_game_screen()

    def show_game_screen(self):
        self.stop_effect()
        # Platinum has a slightly different tint
        if self.difficulty == "platinum":
            self.effect_canvas.config(bg="#101020")
        else:
            self.effect_canvas.config(bg="black")
        self.clear_content()

        info = tk.Label(
            self.content_frame,
            text=(
                f"🎮 Starting {self.difficulty.upper()} mode!\n"
                f"I'm thinking of a number between 1 and {self.max_number}.\n"
                f"You have {self.max_attempts} attempts. Can you guess it?"
            ),
            font=("Arial", 20),
            bg="black",
            fg="white"
        )
        info.pack(pady=(0, 20))

        self.hearts_label = tk.Label(
            self.content_frame,
            text=self.get_hearts_text(),
            font=("Arial", 24),
            fg="red",
            bg="black"
        )
        self.hearts_label.pack(pady=(0, 10))

        self.attempts_label = tk.Label(
            self.content_frame,
            text=f"Attempts: {self.attempts}/{self.max_attempts}",
            font=("Arial", 16),
            bg="black",
            fg="white"
        )
        self.attempts_label.pack(pady=(0, 10))

        self.feedback_label = tk.Label(self.content_frame, text="", font=("Arial", 16),
                                       bg="black", fg="white")
        self.feedback_label.pack(pady=10)

        entry_label = tk.Label(self.content_frame, text=f"Enter your guess (1-{self.max_number}):",
                               font=("Arial", 16), bg="black", fg="white")
        entry_label.pack(pady=(20, 5))

        self.guess_entry = tk.Entry(self.content_frame, width=10, font=("Arial", 18))
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        btn_frame = tk.Frame(self.content_frame, bg="black")
        btn_frame.pack(pady=(20, 0))

        submit_btn = tk.Button(btn_frame, text="Submit Guess", font=("Arial", 14),
                               width=15, command=self.check_guess)
        submit_btn.grid(row=0, column=0, padx=10)

        back_btn = tk.Button(btn_frame, text="Change Difficulty", font=("Arial", 14),
                             width=15, command=self.show_difficulty_screen)
        back_btn.grid(row=0, column=1, padx=10)

    def get_hearts_text(self):
        remaining = self.max_attempts - self.attempts
        if remaining < 0:
            remaining = 0
        return "♥ " * remaining

    def award_trophy(self):
        unlocked_platinum_now = False

        if self.difficulty == "easy":
            self.bronze_trophies += 1
            trophy_msg = "🥉 You earned a Bronze trophy for Easy!"
        elif self.difficulty == "medium":
            self.silver_trophies += 1
            trophy_msg = "🥈 You earned a Silver trophy for Medium!"
        elif self.difficulty == "hard":
            # If this is the first Gold, Platinum unlocks
            if self.gold_trophies == 0:
                unlocked_platinum_now = True
            self.gold_trophies += 1
            trophy_msg = "🥇 You earned a Gold trophy for Hard!"
        elif self.difficulty == "platinum":
            self.platinum_trophies += 1
            trophy_msg = "🏆 You earned a Platinum trophy for Platinum mode!"
        else:
            trophy_msg = ""

        self.save_trophies()

        # Show unlock popup once when first Gold is earned
        if unlocked_platinum_now:
            messagebox.showinfo(
                "Platinum Unlocked!",
                "You earned your first Gold trophy!\n\n"
                "Platinum mode is now unlocked on the main menu."
            )

        return trophy_msg

    def check_guess(self):
        guess_text = self.guess_entry.get().strip()
        if not guess_text.isdigit():
            self.feedback_label.config(text="❌ Invalid input! Please enter a valid number.")
            return

        guess = int(guess_text)
        if guess < 1 or guess > self.max_number:
            self.feedback_label.config(text=f"❌ Please enter a number between 1 and {self.max_number}!")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        self.hearts_label.config(text=self.get_hearts_text())

        if guess == self.secret_number:
            play_sound("correct")
            play_sound("win")
            self.stop_effect()
            trophy_msg = self.award_trophy()
            messagebox.showinfo(
                "Congratulations",
                f"🎉 You guessed the number {self.secret_number} in {self.attempts} attempt(s)!\n\n{trophy_msg}"
            )
            self.ask_play_again()
            return

        if self.attempts < self.max_attempts:
            hint_text, effect = self.get_hint(guess, self.secret_number, self.max_number)
            direction_text = "HIGHER" if guess < self.secret_number else "LOWER"
            self.feedback_label.config(text=f"{hint_text}\n💡 Hint: The number is {direction_text} than {guess}")
            self.set_effect(effect)
        else:
            self.stop_effect()
            messagebox.showinfo(
                "Out of attempts",
                f"😢 You're out of attempts!\nThe number was {self.secret_number}."
            )
            self.ask_play_again()

        self.guess_entry.delete(0, tk.END)

    # -------- effects --------
    def set_effect(self, mode):
        if mode == self.effect_mode:
            return
        self.effect_mode = mode
        self.stop_effect()
        if mode == "fire":
            self.start_fire_effect()
        elif mode == "snow":
            self.start_snow_effect()

    def stop_effect(self):
        self.effect_running = False
        self.effect_canvas.delete("all")
        self.effect_items = []

    # Fire effect: bottom strip
    def start_fire_effect(self):
        self.effect_running = True
        self.effect_canvas.config(bg="black")
        self.effect_items = []
        self.spawn_fire_particles()
        self.animate_fire()

    def spawn_fire_particles(self):
        width = self.effect_canvas.winfo_width()
        height = self.effect_canvas.winfo_height()
        if width <= 1:
            width = self.root.winfo_width()
        if height <= 1:
            height = self.root.winfo_height()
        for _ in range(25):
            x = random.randint(0, max(10, width))
            y = height - random.randint(0, 40)
            size = random.randint(4, 10)
            color = random.choice(["#ff5500", "#ff9900", "#ffdd33", "#ff2200"])
            rect = self.effect_canvas.create_oval(
                x, y, x + size, y + size,
                fill=color, outline=""
            )
            speed = random.uniform(1.5, 3.5)
            self.effect_items.append({"id": rect, "vx": random.uniform(-0.5, 0.5),
                                      "vy": -speed, "type": "fire"})

    def animate_fire(self):
        if not self.effect_running or self.effect_mode != "fire":
            return
        width = self.effect_canvas.winfo_width()
        height = self.effect_canvas.winfo_height()

        for p in self.effect_items:
            self.effect_canvas.move(p["id"], p["vx"], p["vy"])
            x1, y1, x2, y2 = self.effect_canvas.coords(p["id"])
            if y2 < height * 0.7:
                size = x2 - x1
                new_x = random.randint(0, max(10, width))
                new_y = height - random.randint(0, 40)
                self.effect_canvas.coords(
                    p["id"],
                    new_x, new_y,
                    new_x + size, new_y + size
                )
        if random.random() < 0.2:
            self.spawn_fire_particles()
        self.root.after(50, self.animate_fire)

    # Snow effect: flakes fall all over window and disappear on ground
    def start_snow_effect(self):
        self.effect_running = True
        self.effect_canvas.config(bg="#001528")
        self.effect_items = []
        self.spawn_snowflakes(initial=True)
        self.animate_snow()

    def spawn_snowflakes(self, initial=False):
        width = self.effect_canvas.winfo_width()
        height = self.effect_canvas.winfo_height()
        if width <= 1:
            width = self.root.winfo_width()
        if height <= 1:
            height = self.root.winfo_height()

        count = 60 if initial else 10
        for _ in range(count):
            x = random.randint(0, max(10, width))
            y = random.randint(-height, 0) if initial else -10
            size = random.randint(3, 8)
            snow = self.effect_canvas.create_oval(
                x, y, x + size, y + size,
                fill="white", outline=""
            )
            speed = random.uniform(1.0, 2.5)
            self.effect_items.append({"id": snow, "vx": random.uniform(-0.5, 0.5),
                                      "vy": speed, "type": "snow"})

    def animate_snow(self):
        if not self.effect_running or self.effect_mode != "snow":
            return
        height = self.effect_canvas.winfo_height()

        to_remove = []
        for p in self.effect_items:
            self.effect_canvas.move(p["id"], p["vx"], p["vy"])
            x1, y1, x2, y2 = self.effect_canvas.coords(p["id"])
            if y1 >= height:
                self.effect_canvas.delete(p["id"])
                to_remove.append(p)

        for p in to_remove:
            self.effect_items.remove(p)

        if len(self.effect_items) < 100:
            self.spawn_snowflakes(initial=False)

        self.root.after(40, self.animate_snow)

    def ask_play_again(self):
        answer = messagebox.askyesno("Play Again", "Would you like to play again?")
        if answer:
            self.show_difficulty_screen()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGameUI(root)
    root.mainloop()
