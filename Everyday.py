import tkinter as tk
import random
from datetime import date
import os
# ================= DATES =================
START_DATE = date(2023, 11, 23)
today = date.today()
days_together = (today - START_DATE).days

# ================= DAILY MESSAGES =================
daily_messages = [
    "I hope today treats you gently ",
    "No matter what today brings, I'm here for you ",
    "You are loved more than you realize ",
    "Today is better because you exist ",
    "Take today one breath at a time, love ",
    "I believe in you, especially today ",
    "Even on ordinary days, you are special ",
    "You don't have to be perfect to be loved ",
    "Your presence makes everything brighter ",
    "I'm grateful for you every single day ",
    "You're doing better than you think ",
    "Remember:   you are enough, always ",
    "Sending you all my love today ",
    "You make my world so much better ",
    "I'm proud of you for getting through today ",
    "Your smile is my favorite thing ",
    "You deserve all the happiness in the world ",
    "Thank you for being you ",
    "Every day with you is a gift ",
    "You're stronger than you know ",
    "I see you, I hear you, I love you ",
    "You light up my life in every way ",
    "I'm so lucky to have you ",
    "Your heart is beautiful ",
    "You matter so much to me ",
    "I love you more than words can say ",
    "I love you to the moon and back ",
]

daily_message = daily_messages[today.toordinal() % len(daily_messages)]

# ================= DAY / NIGHT MESSAGES =================
morning_messages = [
    "Good morning, my baby!   I hope today is kind to you ",
    "Rise and shine, beautiful! Today is your day ",
    "Good morning!  You're the first thing on my mind ",
    "Wake up, sunshine! The world needs your light ",
    "Morning, love! I believe in you today and always ",
    "Good morning!   Remember, you're amazing ",
    "Hey there!   Sending you morning hugs ",
    "Good morning!  May your day be as sweet as you ",
    "Morning, my heart! You've got this ",
    "Good morning! Start your day knowing you're loved ",
    "Wake up, love! A new day of possibilities awaits ",
    "Good morning!   I'm here with you, always ",
    "Morning!   Your smile is my favorite sunrise ",
    "Good morning! Take it easy on yourself today ",
    "Hey love!  Today will be wonderful because you're in it "
]

night_messages = [
    "Good night, my darlingg.   Rest well.   I'm so proud of you ",
    "Sweet dreams, beautiful.  You deserve peaceful sleep ",
    "Good night!   Tomorrow is a fresh start ",
    "Sleep tight, love. I'll be here when you wake ",
    "Good night!  You did your best today, and that's enough ",
    "Rest well, my heart. Let go of today's worries ",
    "Good night!  May your dreams be as sweet as you are ",
    "Sleep peacefully.   You are safe and loved ",
    "Good night, love!   Recharge for tomorrow ",
    "Sweet dreams!   I'm proud of everything you did today ",
    "Good night!   Let the stars watch over you tonight ",
    "Rest now, you've earned it.  Sleep well ",
    "Good night! Close your eyes and feel my love ",
    "Sleep tight!   Tomorrow is another chance to shine ",
    "Good night, my everything.   Dream of me"
]

# Pick one at random each time
morning_message = random.choice(morning_messages)
night_message = random.choice(night_messages)

