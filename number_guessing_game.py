import random

def get_difficulty():
    """Get the difficulty level from the user."""
    while True:
        print("\n" + "="*50)
        print("WELCOME TO THE NUMBER GUESSING GAME!")
        print("="*50)
        print("\nChoose your difficulty level:")
        print("1. Easy (1-25)")
        print("2. Medium (1-50)")
        print("3. Hard (1-100)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            return 'easy', 25
        elif choice == '2':
            return 'medium', 50
        elif choice == '3':
            return 'hard', 100
        elif choice == '4':
            print("\nThanks for playing! Goodbye!")
            return None, None
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, 3, or 4.")

def get_hint(guess, secret, max_range):
    """Generate a hint based on how close the guess is to the secret number."""
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

def play_game(difficulty, max_number):
    """Play one round of the guessing game."""
    secret_number = random.randint(1, max_number)
    attempts = 0
    guessed = False
    
    print(f"\n🎮 Starting {difficulty.upper()} mode!")
    print(f"I've thought of a number between 1 and {max_number}.")
    print("Can you guess it?\n")
    
    while not guessed:
        try:
            guess = int(input(f"Enter your guess (1-{max_number}): "))
            
            # Validate the input
            if guess < 1 or guess > max_number:
                print(f"❌ Please enter a number between 1 and {max_number}!\n")
                continue
            
            attempts += 1
            
            if guess == secret_number:
                print(f"\n🎉 Congratulations! You guessed the number {secret_number} in {attempts} attempt(s)!")
                guessed = True
            elif guess < secret_number:
                hint = get_hint(guess, secret_number, max_number)
                print(f"{hint}")
                print(f"💡 Hint: The number is HIGHER than {guess}\n")
            else:
                hint = get_hint(guess, secret_number, max_number)
                print(f"{hint}")
                print(f"💡 Hint: The number is LOWER than {guess}\n")
        
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.\n")

def main():
    """Main function to run the game loop."""
    play_again = True
    
    while play_again:
        difficulty, max_number = get_difficulty()
        
        if difficulty is None:
            break
        
        play_game(difficulty, max_number)
        
        # Ask if the user wants to play again
        while True:
            response = input("\nWould you like to play again? (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                break
            elif response in ['no', 'n']:
                play_again = False
                print("\n🙏 Thanks for playing! See you next time!")
                break
            else:
                print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()