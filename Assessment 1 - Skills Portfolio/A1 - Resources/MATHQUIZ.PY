import tkinter as tk
from tkinter import messagebox, ttk
import random
import operator

# Map operator symbols to the actual Python function for calculation
OPERATIONS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

class MathQuizApp:
    """Handles the math quiz application, including UI, state, and game logic."""
    def __init__(self, root):
        # Initialize the main Tkinter window
        self.root = root
        self.root.title("Math Quiz")
        self.root.geometry("650x520")
        self.root.resizable(False, False)

        self.setup_style()
        self.init_variables()
        self.create_pages()
        self.show_page(self.start_page)

        # Bind the Enter key to automatically check the answer
        self.root.bind('<Return>', self.handle_enter_key)

    def setup_style(self):
        # Configures the aesthetic style using ttk
        style = ttk.Style()
        style.theme_use('clam') 

        # Define color palette for modern look (Aesthetics updated here)
        BACKGROUND_COLOR = '#FCFCFC' # Clean, subtle off-white background
        PRIMARY_COLOR = '#673AB7'    # Deep Purple for title and main accent (Title Color Changed)
        SUCCESS_COLOR = '#4CAF50'
        DANGER_COLOR = '#EF5350'
        FONT_FAMILY = 'Arial'

        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Configure standard widgets
        style.configure('.', background=BACKGROUND_COLOR, foreground='#333333', font=(FONT_FAMILY, 12))
        style.configure('TFrame', background=BACKGROUND_COLOR)
        style.configure('TLabel', background=BACKGROUND_COLOR)

        # Header Title: Now Deep Purple
        style.configure('Header.TLabel', font=(FONT_FAMILY, 28, 'bold'), foreground=PRIMARY_COLOR)
        style.configure('Info.TLabel', font=(FONT_FAMILY, 14))
        style.configure('Question.TLabel', font=('Consolas', 38, 'bold'), foreground='#263238')
        
        # Configure standard button style (Aesthetics: increased padding and raised relief)
        style.configure('TButton', 
                        font=(FONT_FAMILY, 13, 'bold'), 
                        padding=[25, 14], 
                        relief='raised',
                        background=PRIMARY_COLOR, 
                        foreground='white')
        style.map('TButton', 
                  background=[('active', '#5E35B1')], # Darker purple on active
                  foreground=[('active', 'white')])

        # Configure difficulty specific buttons 
        style.configure('Easy.TButton', background=SUCCESS_COLOR)
        style.map('Easy.TButton', background=[('active', '#388E3C')])

        style.configure('Moderate.TButton', background='#FFB300') 
        style.map('Moderate.TButton', background=[('active', '#FFA000')])
        
        style.configure('Advanced.TButton', background=DANGER_COLOR) 
        style.map('Advanced.TButton', background=[('active', '#D32F2F')])
        
        # Entry/Input field (Aesthetics: clear white background)
        style.configure('TEntry', font=(FONT_FAMILY, 24), padding=10, fieldbackground='#FFFFFF', foreground='#333333') 
        
        # Progress bar style (Slightly thicker)
        style.configure("Quiz.Horizontal.TProgressbar", 
                        thickness=18, 
                        troughcolor='#E0E0E0', 
                        bordercolor=BACKGROUND_COLOR, 
                        background=PRIMARY_COLOR)

    def init_variables(self):
        # Initialize core game state variables
        self.difficulty = 1
        self.score = 0
        self.question_number = 0
        self.total_questions = 10
        self.correct_answer = None
        self.second_try = False
        # References to UI elements for dynamic updates
        self.quiz_title = None
        self.quiz_question = None
        self.quiz_answer = None
        self.progress = None
        self.current_score_label = None

    def show_page(self, page):
        # Simple page navigation function
        for p in [self.start_page, self.mode_page, self.quiz_page, self.end_page]:
            p.pack_forget()
        page.pack(fill="both", expand=True)

    def handle_enter_key(self, event):
        # Submit answer on Enter press only when the quiz page is visible
        if self.quiz_page.winfo_ismapped():
            self.check_answer()

    # --- Page Creation Methods ---

    def create_pages(self):
        self.create_start_page()
        self.create_mode_page()
        self.create_quiz_page()
        self.create_end_page()

    def create_start_page(self):
        # Setup the initial welcome page
        self.start_page = ttk.Frame(self.root, padding="40 70")

        ttk.Label(self.start_page, text="🧠 Math Quiz 🏋️", style='Header.TLabel').pack(pady=40)

        ttk.Button(self.start_page, text="Start Challenge",
                   command=lambda: self.show_page(self.mode_page),
                   width=20, style='TButton').pack(pady=30)

    def create_mode_page(self):
        # Setup the difficulty selection page
        self.mode_page = ttk.Frame(self.root, padding="25 50")

        ttk.Label(self.mode_page, text="Select Difficulty", style='Header.TLabel').pack(pady=30)

        desc_frame = ttk.Frame(self.mode_page, padding=10)
        desc_frame.pack(pady=20, padx=50, fill='x')
        ttk.Label(desc_frame, text="Easy: (+, -) Small integers (1-10).", style='Info.TLabel', anchor='w').pack(fill='x', pady=2)
        ttk.Label(desc_frame, text="Moderate: (+, -, *) Larger integers (10-100).", style='Info.TLabel', anchor='w').pack(fill='x', pady=2)
        ttk.Label(desc_frame, text="Advanced: (+, -, *, /) Up to thousands (20-1000).", style='Info.TLabel', anchor='w').pack(fill='x', pady=2)

        button_frame = ttk.Frame(self.mode_page)
        button_frame.pack(pady=30)

        btns = [
            ("Easy", 1, 'Easy.TButton'),
            ("Moderate", 2, 'Moderate.TButton'),
            ("Advanced", 3, 'Advanced.TButton')
        ]

        for text, level, style_name in btns:
            ttk.Button(button_frame, text=text, width=15, style=style_name,
                       command=lambda lvl=level: self.start_quiz(lvl)).pack(side='left', padx=10)

        ttk.Button(self.mode_page, text="⬅ Back to Home", style='TButton',
                   command=lambda: self.show_page(self.start_page)).pack(pady=50)

    def create_quiz_page(self):
        # Setup the main question and input page
        self.quiz_page = ttk.Frame(self.root, padding="25 25")

        # Info Bar for Score and Progress
        info_frame = ttk.Frame(self.quiz_page)
        info_frame.pack(fill='x', pady=10)
        
        self.progress = ttk.Progressbar(info_frame, orient="horizontal", length=300, 
                                        mode="determinate", style="Quiz.Horizontal.TProgressbar")
        self.current_score_label = ttk.Label(info_frame, text="Score: 0", font=('Arial', 12, 'bold'))
        
        self.progress.pack(side='left', padx=15, fill='x', expand=True)
        self.current_score_label.pack(side='right', padx=15)
        
        self.quiz_title = ttk.Label(self.quiz_page, text="Question", style='Info.TLabel', font=('Arial', 16, 'bold'))
        self.quiz_title.pack(pady=(20, 10))
        
        self.quiz_question = ttk.Label(self.quiz_page, text="", style='Question.TLabel')
        self.quiz_question.pack(pady=30)
        
        self.quiz_answer = ttk.Entry(self.quiz_page, font=("Arial", 24), justify="center", width=10)
        self.quiz_answer.pack(pady=20)

        self.quiz_submit = ttk.Button(self.quiz_page, text="Submit Answer (Enter)", style='TButton',
                                      command=self.check_answer)
        self.quiz_submit.pack(pady=30)


    def create_end_page(self):
        # Setup the final results page
        self.end_page = ttk.Frame(self.root, padding="25 50")

        ttk.Label(self.end_page, text="🎉 Challenge Complete! 🎉", style='Header.TLabel').pack(pady=30)

        self.end_score = ttk.Label(self.end_page, text="", font=('Arial', 20, 'bold'), foreground='#263238')
        self.end_score.pack(pady=10)

        self.feedback_label = ttk.Label(self.end_page, text="", font=('Arial', 14), foreground='#555555')
        self.feedback_label.pack(pady=10)

        ttk.Button(self.end_page, text="Try New Mode", style='TButton', width=18,
                   command=lambda: self.show_page(self.mode_page)).pack(pady=25)

        ttk.Button(self.end_page, text="Exit Game", style='TButton', width=18,
                   command=self.root.quit).pack(pady=10)

    # --- Game Logic ---

    def get_number_range(self):
        # Returns number range based on difficulty level
        if self.difficulty == 1:
            return 1, 10
        elif self.difficulty == 2:
            return 10, 100
        else:
            return 20, 1000

    def generate_problem(self):
        low, high = self.get_number_range()

        ops = ['+', '-']
        if self.difficulty >= 2:
            ops.append('*')
        if self.difficulty == 3:
            ops.append('/')

        operation = random.choice(ops)

        if operation == '/':
            # Division: Ensures an integer result by working backward from the answer
            num2 = random.randint(2, low) if low > 2 else 2
            result = random.randint(2, 20)
            num1 = num2 * result
        
        elif operation == '-':
            # Subtraction: Ensures a non-negative result
            num1 = random.randint(low, high)
            num2 = random.randint(low, num1)
            result = num1 - num2
            
        elif operation == '*':
             # Multiplication: Scales factors to keep products reasonable
             factor_limit = high // 5 
             num1 = random.randint(1, factor_limit) if self.difficulty == 1 else random.randint(low, factor_limit)
             num2 = random.randint(1, factor_limit) if self.difficulty == 1 else random.randint(low, factor_limit)
             result = num1 * num2
        
        else:
            # Addition
            num1 = random.randint(low, high)
            num2 = random.randint(low, high)
            result = OPERATIONS[operation](num1, num2)

        return num1, operation, num2, int(round(result))

    def start_quiz(self, level):
        # Reset state and begin the quiz
        self.difficulty = level
        self.score = 0
        self.question_number = 0
        self.second_try = False
        self.progress["value"] = 0
        self.show_page(self.quiz_page)
        self.next_question()

    def next_question(self):
        # Display the next question or end the game
        if self.question_number == self.total_questions:
            self.display_results()
            return

        self.question_number += 1
        self.second_try = False

        num1, operation, num2, self.correct_answer = self.generate_problem()

        self.quiz_title.config(text=f"Question {self.question_number} of {self.total_questions}")
        self.quiz_question.config(text=f"{num1} {operation} {num2} = ?")
        self.quiz_answer.delete(0, tk.END)
        self.quiz_answer.focus_set()

        self.progress["value"] = (self.question_number - 1) * (100 / self.total_questions)
        self.current_score_label.config(text=f"Score: {self.score}")

    def check_answer(self):
        # Validate input and check against the correct answer
        try:
            user_input = self.quiz_answer.get().strip()
            if not user_input:
                messagebox.showwarning("Input Error", "Please enter your answer.")
                return
            user_answer = int(user_input)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid whole number.")
            return

        if user_answer == self.correct_answer:
            points_awarded = 0
            
            # Award points based on first or second try
            if not self.second_try:
                points_awarded = 10
                feedback_msg = "Great job! Full points awarded."
            else:
                points_awarded = 5
                feedback_msg = "Correct on your second attempt! Half points awarded."

            self.score += points_awarded
            messagebox.showinfo("Correct!", f"🎉 Correct! (+{points_awarded} points)\n{feedback_msg}")

            self.next_question()
        else:
            # Handle incorrect attempt logic
            if not self.second_try:
                self.second_try = True
                messagebox.showinfo("Incorrect", "❌ Incorrect! Try again. You can still earn half points.")
                self.quiz_answer.delete(0, tk.END)
                self.quiz_answer.focus_set()
            else:
                messagebox.showerror("Incorrect",
                                     f"❌ Still incorrect!\nThe correct answer was: {self.correct_answer}")
                self.next_question()

    def display_results(self):
        # Calculate final score and display results page
        max_score = self.total_questions * 10
        percentage = (self.score / max_score) * 100

        if percentage >= 90:
            grade = "A+"
            feedback = "Outstanding! You are a Math Wiz!"
        elif percentage >= 75:
            grade = "A"
            feedback = "Excellent! Keep up the great work."
        elif percentage >= 60:
            grade = "B"
            feedback = "Good work, but there's room for improvement. Keep practicing!"
        else:
            grade = "C or lower"
            feedback = "Time to hit the books! Let's try again on an easier mode."

        self.end_score.config(text=f"Final Score: {self.score}/{max_score} ({percentage:.0f}%)")
        self.feedback_label.config(text=f"Grade: {grade}\n\n{feedback}")
        self.show_page(self.end_page)


if __name__ == "__main__":
    # Main application entry point
    root = tk.Tk()
    app = MathQuizApp(root)
    root.mainloop()