# ================= MOOD MESSAGES =================
mood_messages = {
    "Happy 😊": [
        "Seeing you happy makes my whole world brighter ",
        "Your happiness is contagious!   Keep shining ",
        "I love seeing you smile like this ",
        "Your joy fills my heart with warmth ",
        "This is the energy I love to see from you!  ",
        "Keep that beautiful smile going, baby!   ",
        "Your happiness is my favorite sight ",
        "I'm so glad to see you feeling good today!   ",
        "Your smile is my favorite sight in the world",
        "Happiness looks so good on you!  ",
        "Your joy lights up my life like nothing else ",
        "Keep shining, love! Your happiness is beautiful ",
        "Seeing you happy makes me the happiest person alive "
    ],
    "Sad 😔": [
        "It's okay to feel sad.   I'll sit with you through it ",
        "Your tears are valid.  Let them flow, I'm here ",
        "Sadness is just love with nowhere to go.   I'm here for you ",
        "You don't have to be strong right now.  Just be ",
        "I'm holding space for your sadness. You're not alone"
        "Aww, my love. I'm here for you.",
        "It's okay to feel down sometimes.  I'm here",
        "Go ahead and let it out, baby. I'm right here for you ",
        "I'm sending you all my love and hugs right now ",
        "Remember, it's okay to not be okay sometimes "
    ],
    "Stressed 😤": [
        "Pause.  Breathe. You're doing your best ",
        "One thing at a time, love. You've got this",
        "Stress means you care. But remember to care for yourself too",
        "Take a deep breath.  Everything will work out ",
        "You're handling so much.   I'm proud of you",
        "Maybe you should take a little break?   You deserve it",
        "Take it easy on yourself, baby.  You're amazing just as you are "
    ],
    "Miss You 💭": [
        "I miss you too, always and in every way",
        "The distance doesn't change how much I love you",
        "Missing you is a reminder of how much you mean to me",
        "I feel you in my heart even when we're apart ",
        "Can't wait until we're together again soon ",
        "Every moment without you makes me cherish you more",
        "You're always on my mind, no matter the miles between us",
        "Counting down the days until I see you again ",
        "Your absence makes the heart grow fonder ",
        "No matter the distance, you're always with me ",
        "I carry you in my heart wherever I go and I hope you feel the same"
    ],
    "Tired 😴": [
        "Rest, my love. You deserve peace ",
        "Being tired means you've been working hard.   Time to rest na ha",
        "Your body needs care.  Please rest, baby",
        "It's okay to pause.   Recharge your energy baby",
        "Tired is valid. Be gentle with yourself tonight or today",
        "I'm here to help you relax.",
        "Let me take care of you, my baby : (",
        "You deserve all the rest in the world"
    ],
    "Anxious 😰": [
        "Anxiety lies. You are safe and you are loved",
        "Breathe with me.  In...   and out.  You're okay ",
        "This feeling will pass.   I'm here while it does ",
        "Your anxiety doesn't define you.  You're so much more ",
        "One moment at a time.   You're doing great",
        "I'm right here with you, always."
        "Everything will be okay, my love"
    ],
    "Excited 🎉": [
        "Your excitement is adorable! Tell me everything!  ",
        "I love seeing you this energized!  ",
        "Your enthusiasm is so cute!   So proud of you! ",
        "Yes baby!  ",
        "Your joy makes my day!  Keep shining!"
        "Good news?   Tell me all about it!"
    ],
    "Lonely 💔": [
        "You're never truly alone.  I'm always with you ",
        "I see you, I hear you, and you matter ",
        "Loneliness is temporary.   You are deeply loved ",
        "Even from afar, you're in my heart always ",
        "I wish I could hug you right now.   Sending virtual hugs 🤗",
        "Even when you can't see me, I am with you"
    ]
}

