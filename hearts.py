import random
import tkinter as tk
from tkinter import messagebox

class NumberGuessingGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        # Start in fullscreen
        self.root.attributes("-fullscreen", True)
        # Allow exiting fullscreen with Escape
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.difficulty = None
        self.max_number = None
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = 0

        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        self.show_difficulty_screen()

    def toggle_fullscreen(self, event=None):
        # Toggle fullscreen on/off
        is_fullscreen = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not is_fullscreen)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_difficulty_screen(self):
        self.clear_frame()
        title = tk.Label(self.main_frame, text="WELCOME TO THE NUMBER GUESSING GAME!", font=("Arial", 24, "bold"))
        title.pack(pady=(0, 20))

        subtitle = tk.Label(self.main_frame, text="Choose your difficulty level:", font=("Arial", 16))
        subtitle.pack(pady=(0, 20))

        btn_easy = tk.Button(self.main_frame, text="Easy (1-25, 20 attempts)", width=30, height=2,
                             font=("Arial", 14),
                             command=lambda: self.start_game("easy", 25, 20))
        btn_medium = tk.Button(self.main_frame, text="Medium (1-50, 10 attempts)", width=30, height=2,
                               font=("Arial", 14),
                               command=lambda: self.start_game("medium", 50, 10))
        btn_hard = tk.Button(self.main_frame, text="Hard (1-100, 5 attempts)", width=30, height=2,
                             font=("Arial", 14),
                             command=lambda: self.start_game("hard", 100, 5))
        btn_exit = tk.Button(self.main_frame, text="Exit", width=30, height=2,
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
            return "🎯 PERFECT! You got it!"
        elif difference <= range_10_percent:
            return "🔥 VERY HOT! You're extremely close!"
        elif difference <= range_20_percent:
            return "🌡️ HOT! You're getting close!"
        elif difference <= range_20_percent * 2:
            return "🌤️ WARM! You're on the right track!"
        elif difference <= range_20_percent * 3:
            return "❄️ COLD! You're not very close."
        else:
            return "🧊 VERY COLD! You're far away!"

    def start_game(self, difficulty, max_number, max_attempts):
        self.difficulty = difficulty
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.secret_number = random.randint(1, max_number)
        self.attempts = 0
        self.show_game_screen()

    def show_game_screen(self):
        self.clear_frame()

        info = tk.Label(
            self.main_frame,
            text=(
                f"🎮 Starting {self.difficulty.upper()} mode!\n"
                f"I've thought of a number between 1 and {self.max_number}.\n"
                f"You have {self.max_attempts} attempts. Can you guess it?"
            ),
            font=("Arial", 20)
        )
        info.pack(pady=(0, 20))

        # Hearts for remaining attempts
        self.hearts_label = tk.Label(
            self.main_frame,
            text=self.get_hearts_text(),
            font=("Arial", 24),
            fg="red"
        )
        self.hearts_label.pack(pady=(0, 10))

        self.attempts_label = tk.Label(
            self.main_frame,
            text=f"Attempts: {self.attempts}/{self.max_attempts}",
            font=("Arial", 16)
        )
        self.attempts_label.pack(pady=(0, 10))

        self.feedback_label = tk.Label(self.main_frame, text="", font=("Arial", 16))
        self.feedback_label.pack(pady=10)

        entry_label = tk.Label(self.main_frame, text=f"Enter your guess (1-{self.max_number}):", font=("Arial", 16))
        entry_label.pack(pady=(20, 5))

        self.guess_entry = tk.Entry(self.main_frame, width=10, font=("Arial", 18))
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        btn_frame = tk.Frame(self.main_frame)
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
            messagebox.showinfo(
                "Congratulations",
                f"🎉 You guessed the number {self.secret_number} in {self.attempts} attempt(s)!"
            )
            self.ask_play_again()
            return

        # If guess is wrong but attempts remain, show hint
        if self.attempts < self.max_attempts:
            if guess < self.secret_number:
                hint = self.get_hint(guess, self.secret_number, self.max_number)
                self.feedback_label.config(text=f"{hint}\n💡 Hint: The number is HIGHER than {guess}")
            else:
                hint = self.get_hint(guess, self.secret_number, self.max_number)
                self.feedback_label.config(text=f"{hint}\n💡 Hint: The number is LOWER than {guess}")
        else:
            # Out of attempts
            messagebox.showinfo(
                "Out of attempts",
                f"😢 You're out of attempts!\nThe number was {self.secret_number}."
            )
            self.ask_play_again()

        self.guess_entry.delete(0, tk.END)

    def ask_play_again(self):
        answer = messagebox.askyesno("Play Again", "Would you like to play again?")
        if answer:
            self.show_difficulty_screen()
        else:
            messagebox.showinfo("Goodbye", "🙏 Thanks for playing! See you next time!")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumberGuessingGameUI(root)
    root.mainloop()
