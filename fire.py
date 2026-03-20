import random
import tkinter as tk
from tkinter import messagebox

class NumberGuessingGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Start in fullscreen
        self.root.attributes("-fullscreen", True)
        # Escape toggles fullscreen
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.difficulty = None
        self.max_number = None
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 0

        # Effect state
        self.effect_mode = "none"  # "fire", "snow", or "none"
        self.effect_items = []
        self.effect_running = False

        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Top/main UI frame
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)

        # Bottom canvas for fire/snow
        self.effect_canvas_height = 150
        self.effect_canvas = tk.Canvas(
            self.main_frame,
            height=self.effect_canvas_height,
            bg="black",
            highlightthickness=0
        )
        self.effect_canvas.pack(fill="x", side="bottom")

        self.show_difficulty_screen()

    def toggle_fullscreen(self, event=None):
        is_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fullscreen)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_difficulty_screen(self):
        self.stop_effect()
        self.clear_content()

        title = tk.Label(self.content_frame, text="WELCOME TO THE NUMBER GUESSING GAME!",
                         font=("Arial", 24, "bold"))
        title.pack(pady=(0, 20))

        subtitle = tk.Label(self.content_frame, text="Choose your difficulty level:",
                            font=("Arial", 16))
        subtitle.pack(pady=(0, 10))

        hint = tk.Label(self.content_frame, text="Press Esc to toggle fullscreen",
                        font=("Arial", 10), fg="gray")
        hint.pack(pady=(0, 20))

        btn_easy = tk.Button(self.content_frame, text="Easy (1-25, 20 attempts)", width=30, height=2,
                             font=("Arial", 14),
                             command=lambda: self.start_game("easy", 25, 20))
        btn_medium = tk.Button(self.content_frame, text="Medium (1-50, 10 attempts)", width=30, height=2,
                               font=("Arial", 14),
                               command=lambda: self.start_game("medium", 50, 10))
        btn_hard = tk.Button(self.content_frame, text="Hard (1-100, 5 attempts)", width=30, height=2,
                             font=("Arial", 14),
                             command=lambda: self.start_game("hard", 100, 5))
        btn_exit = tk.Button(self.content_frame, text="Exit", width=30, height=2,
                             font=("Arial", 14),
                             command=self.root.quit)

        btn_easy.pack(pady=10)
        btn_medium.pack(pady=10)
        btn_hard.pack(pady=10)
        btn_exit.pack(pady=(30, 0))

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
        self.secret_number = random.randint(1, max_number)
        self.attempts = 0
        self.show_game_screen()

    def show_game_screen(self):
        self.stop_effect()
        self.clear_content()

        info = tk.Label(
            self.content_frame,
            text=(
                f"🎮 Starting {self.difficulty.upper()} mode!\n"
                f"I've thought of a number between 1 and {self.max_number}.\n"
                f"You have {self.max_attempts} attempts. Can you guess it?"
            ),
            font=("Arial", 20)
        )
        info.pack(pady=(0, 20))

        self.hearts_label = tk.Label(
            self.content_frame,
            text=self.get_hearts_text(),
            font=("Arial", 24),
            fg="red"
        )
        self.hearts_label.pack(pady=(0, 10))

        self.attempts_label = tk.Label(
            self.content_frame,
            text=f"Attempts: {self.attempts}/{self.max_attempts}",
            font=("Arial", 16)
        )
        self.attempts_label.pack(pady=(0, 10))

        self.feedback_label = tk.Label(self.content_frame, text="", font=("Arial", 16))
        self.feedback_label.pack(pady=10)

        entry_label = tk.Label(self.content_frame, text=f"Enter your guess (1-{self.max_number}):",
                               font=("Arial", 16))
        entry_label.pack(pady=(20, 5))

        self.guess_entry = tk.Entry(self.content_frame, width=10, font=("Arial", 18))
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        btn_frame = tk.Frame(self.content_frame)
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
            self.stop_effect()
            messagebox.showinfo(
                "Congratulations",
                f"🎉 You guessed the number {self.secret_number} in {self.attempts} attempt(s)!"
            )
            self.ask_play_again()
            return

        # If guess is wrong but attempts remain, show hint and effect
        if self.attempts < self.max_attempts:
            hint_text, effect = self.get_hint(guess, self.secret_number, self.max_number)
            if effect == "fire":
                direction_text = "HIGHER" if guess < self.secret_number else "LOWER"
            elif effect == "snow":
                direction_text = "HIGHER" if guess < self.secret_number else "LOWER"
            else:
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

    # Visual effects control
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

    # Fire effect: small rising rectangles with warm colors
    def start_fire_effect(self):
        self.effect_running = True
        self.effect_canvas.config(bg="black")
        self.effect_items = []
        self.spawn_fire_particles()
        self.animate_fire()

    def spawn_fire_particles(self):
        width = self.effect_canvas.winfo_width()
        if width == 1:  # not yet drawn, estimate
            width = self.root.winfo_width()
        for _ in range(20):
            x = random.randint(0, max(10, width))
            y = self.effect_canvas_height - random.randint(0, 20)
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
        height = self.effect_canvas_height

        for p in self.effect_items:
            self.effect_canvas.move(p["id"], p["vx"], p["vy"])
            x1, y1, x2, y2 = self.effect_canvas.coords(p["id"])
            # If above the top, respawn near bottom
            if y2 < 0:
                self.effect_canvas.coords(
                    p["id"],
                    random.randint(0, max(10, width)),
                    height - random.randint(0, 20),
                    random.randint(0, max(10, width)) + (x2 - x1),
                    height - random.randint(0, 20) + (y2 - y1)
                )
        # Occasionally spawn more
        if random.random() < 0.2:
            self.spawn_fire_particles()
        self.root.after(50, self.animate_fire)

    # Snow effect: falling white circles
    def start_snow_effect(self):
        self.effect_running = True
        self.effect_canvas.config(bg="#001528")
        self.effect_items = []
        self.spawn_snowflakes()
        self.animate_snow()

    def spawn_snowflakes(self):
        width = self.effect_canvas.winfo_width()
        if width == 1:
            width = self.root.winfo_width()
        for _ in range(20):
            x = random.randint(0, max(10, width))
            y = random.randint(-self.effect_canvas_height, 0)
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
        width = self.effect_canvas.winfo_width()
        height = self.effect_canvas_height

        for p in self.effect_items:
            self.effect_canvas.move(p["id"], p["vx"], p["vy"])
            x1, y1, x2, y2 = self.effect_canvas.coords(p["id"])
            if y1 > height:
                # respawn at top
                new_x = random.randint(0, max(10, width))
                size = x2 - x1
                self.effect_canvas.coords(
                    p["id"],
                    new_x, -size,
                    new_x + size, 0
                )
        # Occasionally spawn more
        if random.random() < 0.2:
            self.spawn_snowflakes()
        self.root.after(60, self.animate_snow)

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