# ================= MONTHLY 23RD MESSAGES =================
monthly_23rd_messages = {
    1: {  # January
        "title": "NEW YEAR, SAME LOVE",
        "message":  (
            "Happy New Year, my baby!\n\n"
            "As we start another year together,\n"
            "I want you to know that my love for you\n"
            "only grows stronger with time.\n\n"
            "Here's to another year of loving you,\n"
            "supporting you, and being by your side.\n\n"
            "Every January 23rd reminds me that\n"
            "the best decision I ever made was choosing you.\n\n"
            "To new beginnings and forever with you, my Bianca"
        )
    },
    2: {  # February
        "title":  "HAPPY VALENTINE'S AND MOTMOT",
        "message": (
            "Happy Monthsarry, baby!\n\n"
            "February is for lovers, and you are mine.\n"
            "Every beat of my heart spells your name.\n\n"
            "They say love is in the air this month,\n"
            "but for me, love is wherever you are.\n\n"
            "Thank you for being my Valentine every single day,\n"
            "not just in February, but all year round.\n\n"
            "You are my greatest love and my forever Valentine"
        )
    },
    3: {  # March
        "title": "MARCHing WITH YOU",
        "message": (
            "Happy monthsarry, my darling!\n\n"
            "Every day with you brings new reasons to smile.\n\n"
            "You make my world colorful and bright,\n"
            "like flowers blooming after winter.\n\n"
            "Thank you for being the warmth\n"
            "that melts away all my worries.\n\n"
            "Growing and blossoming with you forever"
        )
    },
    4: {  # April
        "title": "Birthmonth naken",
        "message": (
            "Happy Monthsarry, my love!\n\n"
            "Naa koy nabasahan nga April showers bring May flowers,\n"
            "but your love brings joy all year long.\n\n"
            "Even on rainy days, you are my sunshine.\n"
            "Even in storms, you are my shelter.\n\n"
            "Thank you for weathering every day with me,\n"
            "and for making every day feel sunny.\n\n"
        )
    },
    5: {  # May
        "title": "MAY YOUR DAYS BE BRIGHT",
        "message": (
            "Happy May 23rd, gwapa!\n\n"
            "May flowers are in bloom, just like my love for you.\n"
            "Every petal reminds me of a reason I adore you.\n\n"
            "You bring beauty and joy into my life\n"
            "in ways I never thought possible.\n\n"
            "Thank you for being the brightest part of my days,\n"
            "and the sweetest part of my dreams.\n\n"
            "Forever blooming ka"
        )
    },
    6: {  # June
        "title": "The month nga ni confess ka",
        "message": (
            "Happy Monthsarry, my babyy!\n\n"
            "This was the month you confessed to me.\n"
            "You make every day feel like a perfect day.\n\n"
            "Warm, bright, and full of endless possibilities.\n"
            "That's what life with you feels like.\n\n"
            "Thank you for being my light,\n"
            "my warmth, and my everything.\n\n"
            "Basking in your love forever"
        )
    },
    7: {  # July
        "title":  "MONTHSARRYYY",
        "message": (
            "Happy 23rd of the day this month, my Bianca!\n\n"
            "You light up my life in the most magical ways,\n"
            "and every moment with you is a celebration.\n\n"
            "Thank you for making my world sparkle\n"
            "with your love and laughter.\n\n"
            "Celebrating you today and always"
        )
    },
    8: {  # August
        "title": "August with You",
        "message": (
            "Happy August 23rd, my darling!\n\n"
            "As the month continues, so does my love for you—\n"
            "endless, warm, and full of light.\n\n"
            "You are my favorite season,\n"
            "my favorite moment, my favorite everything.\n\n"
            "Thank you for making every day feel like\n"
            "the best day of my life.\n\n"
            "Here's to more months with you"
        )
    },
    9: {  # September
        "title": "September Monthsarry",
        "message": (
            "Happy September 23rd, baby!\n\n"
            "As the classes continue,\n"
            "so does my love for you grow stronger.\n\n"
            "I keep thinking about you,\n"
            "I keep missing you each moment.\n\n"
            "Every day, I fall a little deeper,\n"
            "love you a little more, cherish you a little longer.\n\n"
            "Forever falling for you"
        )
    },
    10: {  # October
        "title": "Another Month with You",
        "message": (
            "Happy October 23rd, my bae! Hapit na Halloween soo\n\n"
            "I'm under your spell, and I never want to break free.\n"
            "You've bewitched me, body and soul.\n\n"
            "Every day with you is a treat (no tricks bisag LDR),\n"
            "and I'm so grateful for your magic in my life.\n\n"
            "You're not scary, you're the sweetest thing ever.\n\n"
            "I'm gonna haunt your heart forever"
        )
    },
    11: {  # November
        "title": "THANKFUL FOR YOU",
        "message": (
            "Happy November 23rd, my everything!\n\n"
            "Today is extra special—it's our anniversary!  🎉\n"
            "November 23, 2023, the day we became us.\n\n"
            "I am endlessly thankful for you,\n"
            "for your love, your patience, your beautiful heart.\n\n"
            "You are my greatest blessing,\n"
            "and I thank the universe every day for you.\n\n"
            "Here's to many more years together!\n"
            "I love you more than words can say "
        )
    },
    12: {  # December
        "title": "My CHRISTMAS MIRACLE",
        "message": (
            "Happy December 23rd, my Christmas miracle!\n\n"
            "As the year comes to an end,\n"
            "I reflect on all the beautiful moments we've shared.\n\n"
            "You are the greatest gift I've ever received,\n"
            "wrapped in love, tied with forever.\n\n"
            "Thank you for making this year magical,\n"
            "and for being my home during the holidays.\n\n"
            "Here's to ending this year with you,\n"
            "and starting the next one the same way 🎁❄️"
        )
    }
}

