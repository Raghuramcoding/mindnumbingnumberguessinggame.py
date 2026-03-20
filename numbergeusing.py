import random
import tkinter as tk
from tkinter import messagebox

class NumberGuessingGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")

        self.difficulty = None
        self.max_number = None
        self.secret_number = None
        self.attempts = 0

        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        self.show_difficulty_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_difficulty_screen(self):
        self.clear_frame()
        title = tk.Label(self.main_frame, text="WELCOME TO THE NUMBER GUESSING GAME!", font=("Arial", 16, "bold"))
        title.pack(pady=(0, 10))

        subtitle = tk.Label(self.main_frame, text="Choose your difficulty level:", font=("Arial", 12))
        subtitle.pack(pady=(0, 10))

        btn_easy = tk.Button(self.main_frame, text="Easy (1-25)", width=20, command=lambda: self.start_game("easy", 25))
        btn_medium = tk.Button(self.main_frame, text="Medium (1-50)", width=20, command=lambda: self.start_game("medium", 50))
        btn_hard = tk.Button(self.main_frame, text="Hard (1-100)", width=20, command=lambda: self.start_game("hard", 100))
        btn_exit = tk.Button(self.main_frame, text="Exit", width=20, command=self.root.quit)

        btn_easy.pack(pady=5)
        btn_medium.pack(pady=5)
        btn_hard.pack(pady=5)
        btn_exit.pack(pady=(15, 0))

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

    def start_game(self, difficulty, max_number):
        self.difficulty = difficulty
        self.max_number = max_number
        self.secret_number = random.randint(1, max_number)
        self.attempts = 0
        self.show_game_screen()

    def show_game_screen(self):
        self.clear_frame()

        info = tk.Label(
            self.main_frame,
            text=f"🎮 Starting {self.difficulty.upper()} mode!\nI've thought of a number between 1 and {self.max_number}.\nCan you guess it?",
            font=("Arial", 12)
        )
        info.pack(pady=(0, 10))

        self.feedback_label = tk.Label(self.main_frame, text="", font=("Arial", 11))
        self.feedback_label.pack(pady=5)

        entry_label = tk.Label(self.main_frame, text=f"Enter your guess (1-{self.max_number}):", font=("Arial", 11))
        entry_label.pack(pady=(10, 0))

        self.guess_entry = tk.Entry(self.main_frame, width=10, font=("Arial", 12))
        self.guess_entry.pack(pady=5)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=(10, 0))

        submit_btn = tk.Button(btn_frame, text="Submit Guess", command=self.check_guess)
        submit_btn.grid(row=0, column=0, padx=5)

        back_btn = tk.Button(btn_frame, text="Change Difficulty", command=self.show_difficulty_screen)
        back_btn.grid(row=0, column=1, padx=5)

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

        if guess == self.secret_number:
            messagebox.showinfo(
                "Congratulations",
                f"🎉 You guessed the number {self.secret_number} in {self.attempts} attempt(s)!"
            )
            self.ask_play_again()
        elif guess < self.secret_number:
            hint = self.get_hint(guess, self.secret_number, self.max_number)
            self.feedback_label.config(text=f"{hint}\n💡 Hint: The number is HIGHER than {guess}")
        else:
            hint = self.get_hint(guess, self.secret_number, self.max_number)
            self.feedback_label.config(text=f"{hint}\n💡 Hint: The number is LOWER than {guess}")

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
