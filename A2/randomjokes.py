import tkinter as tk
import random

root = tk.Tk()
root.title("Fun Joke Time")
root.geometry("900x700")
root.resizable(False, False)

jokes = [
    ("Why did the chicken cross the road?", "To get to the other side."),
    ("What happens if you boil a clown?", "You get a laughing stock."),
    ("Why did the car get a flat tire?", "Because there was a fork in the road!"),
    ("How did the hipster burn his mouth?", "He ate his pizza before it was cool."),
    ("What did the janitor say when he jumped out of the closet?", "SUPPLIES!!!!"),
    ("Have you heard about the band 1023MB?", "It's probably because they haven't got a gig yet…"),
    ("Why does the golfer wear two pants?", "Because he's afraid he might get a 'Hole-in-one.'"),
    ("Why should you wear glasses to maths class?", "Because it helps with division."),
    ("Why does it take pirates so long to learn the alphabet?", "Because they could spend years at C."),
    ("Why did the woman go on the date with the mushroom?", "Because he was a fun-ghi."),
    ("Why do bananas never get lonely?", "Because they hang out in bunches."),
    ("What did the buffalo say when his kid went to college?", "Bison."),
    ("Why shouldn't you tell secrets in a cornfield?", "Too many ears."),
    ("What do you call someone who doesn't like carbs?", "Lack-Toast Intolerant."),
    ("Why did the can crusher quit his job?", "Because it was soda pressing."),
    ("Why did the birthday boy wrap himself in paper?", "He wanted to live in the present."),
    ("What does a house wear?", "A dress."),
    ("Why couldn't the toilet paper cross the road?", "Because it got stuck in a crack."),
    ("Why didn't the bike want to go anywhere?", "Because it was two-tired!"),
    ("Want to hear a pizza joke?", "Nahhh, it's too cheesy!"),
    ("Why are chemists great at solving problems?", "Because they have all of the solutions!"),
    ("Why is it impossible to starve in the desert?", "Because of all the sand which is there!"),
    ("What did the cheese say when it looked in the mirror?", "Halloumi!"),
    ("Why did the developer go broke?", "Because he used up all his cache."),
    ("Did you know that ants are the only animals that don't get sick?", "It's true! They have little antibodies."),
    ("Why did the donut go to the dentist?", "To get a filling."),
    ("What do you call a bear with no teeth?", "A gummy bear!"),
    ("What does a vegan zombie like to eat?", "Graaains."),
    ("What do you call a dinosaur with only one eye?", "A Do-you-think-he-saw-us!"),
    ("Why should you never fall in love with a tennis player?", "Because to them... love means NOTHING!"),
]

random.shuffle(jokes)

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#1f1f2f")
        self.index = 0

        self.emoji_label = tk.Label(root, text="", font=("Arial", 28), bg="#1f1f2f", fg="#ffdd57")
        self.emoji_label.pack(pady=15)
        self.animate_emojis()

        self.title_label = tk.Label(root, text="😂 Fun Joke Time 😂", font=("Comic Sans MS", 32, "bold"), bg="#1f1f2f", fg="#ff6f61")
        self.title_label.pack(pady=20)

        self.progress_label = tk.Label(root, text=f"Joke {self.index+1} of {len(jokes)}", font=("Arial", 14), bg="#1f1f2f", fg="#f5f5f5")
        self.progress_label.pack(pady=5)

        self.joke_frame = tk.Frame(root, bg="#2e2e44", bd=5, relief="ridge")
        self.joke_frame.pack(pady=30, padx=50, fill="both", expand=True)

        self.joke_label = tk.Label(self.joke_frame, text="", font=("Arial", 20), bg="#2e2e44", fg="#ffffff", wraplength=800, justify="center")
        self.joke_label.pack(pady=50, padx=20)

        self.punchline_button = tk.Button(root, text="Show Punchline", font=("Arial", 16, "bold"), bg="#ff6f61", fg="#1f1f2f", width=18, command=self.show_punchline)
        self.punchline_button.pack(pady=10)

        self.next_button = tk.Button(root, text="Next Joke", font=("Arial", 16, "bold"), bg="#6a67ce", fg="#ffffff", width=18, command=self.next_joke)
        self.next_button.pack(pady=10)
        self.next_button.pack_forget()

        self.quit_button = tk.Button(root, text="Quit", font=("Arial", 16, "bold"), bg="#e74c3c", fg="#ffffff", width=18, command=root.quit)
        self.quit_button.pack(pady=10)

        self.show_joke()

    def animate_emojis(self):
        emojis = ["💀", "🤣", "😒", "😂", "😍", "👌", "😭", "😎", "🤪", "🙃"]
        self.emoji_label.config(text=" ".join(random.choices(emojis, k=7)))
        self.root.after(400, self.animate_emojis)

    def show_joke(self):
        self.joke_label.config(text=jokes[self.index][0])
        self.punchline_button.pack(pady=10)
        self.next_button.pack_forget()
        self.progress_label.config(text=f"Joke {self.index+1} of {len(jokes)}")

    def show_punchline(self):
        setup, punchline = jokes[self.index]
        self.joke_label.config(text=f"{setup}\n\n➡ {punchline}")
        self.punchline_button.pack_forget()
        self.next_button.pack(pady=10)

    def next_joke(self):
        self.index = (self.index + 1) % len(jokes)
        self.show_joke()

app = JokeApp(root)
root.mainloop()