clicked_moods = set()
all_moods = set(mood_messages.keys())

# ================= HIGH SCORE =================
HIGHSCORE_FILE = "highscore.txt"

if os.path.exists(HIGHSCORE_FILE):
    with open(HIGHSCORE_FILE, "r") as f:
        try:
            high_score = int(f.read())
        except: 
            high_score = 0
else:
    high_score = 0

# ================= FUNCTIONS =================
def show_message(mood):
    clicked_moods.add(mood)
    # Pick a random message from the list for that mood
    message_label.config(text=random.choice(mood_messages[mood]))

    if clicked_moods == all_moods:
        # Check if today is the 23rd
        if today.day == 23:
            unlock_special_23rd_message()
        else:
            unlock_secret()

def unlock_secret():
    secret_label.config(
        text=(
            "🎁 Secret unlocked 💖\n\n"
            "Every day with you is my favorite.\n"
            "I'd choose you in every lifetime no matter what your mood is."
        ),
        fg="#b30059"
    )

def unlock_special_23rd_message():
    """Special message that only unlocks on the 23rd of any month"""
    current_month = today.month
    months_together = ((today.year - START_DATE.year) * 12 + 
                       (today.month - START_DATE.month))
    
    # Get the message for the current month
    month_data = monthly_23rd_messages[current_month]
    
    secret_label.config(
        text=(
            f"✨ {month_data['title']} ✨\n\n"
            f"📅 Month {months_together} Together 📅\n\n"
            f"{month_data['message']}"
        ),
        fg="#b30059",
        font=("Helvetica", 10, "bold")
    )

def show_morning():
    # Pick a random morning message each time
    daynight_label.config(text=random.choice(morning_messages))

def show_night():
    # Pick a random night message each time
    daynight_label.config(text=random.choice(night_messages))

# ================= GUI SETUP =================
window = tk.Tk()
window.title("For You 💕")
window.geometry("500x700")
window.resizable(True, True)
window.configure(bg="#fff0f5")

# Create main canvas with scrollbar
main_canvas = tk.Canvas(window, bg="#fff0f5", highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas, bg="#fff0f5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
)

main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

main_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Bind mousewheel for scrolling
def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Background canvas for hearts (taller to fit all content)
canvas = tk.Canvas(scrollable_frame, width=500, height=1000, bg="#fff0f5", highlightthickness=0)
canvas.pack()

frame = tk.Frame(canvas, bg="#fff0f5")
frame.place(relx=0.5, rely=0.02, anchor="n")

# ================= HEART ANIMATION =================
hearts = []

def create_heart():
    x = random.randint(20, 460)
    y = 980
    heart = canvas.create_text(x, y, text="💖", font=("Arial", 18))
    hearts.append(heart)

def animate_hearts():
    if random.random() < 0.25:
        create_heart()

    for heart in hearts[: ]:
        canvas.move(heart, 0, -2)
        coords = canvas.coords(heart)
        if coords and coords[1] < -20:
            canvas.delete(heart)
            hearts.remove(heart)

    window.after(50, animate_hearts)

# ================= TITLE =================
tk.Label(
    frame,
    text="How Are You Feeling Today?  💖",
    font=("Helvetica", 16, "bold"),
    bg="#fff0f5",
    fg="#b30059"
).pack(pady=5)

# ================= DAYS TOGETHER =================
days_label = tk.Label(
    frame,
    text=f"💞 {days_together} days together since Nov 23, 2023",
    font=("Helvetica", 11, "bold"),
    bg="#fff0f5",
    fg="#800040"
)
days_label.pack(pady=5)

# Add special indicator if today is the 23rd
if today.day == 23:
    tk.Label(
        frame,
        text="✨ Today is our special day! ✨",
        font=("Helvetica", 10, "bold"),
        bg="#ffb3d9",
        fg="#b30059",
        padx=10,
        pady=5
    ).pack(pady=5)

# ================= DAILY MESSAGE =================
tk.Label(
    frame,
    text=f"Today's message:\n{daily_message}",
    font=("Helvetica", 11),
    wraplength=420,
    justify="center",
    bg="white",
    fg="#4d004d",
    padx=15,
    pady=15
).pack(pady=8)

# ================= GOOD MORNING / NIGHT =================
daynight_label = tk.Label(
    frame,
    text="Tap below for a message 💗",
    font=("Helvetica", 11, "italic"),
    wraplength=400,
    justify="center",
    bg="#fff0f5",
    fg="#4d004d"
)
daynight_label.pack(pady=6)

switch_frame = tk.Frame(frame, bg="#fff0f5")
switch_frame.pack(pady=4)

tk.Button(
    switch_frame,
    text="☀️ Good Morning",
    font=("Helvetica", 10, "bold"),
    bg="#ffb3d9",
    fg="#4d004d",
    width=16,
    command=show_morning
).pack(side="left", padx=5)

tk.Button(
    switch_frame,
    text="🌙 Good Night",
    font=("Helvetica", 10, "bold"),
    bg="#d9b3ff",
    fg="#4d004d",
    width=16,
    command=show_night
).pack(side="right", padx=5)

# ================= MOOD DISPLAY =================
message_label = tk.Label(
    frame,
    text="Choose a mood and I'll be right here 🤍",
    font=("Helvetica", 12),
    wraplength=420,
    justify="center",
    bg="white",
    fg="#4d004d",
    padx=20,
    pady=15
)
message_label.pack(pady=10)

# ================= MOOD BUTTONS =================
for mood in mood_messages: 
    tk.Button(
        frame,
        text=mood,
        font=("Helvetica", 11, "bold"),
        width=26,
        bg="#ff80bf",
        fg="white",
        activebackground="#ff4da6",
        command=lambda m=mood: show_message(m)
    ).pack(pady=4)

# ================= SECRET MESSAGE =================
secret_label = tk.Label(
    frame,
    text="",
    font=("Helvetica", 11, "bold"),
    wraplength=440,
    justify="center",
    bg="#fff0f5"
)
secret_label.pack(pady=15)

# ================= MINI-GAME =================
def open_game():
    game = tk.Toplevel()
    game.title("Murag Flappy Bird but.. ...")
    game.geometry("400x500")
    game.resizable(False, False)

    game_canvas = tk.Canvas(game, width=400, height=450, bg="#e6f7ff")
    game_canvas.pack()

    score = 0
    velocity = 0
    pipes = []
    game_running = True

    player = game_canvas.create_text(80, 225, text="💗", font=("Arial", 28))

    score_text = game_canvas.create_text(
        200, 30,
        text=f"Score:   0  |  High:   {high_score}",
        font=("Arial", 12, "bold")
    )

    def flap(event=None):
        nonlocal velocity
        if game_running:
            velocity = -5  # Gentler flap

    def create_pipe():
        gap_y = random.randint(130, 300)
        gap_size = 200  # MUCH bigger gap
        top = game_canvas.create_rectangle(400, 0, 450, gap_y - gap_size//2, fill="#ff80bf", outline="#ff4da6", width=2)
        bottom = game_canvas.create_rectangle(400, gap_y + gap_size//2, 450, 450, fill="#ff80bf", outline="#ff4da6", width=2)
        pipes.append((top, bottom, False))

    def hit_pipe():
        coords = game_canvas.bbox(player)
        if not coords:
            return False
        px1, py1, px2, py2 = coords
        
        for top, bottom, _ in pipes:
            top_coords = game_canvas.bbox(top)
            bottom_coords = game_canvas.bbox(bottom)
            
            if not top_coords or not bottom_coords: 
                continue
                
            tx1, ty1, tx2, ty2 = top_coords
            bx1, by1, bx2, by2 = bottom_coords
            
            # Check overlap with top pipe
            if (px1 < tx2 and px2 > tx1 and py1 < ty2 and py2 > ty1):
                return True
            # Check overlap with bottom pipe
            if (px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1):
                return True
        return False

    def move():
        nonlocal velocity, score, game_running
        global high_score

        if not game_running: 
            return

        # Much gentler gravity
        velocity += 0.25
        game_canvas.move(player, 0, velocity)

        # Move pipes slower
        for i, pipe in enumerate(pipes[: ]):
            top, bottom, scored = pipe
            game_canvas.move(top, -3, 0)
            game_canvas.move(bottom, -3, 0)

            # Check if pipe passed the player and hasn't been scored yet
            if not scored and game_canvas.coords(top)[2] < 80:
                pipes[pipes.index(pipe)] = (top, bottom, True)
                score += 1
                game_canvas.itemconfig(
                    score_text,
                    text=f"Score:  {score}  |  High:  {high_score}"
                )

            # Remove pipes that are off screen
            if game_canvas.coords(top)[2] < 0:
                game_canvas.delete(top)
                game_canvas.delete(bottom)
                pipes.remove(pipe)

        coords = game_canvas.coords(player)
        if not coords:
            return

        y = coords[1]

        # Check collision
        if y < 15 or y > 435 or hit_pipe():
            end_game()
            return

        # Spawn pipes MUCH less frequently
        if random.random() < 0.012:
            create_pipe()

        game. after(30, move)

    def end_game():
        nonlocal game_running
        global high_score
        game_running = False

        if score > high_score:
            high_score = score
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(high_score))

        game_canvas.create_rectangle(50, 180, 350, 320, fill="white", outline="#ff66a3", width=2)

        game_canvas.create_text(
            200, 250,
            text=f"Game Over 💔\nScore: {score}\nHigh Score: {high_score}\n\nTry again baby!",
            font=("Helvetica", 12, "bold"),
            fill="#b30059",
            justify="center"
        )

        tk.Button(
            game,
            text="🔁 Play Again",
            font=("Helvetica", 11, "bold"),
            bg="#ff66a3",
            fg="white",
            command=lambda: restart_game(game)
        ).pack(pady=10)

    def restart_game(old_game):
        old_game.destroy()
        open_game()

    # Instructions
    game_canvas.create_text(
        200, 425,
        text="Press SPACE or CLICK! ",
        font=("Arial", 10),
        fill="#4d004d"
    )

    game.bind("<space>", flap)
    game.bind("<Button-1>", flap)

    move()

# ================= BUTTON =================
tk.Button(
    frame,
    text="🎮 Play when you're bored",
    font=("Helvetica", 12, "bold"),
    bg="#ff66a3",
    fg="white",
    padx=20,
    pady=10,
    command=lambda: open_game()
).pack(pady=10)

# ================= FOOTER =================
tk.Label(
    frame,
    text="Made with love, just for you 💗",
    font=("Helvetica", 9),
    bg="#fff0f5",
    fg="#800040"
).pack(pady=5)

tk.Label(
    frame,
    text="Even when you're bored,\nI'm here with you 💗",
    font=("Helvetica", 10),
    bg="#fff0f5",
    fg="#800040"
).pack(pady=10)

# ================= START ANIMATION =================
animate_hearts()

window.mainloop()