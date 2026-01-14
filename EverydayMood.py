import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
from datetime import date, datetime
import calendar as cal
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================= COLOR AND FONT CONSTANTS =================
COLORS = {
    'bg_main': '#fff0f5',
    'bg_light': '#ffe6f0',
    'primary': '#ff66a3',
    'secondary': '#9966ff',
    'accent': '#b30059',
    'text_dark': '#4d004d',
    'text_light': '#800040',
    'success': '#66cc66',
    'white': '#ffffff',
    'pink_light': '#ffb3d9',
    'purple_light': '#d9b3ff'
}

FONTS = {
    'title': ('Helvetica', 16, 'bold'),
    'heading': ('Helvetica', 14, 'bold'),
    'body': ('Helvetica', 11),
    'small': ('Helvetica', 9),
    'button': ('Helvetica', 11, 'bold')
}

# ================= FILE PATHS =================
HIGHSCORE_FILE = "highscore.txt"
ACHIEVEMENTS_FILE = "achievements.json"
JOURNAL_FILE = "journal_entries.json"
SETTINGS_FILE = "settings.json"
EMAIL_CONFIG_FILE = "email_config.json"
ERROR_LOG_FILE = "error_log.txt"

# ================= EMAIL NOTIFIER CLASS =================
class EmailNotifier:
    """Handles email notifications for journal entries"""
    
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load email configuration from file"""
        try:
            if os.path.exists(EMAIL_CONFIG_FILE):
                with open(EMAIL_CONFIG_FILE, 'r') as f:
                    return json.load(f)
            else:
                # Create default config from template
                default_config = {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "sender_email": "",
                    "sender_password": "",
                    "recipient_email": "",
                    "notifications_enabled": False
                }
                with open(EMAIL_CONFIG_FILE, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            self.log_error(f"Error loading email config: {str(e)}")
            return None
    
    def save_config(self, config):
        """Save email configuration to file"""
        try:
            with open(EMAIL_CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.config = config
            return True
        except Exception as e:
            self.log_error(f"Error saving email config: {str(e)}")
            return False
    
    def send_journal_notification(self, entry_data):
        """
        Send email notification when new journal entry is created
        Returns: (success: bool, error_message: str)
        """
        if not self.config or not self.config.get('notifications_enabled', False):
            return (False, "Notifications disabled")
        
        # Validate configuration
        if not self.config.get('sender_email') or not self.config.get('sender_password'):
            return (False, "Email not configured. Please check Settings tab.")
        
        if not self.config.get('recipient_email'):
            return (False, "Recipient email not set")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['sender_email']
            msg['To'] = self.config['recipient_email']
            
            # Create subject with mood emoji
            mood_text = entry_data.get('mood', 'Unknown')
            date_str = entry_data.get('date', datetime.now().strftime('%Y-%m-%d'))
            msg['Subject'] = f"💕 New Journal Entry from Bianca - {mood_text} - {date_str}"
            
            # Create body
            body = f"""
Hello! 💖

Bianca just wrote a new journal entry:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: {entry_data.get('date', 'Unknown')}
Time: {entry_data.get('timestamp', 'Unknown')}
Mood: {entry_data.get('mood', 'Unknown')}
Days Together: {entry_data.get('days_together', 'N/A')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{entry_data.get('entry', '')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Keep being there for her, she loves you so much! 💗

With love,
Your EverydayMood App 💕
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server and send
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['sender_email'], self.config['sender_password'])
            server.send_message(msg)
            server.quit()
            
            return (True, "Email sent successfully!")
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "Authentication failed. Please check your email and password."
            self.log_error(error_msg)
            return (False, error_msg)
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error: {str(e)}"
            self.log_error(error_msg)
            return (False, error_msg)
        except Exception as e:
            error_msg = f"Error sending email: {str(e)}"
            self.log_error(error_msg)
            return (False, error_msg)
    
    def log_error(self, message):
        """Log errors to file"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(ERROR_LOG_FILE, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except:
            pass  # Silently fail if can't write to log


# ================= JOURNAL MANAGER CLASS =================
class JournalManager:
    """Manages journal entries and statistics"""
    
    def __init__(self):
        self.entries = self.load_entries()
        self.email_notifier = EmailNotifier()
    
    def load_entries(self):
        """Load journal entries from file"""
        try:
            if os.path.exists(JOURNAL_FILE):
                with open(JOURNAL_FILE, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            self.log_error(f"Error loading journal entries: {str(e)}")
            return []
    
    def save_entries(self):
        """Save journal entries to file"""
        try:
            with open(JOURNAL_FILE, 'w') as f:
                json.dump(self.entries, f, indent=4)
            return True
        except Exception as e:
            self.log_error(f"Error saving journal entries: {str(e)}")
            return False
    
    def add_entry(self, mood, entry_text, days_together):
        """Add a new journal entry"""
        now = datetime.now()
        new_entry = {
            "id": len(self.entries) + 1,
            "timestamp": now.strftime('%Y-%m-%d %H:%M:%S'),
            "date": now.strftime('%Y-%m-%d'),
            "mood": mood,
            "entry": entry_text,
            "email_sent": False,
            "days_together": days_together
        }
        
        self.entries.append(new_entry)
        
        # Try to send email
        success, message = self.email_notifier.send_journal_notification(new_entry)
        new_entry['email_sent'] = success
        
        # Save regardless of email status
        self.save_entries()
        
        return (True, message, success)
    
    def get_entries(self, mood_filter=None, search_term=None):
        """Get filtered journal entries"""
        filtered = self.entries
        
        if mood_filter and mood_filter != "All Moods":
            filtered = [e for e in filtered if e.get('mood') == mood_filter]
        
        if search_term:
            search_lower = search_term.lower()
            filtered = [e for e in filtered if search_lower in e.get('entry', '').lower()]
        
        return sorted(filtered, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def get_statistics(self):
        """Calculate journal statistics"""
        if not self.entries:
            return {
                'total_entries': 0,
                'writing_streak': 0,
                'most_common_mood': 'N/A',
                'first_entry_date': 'N/A'
            }
        
        # Count moods
        mood_counts = {}
        for entry in self.entries:
            mood = entry.get('mood', 'Unknown')
            mood_counts[mood] = mood_counts.get(mood, 0) + 1
        
        most_common_mood = max(mood_counts.items(), key=lambda x: x[1])[0] if mood_counts else 'N/A'
        
        # Calculate streak (consecutive days)
        dates = sorted(set(e.get('date', '') for e in self.entries), reverse=True)
        streak = 0
        if dates:
            today = datetime.now().strftime('%Y-%m-%d')
            current_date = datetime.strptime(dates[0], '%Y-%m-%d')
            
            for date_str in dates:
                entry_date = datetime.strptime(date_str, '%Y-%m-%d')
                if (current_date - entry_date).days <= 1:
                    streak += 1
                    current_date = entry_date
                else:
                    break
        
        return {
            'total_entries': len(self.entries),
            'writing_streak': streak,
            'most_common_mood': most_common_mood,
            'first_entry_date': self.entries[0].get('date', 'N/A') if self.entries else 'N/A'
        }
    
    def log_error(self, message):
        """Log errors to file"""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(ERROR_LOG_FILE, 'a') as f:
                f.write(f"[{timestamp}] {message}\n")
        except:
            pass


# ================= SETTINGS MANAGER =================
class SettingsManager:
    """Manages application settings"""
    
    def __init__(self):
        self.settings = self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        default_settings = {
            'theme': 'light',
            'font_size': 'medium',
            'animations_enabled': True,
            'accent_color': COLORS['primary']
        }
        
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
        except:
            pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            with open(SETTINGS_FILE, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except:
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()




# ================= DATA STRUCTURES =================
START_DATE = date(2023, 11, 23)


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
        "Remember:       you are enough, always ",
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


morning_messages = [
        "Good morning, my baby!       I hope today is kind to you ",
        "Rise and shine, beautiful! Today is your day ",
        "Good morning!      You're the first thing on my mind ",
        "Wake up, sunshine! The world needs your light ",
        "Morning, love!    I believe in you today and always ",
        "Good morning!       Remember, you're amazing ",
        "Hi there!       Sending you morning hugs ",
        "Good morning!  May your day be as sweet as you ",
        "Morning, my heart!  You've got this ",
        "Good morning!   Start your day knowing you're loved ",
        "Wake up, love!  A new day of possibilities awaits ",
        "Good morning!       I'm here with you, always ",
        "Morning!       Your smile is my favorite sunrise ",
        "Good morning!  Take it easy on yourself today ",
        "Hey baby!  Today will be wonderful because you're in it "
    ]


night_messages = [
        "Good night, my darlingg.       Rest well.       I'm so proud of you ",
        "Sweet dreams, beautiful.    You deserve peaceful sleep ",
        "Good night!     Tomorrow is a fresh start ",
        "Sleep tight, love.     I'll be here when you wake ",
        "Good night!  You did your best today, and that's enough ",
        "Rest well, my heart.  Let go of today's worries ",
        "Good night!  May your dreams be as sweet as you are ",
        "Sleep peacefully.       You are safe and loved ",
        "Good night, love!   Recharge for tomorrow ",
        "Sweet dreams!       I'm proud of everything you did today ",
        "Good night!       Let the stars watch over you tonight ",
        "Rest now, you've earned it.    Sleep well ",
        "Good night!  Close your eyes and feel my love ",
        "Sleep tight!       Tomorrow is another chance to shine ",
        "Good night, my dearest baby.     Dream of me.",
        "Good night!  I love you more than the stars in the sky "
    ]


mood_messages = {
        "Happy 😊": [
            "Seeing you happy makes my whole world brighter ",
            "Your happiness is contagious!       Keep shining ",
            "I love seeing you smile like this ",
            "Your joy fills my heart with warmth ",
            "This is the energy I love to see from you!      ",
            "Keep that beautiful smile going, baby!       ",
            "Your happiness is my favorite sight ",
            "I'm so glad to see you feeling good today!       ",
            "Your smile is my favorite sight in the world",
            "Happiness looks so good on you!    ",
            "Your joy lights up my life like nothing else ",
            "Keep shining, love!  Your happiness is beautiful ",
            "Seeing you happy makes me the happiest person alive "
        ],
        "Sad 😔": [
            "It's okay to feel sad.       I'll sit with you through it ",
            "Your tears are valid.     Let them flow, I'm here ",
            "Sadness is just love with nowhere to go.       I'm here for you ",
            "You don't have to be strong right now.  Just be ",
            "I'm holding space for your sadness.  You're not alone",
            "Aww, my love.   I'm here for you.",
            "It's okay to feel down sometimes.  I'm here",
            "Go ahead and let it out, baby.  I'm right here for you ",
            "I'm sending you all my love and hugs right now ",
            "Remember, it's okay to not be okay sometimes "
        ],
        "Stressed 😤": [
            "Pause.      Breathe.  You're doing your best ",
            "One thing at a time, love.  You've got this",
            "Stress means you care.  But remember to care for yourself too",
            "Take a deep breath.     Everything will work out ",
            "You're handling so much.       I'm proud of you",
            "Maybe you should take a little break?       You deserve it",
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
            "Rest, my love.  You deserve peace ",
            "Being tired means you've been working hard.       Time to rest na ha",
            "Your body needs care.   Please rest, baby",
            "It's okay to pause.     Recharge your energy baby",
            "Tired is valid.  Be gentle with yourself tonight or today",
            "I'm here to help you relax.",
            "Let me take care of you, my baby :     (",
            "You deserve all the rest in the world"
        ],
        "Anxious 😰": [
            "Anxiety lies.  You are safe and you are loved",
            "Breathe with me.      In...       and out.      You're okay ",
            "This feeling will pass.   I'm here while it does ",
            "Your anxiety doesn't define you.  You're so much more ",
            "One moment at a time.    You're doing great",
            "I'm right here with you, always.",
            "Everything will be okay, my love"
        ],
        "Excited 🎉": [
            "Your excitement is adorable!  Tell me everything!      ",
            "I love seeing you this energized!  ",
            "Your enthusiasm is so cute!   So proud of you!     ",
            "Yes baby!      ",
            "Your joy makes my day!   Keep shining!",
            "Good news?       Tell me all about it!"
        ],
        "Lonely 💔": [
            "You're never truly alone.  I'm always with you ",
            "I see you, I hear you, and you matter ",
            "Loneliness is temporary.     You are deeply loved ",
            "Even from afar, you're in my heart always ",
            "I wish I could hug you right now.       Sending virtual hugs 🤗",
            "Even when you can't see me, I am with you"
        ]
    }


monthly_23rd_messages = {
        1: {  # January
            "title": "NEW YEAR, SAME LOVE",
            "message":      (
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
            "title":      "HAPPY VALENTINE'S AND MOTMOT",
            "message":   (
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
            "title":  "MARCHing WITH YOU",
            "message":    (
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
            "title":  "Birthmonth naken",
            "message":  (
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
            "title":  "MAY YOUR DAYS BE BRIGHT",
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
            "title":      "MONTHSARRYYY",
            "message":  (
                "Happy 23rd of the day this month, my Bianca!\n\n"
                "You light up my life in the most magical ways,\n"
                "and every moment with you is a celebration.\n\n"
                "Thank you for making my world sparkle\n"
                "with your love and laughter.\n\n"
                "Celebrating you today and always"
            )
        },
        8: {  # August
            "title":  "August with You",
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
            "title":  "September Monthsarry",
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
                "Happy October 23rd, my bae!     Hapit na Halloween soo\n\n"
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
            "message":    (
                "Happy November 23rd, my everything!\n\n"
                "Today is extra special—it's our anniversary!      🎉\n"
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
                "and starting the next one the same way"
            )
        }
    }


achievements = {
        1: {
            "title": "First Flight!    ",
            "message": (
                "You got your first point!\n\n"
                "Just like how we started—\n"
                "one small step that led to something beautiful.\n\n"
                "I'm proud of you, baby!    Keep going!   "
            ),
            "emoji": "🎈"
        },
        5: {
            "title": "Rising Star!   ",
            "message": (
                "5 points!     You're getting good at this!\n\n"
                "Just like how you've gotten better\n"
                "at stealing my heart every single day.\n\n"
                "You're doing amazing, my love!  Keep it up!    "
            ),
            "emoji": "✨"
        },
        10: {
            "title": "Perfect Ten!  ",
            "message": (
                "10 points!  You're a natural!\n\n"
                "You know what else is a perfect 10?\n"
                "You.     Every single day.\n\n"
                "I'm so lucky to have you!    hehe"
            ),
            "emoji":    "🌟"
        },
        15: {
            "title": "CHAMPION OF MY HEART!  ",
            "message": (
                "15 POINTS!  You're incredible!\n\n"
                "You've mastered this game,\n"
                "just like you've mastered making me\n"
                "fall in love with you over and over.\n\n"
                "You are my champion, my everything,\n"
                "my greatest achievement in life.\n\n"
                "I love you more than all the high scores\n"
                "in the world combined!"
            ),
            "emoji":  "🏆"
        }
    }


# ================= PASSWORD PROTECTION =================
def check_password():
    """Check if the entered password is correct"""
    entered = password_entry.get()
    if entered == "112323":  
        login_window.destroy()
        open_main_app()
    else:
        error_label.config(text=" Wrong password!    Try again, baby :  )")
        password_entry.delete(0, tk.END)

def on_enter_key(event):
    """Allow Enter key to submit password"""
    check_password()

# Create login window
login_window = tk.  Tk()
login_window.title("For Bianca Nichole B.  Oxcello ")
login_window.geometry("450x350")
login_window.resizable(False, False)
login_window.configure(bg="#fff0f5")

# Center the window
login_window.eval('tk::PlaceWindow .   center')

# Login content
tk.Label(
    login_window,
    text="💖",
    font=("Arial", 48),
    bg="#fff0f5"
).pack(pady=20)

tk.Label(
    login_window,
    text="Enter Password",
    font=("Helvetica", 16, "bold"),
    bg="#fff0f5",
    fg="#b30059"
).pack(pady=5)

tk.Label(
    login_window,
    text="(Hint: Our special date! )",
    font=("Helvetica", 9, "italic"),
    bg="#fff0f5",
    fg="#800040"
).pack(pady=2)

# Password entry
password_entry = tk.Entry(
    login_window,
    font=("Helvetica", 20),
    justify="center",
    width=12,
    show="•"  # Hides the password with dots
)
password_entry.pack(pady=15)
password_entry.focus()

# Error label
error_label = tk.  Label(
    login_window,
    text="",
    font=("Helvetica", 10),
    bg="#fff0f5",
    fg="#cc0000"
)
error_label.pack(pady=5)

# Submit button - BIGGER AND EASIER TO CLICK
submit_button = tk.Button(
    login_window,
    text=" Enter ",
    font=("Helvetica", 14, "bold"),
    bg="#ff66a3",
    fg="white",
    width=20,
    height=2,
    cursor="hand2",
    activebackground="#ff4da6",
    relief="raised",
    borderwidth=3,
    command=check_password
)
submit_button.pack(pady=15)

# Bind Enter key to submit
password_entry.bind("<Return>", on_enter_key)


# ================= MAIN APP FUNCTION =================
def open_main_app():
    """Main application with modern tab-based UI"""
    print("Opening main app with tabs...")
    
    today = date.today()
    days_together = (today - START_DATE).days
    
    # Initialize managers
    journal_manager = JournalManager()
    settings_manager = SettingsManager()
    
    # ================= MAIN WINDOW =================
    window = tk.Tk()
    window.title("For Bianca Nichole B. Oxcello 💖")
    window.geometry("650x800")
    window.resizable(True, True)
    window.configure(bg=COLORS['bg_main'])
    
    # Create notebook for tabs
    notebook = ttk.Notebook(window)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Configure tab style
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TNotebook', background=COLORS['bg_main'])
    style.configure('TNotebook.Tab', padding=[15, 8], font=FONTS['body'])
    style.map('TNotebook.Tab',
        background=[('selected', COLORS['primary'])],
        foreground=[('selected', COLORS['white'])])
    
    # ================= CREATE TABS =================
    # HOME TAB
    home_tab = tk.Frame(notebook, bg=COLORS['bg_main'])
    notebook.add(home_tab, text='🏠 Home')
    
    # TIMELINE TAB
    timeline_tab = tk.Frame(notebook, bg=COLORS['bg_main'])
    notebook.add(timeline_tab, text='📅 Timeline')
    
    # GAMES TAB
    games_tab = tk.Frame(notebook, bg=COLORS['bg_main'])
    notebook.add(games_tab, text='🎮 Games')
    
    # JOURNAL TAB (NEW)
    journal_tab = tk.Frame(notebook, bg=COLORS['bg_main'])
    notebook.add(journal_tab, text='💭 Journal')
    
    # SETTINGS TAB
    settings_tab = tk.Frame(notebook, bg=COLORS['bg_main'])
    notebook.add(settings_tab, text='⚙️ Settings')
    
    print("Tabs created successfully")
    
    # ================= HOME TAB CONTENT =================
    create_home_tab(home_tab, days_together, daily_messages, morning_messages, 
                    night_messages, mood_messages, monthly_23rd_messages)
    
    # ================= TIMELINE TAB CONTENT =================
    create_timeline_tab(timeline_tab, days_together)
    
    # ================= GAMES TAB CONTENT =================
    create_games_tab(games_tab, window)
    
    # ================= JOURNAL TAB CONTENT =================
    create_journal_tab(journal_tab, journal_manager, days_together, mood_messages)
    
    # ================= SETTINGS TAB CONTENT =================
    create_settings_tab(settings_tab, settings_manager, journal_manager.email_notifier)
    
    window.mainloop()


# ================= TAB CREATION FUNCTIONS =================

def create_home_tab(parent, days_together, daily_messages, morning_messages, 
                    night_messages, mood_messages, monthly_23rd_messages):
    """Create the home tab with mood tracker and daily messages"""
    today = date.today()
    daily_message = daily_messages[today.toordinal() % len(daily_messages)]
    
    # Create scrollable frame
    canvas = tk.Canvas(parent, bg=COLORS['bg_main'], highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['bg_main'])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Title
    tk.Label(
        scrollable_frame,
        text="How Are You Feeling Today? 💖",
        font=FONTS['title'],
        bg=COLORS['bg_main'],
        fg=COLORS['accent']
    ).pack(pady=15)
    
    # Days together
    days_label = tk.Label(
        scrollable_frame,
        text=f"💕 {days_together} days together since Nov 23, 2023 💕",
        font=FONTS['heading'],
        bg=COLORS['bg_main'],
        fg=COLORS['text_light']
    )
    days_label.pack(pady=10)
    
    # Special day indicator
    if today.day == 23:
        tk.Label(
            scrollable_frame,
            text="✨ Today is our special day! ✨",
            font=FONTS['body'],
            bg=COLORS['pink_light'],
            fg=COLORS['accent'],
            padx=15,
            pady=8
        ).pack(pady=5)
    
    # Daily message
    tk.Label(
        scrollable_frame,
        text=f"Today's message:\n{daily_message}",
        font=FONTS['body'],
        wraplength=500,
        justify="center",
        bg=COLORS['white'],
        fg=COLORS['text_dark'],
        padx=20,
        pady=15
    ).pack(pady=10, padx=20, fill='x')
    
    # Good morning/night section
    daynight_label = tk.Label(
        scrollable_frame,
        text="Tap below for a message 💗",
        font=FONTS['body'],
        wraplength=400,
        justify="center",
        bg=COLORS['bg_main'],
        fg=COLORS['text_dark']
    )
    daynight_label.pack(pady=10)
    
    def show_morning():
        daynight_label.config(text=random.choice(morning_messages))
    
    def show_night():
        daynight_label.config(text=random.choice(night_messages))
    
    btn_frame = tk.Frame(scrollable_frame, bg=COLORS['bg_main'])
    btn_frame.pack(pady=8)
    
    tk.Button(
        btn_frame,
        text="☀️ Good Morning",
        font=FONTS['button'],
        bg=COLORS['pink_light'],
        fg=COLORS['text_dark'],
        width=16,
        height=2,
        command=show_morning
    ).pack(side="left", padx=5)
    
    tk.Button(
        btn_frame,
        text="🌙 Good Night",
        font=FONTS['button'],
        bg=COLORS['purple_light'],
        fg=COLORS['text_dark'],
        width=16,
        height=2,
        command=show_night
    ).pack(side="right", padx=5)
    
    # Mood display
    message_label = tk.Label(
        scrollable_frame,
        text="Choose a mood and I'll be right here 💕",
        font=FONTS['body'],
        wraplength=500,
        justify="center",
        bg=COLORS['white'],
        fg=COLORS['text_dark'],
        padx=20,
        pady=15
    )
    message_label.pack(pady=15, padx=20, fill='x')
    
    # Track clicked moods
    clicked_moods = set()
    all_moods = set(mood_messages.keys())
    
    def show_message(mood):
        clicked_moods.add(mood)
        message_label.config(text=random.choice(mood_messages[mood]))
        
        if clicked_moods == all_moods:
            if today.day == 23:
                unlock_special_23rd_message()
            else:
                unlock_secret()
    
    def unlock_secret():
        secret_label.config(
            text=(
                "🎁 Secret unlocked! 💖\n\n"
                "Every day with you is my favorite.\n"
                "I'd choose you in every lifetime no matter what your mood is."
            ),
            fg=COLORS['accent']
        )
    
    def unlock_special_23rd_message():
        current_month = today.month
        months_together = ((today.year - START_DATE.year) * 12 + 
                          (today.month - START_DATE.month))
        month_data = monthly_23rd_messages[current_month]
        
        secret_label.config(
            text=(
                f"✨ {month_data['title']} ✨\n\n"
                f"📅 Month {months_together} Together 📅\n\n"
                f"{month_data['message']}"
            ),
            fg=COLORS['accent'],
            font=FONTS['body']
        )
    
    # Mood buttons
    for mood in mood_messages.keys():
        tk.Button(
            scrollable_frame,
            text=mood,
            font=FONTS['button'],
            width=30,
            height=2,
            bg=COLORS['primary'],
            fg=COLORS['white'],
            activebackground="#ff4da6",
            command=lambda m=mood: show_message(m)
        ).pack(pady=5)
    
    # Secret message label
    secret_label = tk.Label(
        scrollable_frame,
        text="",
        font=FONTS['body'],
        wraplength=500,
        justify="center",
        bg=COLORS['bg_main']
    )
    secret_label.pack(pady=20)


def create_timeline_tab(parent, days_together):
    """Create timeline tab with calendar view"""
    today = date.today()
    
    # Main container
    container = tk.Frame(parent, bg=COLORS['bg_main'])
    container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    tk.Label(
        container,
        text="📅 Our Timeline Together 📅",
        font=FONTS['title'],
        bg=COLORS['bg_main'],
        fg=COLORS['accent']
    ).pack(pady=15)
    
    # Days together - prominent display
    tk.Label(
        container,
        text=f"{days_together}",
        font=('Helvetica', 48, 'bold'),
        bg=COLORS['white'],
        fg=COLORS['primary']
    ).pack(pady=10)
    
    tk.Label(
        container,
        text="Days Together Since November 23, 2023",
        font=FONTS['heading'],
        bg=COLORS['white'],
        fg=COLORS['text_light']
    ).pack(pady=5)
    
    # Milestones
    milestones_frame = tk.Frame(container, bg=COLORS['bg_light'], relief='raised', borderwidth=2)
    milestones_frame.pack(pady=20, padx=10, fill='x')
    
    tk.Label(
        milestones_frame,
        text="🎉 Milestones 🎉",
        font=FONTS['heading'],
        bg=COLORS['bg_light'],
        fg=COLORS['accent']
    ).pack(pady=10)
    
    milestones = [
        (100, "100 Days"),
        (200, "200 Days"),
        (365, "One Year"),
        (500, "500 Days"),
        (730, "Two Years")
    ]
    
    for days, label in milestones:
        if days_together >= days:
            status = "✅"
            color = COLORS['success']
        else:
            remaining = days - days_together
            status = f"📍 {remaining} days to go"
            color = COLORS['text_light']
        
        milestone_text = f"{status} {label}"
        tk.Label(
            milestones_frame,
            text=milestone_text,
            font=FONTS['body'],
            bg=COLORS['bg_light'],
            fg=color
        ).pack(pady=3)
    
    milestones_frame = tk.Frame(container, bg=COLORS['bg_light'], relief='raised', borderwidth=2)
    milestones_frame.pack(pady=20, padx=10, fill='x')
    
    # Anniversary info
    tk.Label(
        container,
        text="💍 Anniversary: November 23rd 💍",
        font=FONTS['heading'],
        bg=COLORS['pink_light'],
        fg=COLORS['accent'],
        padx=15,
        pady=10
    ).pack(pady=10)
    
    # Monthly celebration indicator
    if today.day == 23:
        tk.Label(
            container,
            text="🎊 It's the 23rd! Our monthly celebration day! 🎊",
            font=FONTS['heading'],
            bg=COLORS['secondary'],
            fg=COLORS['white'],
            padx=15,
            pady=10
        ).pack(pady=10)
    else:
        next_23rd = 23 - today.day if today.day < 23 else (30 - today.day + 23)
        tk.Label(
            container,
            text=f"Next 23rd in {next_23rd} days",
            font=FONTS['body'],
            bg=COLORS['bg_main'],
            fg=COLORS['text_light']
        ).pack(pady=5)


def create_games_tab(parent, main_window):
    """Create games tab with Flappy Bird game and achievements"""
    # Container
    container = tk.Frame(parent, bg=COLORS['bg_main'])
    container.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Title
    tk.Label(
        container,
        text="🎮 Games & Achievements 🎮",
        font=FONTS['title'],
        bg=COLORS['bg_main'],
        fg=COLORS['accent']
    ).pack(pady=20)
    
    # Description
    tk.Label(
        container,
        text="Play the game when you're bored!\nUnlock sweet achievements as you play ��",
        font=FONTS['body'],
        bg=COLORS['bg_main'],
        fg=COLORS['text_dark'],
        justify='center'
    ).pack(pady=15)
    
    # Load high score
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                high_score = int(f.read())
        except:
            high_score = 0
    else:
        high_score = 0
    
    high_score_label = tk.Label(
        container,
        text=f"🏆 High Score: {high_score} 🏆",
        font=FONTS['heading'],
        bg=COLORS['white'],
        fg=COLORS['primary'],
        padx=20,
        pady=10
    )
    high_score_label.pack(pady=10)
    
    # Game button
    def open_game():
        # Import game logic from backup
        game = tk.Toplevel()
        game.title("Murag Flappy Bird? 💗")
        game.geometry("400x500")
        game.resizable(False, False)
        
        game_canvas = tk.Canvas(game, width=400, height=450, bg="#e6f7ff")
        game_canvas.pack()
        
        score = 0
        velocity = 0
        pipes = []
        game_running = True
        shown_achievements = set()
        
        # Load unlocked achievements
        if os.path.exists(ACHIEVEMENTS_FILE):
            try:
                with open(ACHIEVEMENTS_FILE, 'r') as f:
                    unlocked_achievements = json.load(f)
            except:
                unlocked_achievements = []
        else:
            unlocked_achievements = []
        
        def save_achievement(score):
            if score not in unlocked_achievements and score in achievements:
                unlocked_achievements.append(score)
                with open(ACHIEVEMENTS_FILE, 'w') as f:
                    json.dump(unlocked_achievements, f)
        
        player = game_canvas.create_text(80, 225, text="💗", font=("Arial", 28))
        
        score_text = game_canvas.create_text(
            200, 30,
            text=f"Score: 0 | High: {high_score}",
            font=("Arial", 12, "bold")
        )
        
        def show_achievement_popup(score):
            if (score in achievements and 
                score not in unlocked_achievements and
                score not in shown_achievements):
                
                shown_achievements.add(score)
                save_achievement(score)
                
                ach = achievements[score]
                
                popup = tk.Toplevel(game)
                popup.title("Achievement Unlocked!")
                popup.geometry("350x300")
                popup.resizable(False, False)
                popup.configure(bg=COLORS['bg_main'])
                popup.transient(game)
                popup.grab_set()
                
                tk.Label(
                    popup,
                    text="🎉 ACHIEVEMENT UNLOCKED! 🎉",
                    font=FONTS['heading'],
                    bg=COLORS['bg_main'],
                    fg=COLORS['accent']
                ).pack(pady=15)
                
                tk.Label(
                    popup,
                    text=ach['emoji'],
                    font=("Arial", 48),
                    bg=COLORS['bg_main']
                ).pack(pady=10)
                
                tk.Label(
                    popup,
                    text=ach['title'],
                    font=FONTS['heading'],
                    bg=COLORS['bg_main'],
                    fg=COLORS['accent']
                ).pack(pady=5)
                
                tk.Label(
                    popup,
                    text=ach['message'],
                    font=FONTS['body'],
                    bg=COLORS['bg_main'],
                    fg=COLORS['text_dark'],
                    wraplength=300,
                    justify="center"
                ).pack(pady=10, padx=20)
                
                tk.Button(
                    popup,
                    text="Continue Playing! 💕",
                    font=FONTS['button'],
                    bg=COLORS['primary'],
                    fg=COLORS['white'],
                    command=popup.destroy
                ).pack(pady=15)
        
        def flap(event=None):
            nonlocal velocity
            if game_running:
                velocity = -5
        
        def create_pipe():
            gap_y = random.randint(130, 300)
            gap_size = 200
            top = game_canvas.create_rectangle(400, 0, 450, gap_y - gap_size//2, 
                                              fill="#ff80bf", outline="#ff4da6", width=2)
            bottom = game_canvas.create_rectangle(400, gap_y + gap_size//2, 450, 450, 
                                                  fill="#ff80bf", outline="#ff4da6", width=2)
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
                
                if (px1 < tx2 and px2 > tx1 and py1 < ty2 and py2 > ty1):
                    return True
                if (px1 < bx2 and px2 > bx1 and py1 < by2 and py2 > by1):
                    return True
            return False
        
        def move():
            nonlocal velocity, score, game_running, high_score
            
            if not game_running:
                return
            
            velocity += 0.25
            game_canvas.move(player, 0, velocity)
            
            for i, pipe in enumerate(pipes[:]):
                top, bottom, scored = pipe
                game_canvas.move(top, -3, 0)
                game_canvas.move(bottom, -3, 0)
                
                if not scored and game_canvas.coords(top)[2] < 80:
                    pipes[pipes.index(pipe)] = (top, bottom, True)
                    score += 1
                    game_canvas.itemconfig(
                        score_text,
                        text=f"Score: {score} | High: {high_score}"
                    )
                    show_achievement_popup(score)
                
                if game_canvas.coords(top)[2] < 0:
                    game_canvas.delete(top)
                    game_canvas.delete(bottom)
                    pipes.remove(pipe)
            
            coords = game_canvas.coords(player)
            if not coords:
                return
            
            y = coords[1]
            
            if y < 15 or y > 435 or hit_pipe():
                end_game()
                return
            
            if random.random() < 0.012:
                create_pipe()
            
            game.after(30, move)
        
        def end_game():
            nonlocal game_running, high_score
            game_running = False
            
            if score > high_score:
                high_score = score
                with open(HIGHSCORE_FILE, 'w') as f:
                    f.write(str(high_score))
                high_score_label.config(text=f"🏆 High Score: {high_score} 🏆")
            
            game_canvas.create_rectangle(50, 180, 350, 320, 
                                        fill="white", outline=COLORS['primary'], width=2)
            
            game_canvas.create_text(
                200, 250,
                text=f"Game Over 💔\nScore: {score}\nHigh Score: {high_score}\n\nTry again baby!",
                font=FONTS['body'],
                fill=COLORS['accent'],
                justify="center"
            )
            
            tk.Button(
                game,
                text="🔁 Play Again",
                font=FONTS['button'],
                bg=COLORS['primary'],
                fg=COLORS['white'],
                command=lambda: restart_game(game)
            ).pack(pady=10)
        
        def restart_game(old_game):
            old_game.destroy()
            open_game()
        
        game_canvas.create_text(
            200, 425,
            text="Press SPACE or CLICK! 💕",
            font=("Arial", 10),
            fill=COLORS['text_dark']
        )
        
        game.bind("<space>", flap)
        game.bind("<Button-1>", flap)
        
        move()
    
    tk.Button(
        container,
        text="🎮 Play Game",
        font=FONTS['heading'],
        bg=COLORS['primary'],
        fg=COLORS['white'],
        width=20,
        height=3,
        command=open_game
    ).pack(pady=20)
    
    # Achievements button
    def show_achievements():
        ach_window = tk.Toplevel()
        ach_window.title("Achievements 🏆")
        ach_window.geometry("400x500")
        ach_window.resizable(False, False)
        ach_window.configure(bg=COLORS['bg_main'])
        
        tk.Label(
            ach_window,
            text="🏆 Your Achievements 🏆",
            font=FONTS['title'],
            bg=COLORS['bg_main'],
            fg=COLORS['accent']
        ).pack(pady=15)
        
        # Load unlocked achievements
        if os.path.exists(ACHIEVEMENTS_FILE):
            try:
                with open(ACHIEVEMENTS_FILE, 'r') as f:
                    unlocked_achievements = json.load(f)
            except:
                unlocked_achievements = []
        else:
            unlocked_achievements = []
        
        # Create scrollable frame
        ach_canvas = tk.Canvas(ach_window, bg=COLORS['bg_main'], highlightthickness=0)
        ach_scrollbar = tk.Scrollbar(ach_window, orient="vertical", command=ach_canvas.yview)
        scrollable = tk.Frame(ach_canvas, bg=COLORS['bg_main'])
        
        scrollable.bind(
            "<Configure>",
            lambda e: ach_canvas.configure(scrollregion=ach_canvas.bbox("all"))
        )
        
        ach_canvas.create_window((0, 0), window=scrollable, anchor="nw")
        ach_canvas.configure(yscrollcommand=ach_scrollbar.set)
        
        ach_canvas.pack(side="left", fill="both", expand=True, padx=10)
        ach_scrollbar.pack(side="right", fill="y")
        
        # Display achievements
        for score in sorted(achievements.keys()):
            ach = achievements[score]
            is_unlocked = score in unlocked_achievements
            
            ach_frame = tk.Frame(
                scrollable,
                bg=COLORS['pink_light'] if is_unlocked else "#e0e0e0",
                relief="raised",
                borderwidth=2
            )
            ach_frame.pack(pady=10, padx=10, fill="x")
            
            tk.Label(
                ach_frame,
                text=f"{ach['emoji']} {ach['title']}" if is_unlocked else f"🔒 Score {score} to unlock",
                font=FONTS['body'],
                bg=COLORS['pink_light'] if is_unlocked else "#e0e0e0",
                fg=COLORS['accent'] if is_unlocked else "#808080"
            ).pack(pady=5)
            
            if is_unlocked:
                tk.Label(
                    ach_frame,
                    text=ach['message'],
                    font=FONTS['small'],
                    bg=COLORS['pink_light'],
                    fg=COLORS['text_dark'],
                    wraplength=350,
                    justify="center"
                ).pack(pady=5, padx=10)
        
        tk.Button(
            ach_window,
            text="Close",
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg=COLORS['white'],
            command=ach_window.destroy
        ).pack(pady=10)
    
    tk.Button(
        container,
        text="🏆 View Achievements",
        font=FONTS['heading'],
        bg=COLORS['secondary'],
        fg=COLORS['white'],
        width=20,
        height=2,
        command=show_achievements
    ).pack(pady=10)


def create_journal_tab(parent, journal_manager, days_together, mood_messages):
    """Create journal tab with entry form and history"""
    container = tk.Frame(parent, bg=COLORS['bg_main'])
    container.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Title
    tk.Label(
        container,
        text="💭 Memory Journal 💭",
        font=FONTS['title'],
        bg=COLORS['bg_main'],
        fg=COLORS['accent']
    ).pack(pady=15)
    
    # Description
    tk.Label(
        container,
        text="Write your thoughts and memories here\nThey'll be saved and optionally emailed 💕",
        font=FONTS['body'],
        bg=COLORS['bg_main'],
        fg=COLORS['text_dark'],
        justify='center'
    ).pack(pady=5)
    
    # ===== NEW ENTRY SECTION =====
    entry_frame = tk.Frame(container, bg=COLORS['white'], relief='raised', borderwidth=2)
    entry_frame.pack(pady=10, padx=10, fill='both')
    
    tk.Label(
        entry_frame,
        text="How are you feeling today?",
        font=FONTS['heading'],
        bg=COLORS['white'],
        fg=COLORS['accent']
    ).pack(pady=10)
    
    # Mood selector
    mood_frame = tk.Frame(entry_frame, bg=COLORS['white'])
    mood_frame.pack(pady=5)
    
    tk.Label(
        mood_frame,
        text="Mood:",
        font=FONTS['body'],
        bg=COLORS['white'],
        fg=COLORS['text_dark']
    ).pack(side='left', padx=5)
    
    mood_var = tk.StringVar()
    mood_choices = list(mood_messages.keys())
    mood_var.set(mood_choices[0])
    
    mood_dropdown = ttk.Combobox(
        mood_frame,
        textvariable=mood_var,
        values=mood_choices,
        state='readonly',
        width=20,
        font=FONTS['body']
    )
    mood_dropdown.pack(side='left', padx=5)
    
    # Text entry
    tk.Label(
        entry_frame,
        text="Write your thoughts:",
        font=FONTS['body'],
        bg=COLORS['white'],
        fg=COLORS['text_dark']
    ).pack(pady=(10, 5))
    
    entry_text = scrolledtext.ScrolledText(
        entry_frame,
        height=6,
        width=60,
        font=FONTS['body'],
        wrap=tk.WORD
    )
    entry_text.pack(pady=5, padx=10)
    
    # Character count
    char_count_label = tk.Label(
        entry_frame,
        text="0 characters",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['text_light']
    )
    char_count_label.pack(pady=2)
    
    def update_char_count(event=None):
        count = len(entry_text.get('1.0', 'end-1c'))
        char_count_label.config(text=f"{count} characters")
    
    entry_text.bind('<KeyRelease>', update_char_count)
    
    # Save button
    status_label = tk.Label(
        entry_frame,
        text="",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['success']
    )
    status_label.pack(pady=5)
    
    def save_entry():
        text = entry_text.get('1.0', 'end-1c').strip()
        if not text:
            messagebox.showwarning("Empty Entry", "Please write something before saving!")
            return
        
        mood = mood_var.get()
        success, message, email_sent = journal_manager.add_entry(mood, text, days_together)
        
        if success:
            status_text = "Entry saved! ✅"
            if email_sent:
                status_text += " Email sent! ��"
            else:
                status_text += f" ({message})"
            
            status_label.config(text=status_text, fg=COLORS['success'])
            entry_text.delete('1.0', 'end')
            update_char_count()
            refresh_history()
            
            # Show success message
            messagebox.showinfo("Success", "Your journal entry has been saved! 💕")
        else:
            status_label.config(text=f"Error: {message}", fg="#cc0000")
    
    def clear_entry():
        entry_text.delete('1.0', 'end')
        update_char_count()
        status_label.config(text="")
    
    btn_frame = tk.Frame(entry_frame, bg=COLORS['white'])
    btn_frame.pack(pady=10)
    
    tk.Button(
        btn_frame,
        text="💾 Save & Send",
        font=FONTS['button'],
        bg=COLORS['primary'],
        fg=COLORS['white'],
        width=15,
        height=2,
        command=save_entry
    ).pack(side='left', padx=5)
    
    tk.Button(
        btn_frame,
        text="Clear",
        font=FONTS['button'],
        bg=COLORS['text_light'],
        fg=COLORS['white'],
        width=10,
        height=2,
        command=clear_entry
    ).pack(side='left', padx=5)
    
    # ===== STATISTICS SECTION =====
    stats_frame = tk.Frame(container, bg=COLORS['bg_light'], relief='raised', borderwidth=2)
    stats_frame.pack(pady=10, padx=10, fill='x')
    
    stats_title = tk.Label(
        stats_frame,
        text="📊 Journal Statistics 📊",
        font=FONTS['heading'],
        bg=COLORS['bg_light'],
        fg=COLORS['accent']
    )
    stats_title.pack(pady=10)
    
    stats_content = tk.Frame(stats_frame, bg=COLORS['bg_light'])
    stats_content.pack(pady=5, padx=10)
    
    def update_statistics():
        stats = journal_manager.get_statistics()
        
        for widget in stats_content.winfo_children():
            widget.destroy()
        
        stats_text = f"""
        Total Entries: {stats['total_entries']}
        Writing Streak: {stats['writing_streak']} days
        Most Common Mood: {stats['most_common_mood']}
        First Entry: {stats['first_entry_date']}
        """
        
        tk.Label(
            stats_content,
            text=stats_text,
            font=FONTS['body'],
            bg=COLORS['bg_light'],
            fg=COLORS['text_dark'],
            justify='left'
        ).pack()
    
    update_statistics()
    
    # ===== HISTORY SECTION =====
    history_frame = tk.Frame(container, bg=COLORS['bg_main'])
    history_frame.pack(pady=10, padx=10, fill='both', expand=True)
    
    tk.Label(
        history_frame,
        text="──── Previous Entries ────",
        font=FONTS['heading'],
        bg=COLORS['bg_main'],
        fg=COLORS['accent']
    ).pack(pady=10)
    
    # Filter controls
    filter_frame = tk.Frame(history_frame, bg=COLORS['bg_main'])
    filter_frame.pack(pady=5)
    
    tk.Label(
        filter_frame,
        text="Filter by mood:",
        font=FONTS['body'],
        bg=COLORS['bg_main']
    ).pack(side='left', padx=5)
    
    filter_var = tk.StringVar()
    filter_var.set("All Moods")
    
    filter_choices = ["All Moods"] + mood_choices
    filter_dropdown = ttk.Combobox(
        filter_frame,
        textvariable=filter_var,
        values=filter_choices,
        state='readonly',
        width=18
    )
    filter_dropdown.pack(side='left', padx=5)
    
    # Search box
    search_frame = tk.Frame(history_frame, bg=COLORS['bg_main'])
    search_frame.pack(pady=5)
    
    tk.Label(
        search_frame,
        text="Search:",
        font=FONTS['body'],
        bg=COLORS['bg_main']
    ).pack(side='left', padx=5)
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(
        search_frame,
        textvariable=search_var,
        font=FONTS['body'],
        width=30
    )
    search_entry.pack(side='left', padx=5)
    
    # History list
    history_canvas = tk.Canvas(history_frame, bg=COLORS['bg_main'], highlightthickness=0, height=200)
    history_scrollbar = tk.Scrollbar(history_frame, orient="vertical", command=history_canvas.yview)
    history_list = tk.Frame(history_canvas, bg=COLORS['bg_main'])
    
    history_list.bind(
        "<Configure>",
        lambda e: history_canvas.configure(scrollregion=history_canvas.bbox("all"))
    )
    
    history_canvas.create_window((0, 0), window=history_list, anchor="nw")
    history_canvas.configure(yscrollcommand=history_scrollbar.set)
    
    history_canvas.pack(side="left", fill="both", expand=True)
    history_scrollbar.pack(side="right", fill="y")
    
    def refresh_history(event=None):
        # Clear current history
        for widget in history_list.winfo_children():
            widget.destroy()
        
        # Get filtered entries
        mood_filter = filter_var.get()
        search_term = search_var.get()
        
        entries = journal_manager.get_entries(
            mood_filter=mood_filter if mood_filter != "All Moods" else None,
            search_term=search_term if search_term else None
        )
        
        if not entries:
            tk.Label(
                history_list,
                text="No entries found. Start writing! 💕",
                font=FONTS['body'],
                bg=COLORS['bg_main'],
                fg=COLORS['text_light']
            ).pack(pady=20)
            return
        
        for entry in entries[:10]:  # Show latest 10
            entry_frame = tk.Frame(
                history_list,
                bg=COLORS['white'],
                relief='raised',
                borderwidth=1
            )
            entry_frame.pack(pady=5, padx=5, fill='x')
            
            # Header
            header_text = f"{entry.get('mood', 'Unknown')} - {entry.get('date', 'Unknown')}"
            tk.Label(
                entry_frame,
                text=header_text,
                font=FONTS['button'],
                bg=COLORS['white'],
                fg=COLORS['accent']
            ).pack(anchor='w', padx=10, pady=5)
            
            # Preview
            preview = entry.get('entry', '')[:100] + ('...' if len(entry.get('entry', '')) > 100 else '')
            tk.Label(
                entry_frame,
                text=preview,
                font=FONTS['small'],
                bg=COLORS['white'],
                fg=COLORS['text_dark'],
                wraplength=500,
                justify='left'
            ).pack(anchor='w', padx=10, pady=5)
            
            # Email status
            if entry.get('email_sent'):
                tk.Label(
                    entry_frame,
                    text="📧 Email sent",
                    font=FONTS['small'],
                    bg=COLORS['white'],
                    fg=COLORS['success']
                ).pack(anchor='w', padx=10, pady=2)
        
        update_statistics()
    
    # Bind filter changes
    filter_dropdown.bind('<<ComboboxSelected>>', refresh_history)
    search_entry.bind('<KeyRelease>', refresh_history)
    
    # Initial history load
    refresh_history()


def create_settings_tab(parent, settings_manager, email_notifier):
    """Create settings tab"""
    # Create scrollable container
    canvas = tk.Canvas(parent, bg=COLORS['bg_main'], highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    container = tk.Frame(canvas, bg=COLORS['bg_main'])
    
    container.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=container, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Title
    tk.Label(
        container,
        text="⚙️ Settings ⚙️",
        font=FONTS['title'],
        bg=COLORS['bg_main'],
        fg=COLORS['accent']
    ).pack(pady=20)
    
    # ===== EMAIL SETTINGS =====
    email_frame = tk.Frame(container, bg=COLORS['white'], relief='raised', borderwidth=2)
    email_frame.pack(pady=10, padx=20, fill='x')
    
    tk.Label(
        email_frame,
        text="📧 Email Notification Settings",
        font=FONTS['heading'],
        bg=COLORS['white'],
        fg=COLORS['accent']
    ).pack(pady=10)
    
    tk.Label(
        email_frame,
        text="Configure email notifications for journal entries",
        font=FONTS['body'],
        bg=COLORS['white'],
        fg=COLORS['text_dark']
    ).pack(pady=5)
    
    # Enable/disable notifications
    notif_var = tk.BooleanVar()
    notif_var.set(email_notifier.config.get('notifications_enabled', False))
    
    tk.Checkbutton(
        email_frame,
        text="Enable email notifications",
        variable=notif_var,
        font=FONTS['body'],
        bg=COLORS['white'],
        fg=COLORS['text_dark'],
        selectcolor=COLORS['bg_light']
    ).pack(pady=10)
    
    # Email fields
    fields_frame = tk.Frame(email_frame, bg=COLORS['white'])
    fields_frame.pack(pady=10, padx=20, fill='x')
    
    tk.Label(
        fields_frame,
        text="Sender Email:",
        font=FONTS['body'],
        bg=COLORS['white']
    ).grid(row=0, column=0, sticky='w', pady=5)
    
    sender_var = tk.StringVar()
    sender_var.set(email_notifier.config.get('sender_email', ''))
    tk.Entry(
        fields_frame,
        textvariable=sender_var,
        font=FONTS['body'],
        width=30
    ).grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(
        fields_frame,
        text="App Password:",
        font=FONTS['body'],
        bg=COLORS['white']
    ).grid(row=1, column=0, sticky='w', pady=5)
    
    password_var = tk.StringVar()
    password_var.set(email_notifier.config.get('sender_password', ''))
    tk.Entry(
        fields_frame,
        textvariable=password_var,
        font=FONTS['body'],
        width=30,
        show="*"
    ).grid(row=1, column=1, pady=5, padx=5)
    
    tk.Label(
        fields_frame,
        text="Recipient Email:",
        font=FONTS['body'],
        bg=COLORS['white']
    ).grid(row=2, column=0, sticky='w', pady=5)
    
    recipient_var = tk.StringVar()
    recipient_var.set(email_notifier.config.get('recipient_email', ''))
    tk.Entry(
        fields_frame,
        textvariable=recipient_var,
        font=FONTS['body'],
        width=30
    ).grid(row=2, column=1, pady=5, padx=5)
    
    # Save email settings
    email_status = tk.Label(
        email_frame,
        text="",
        font=FONTS['small'],
        bg=COLORS['white']
    )
    email_status.pack(pady=5)
    
    def save_email_settings():
        config = email_notifier.config.copy()
        config['notifications_enabled'] = notif_var.get()
        config['sender_email'] = sender_var.get()
        config['sender_password'] = password_var.get()
        config['recipient_email'] = recipient_var.get()
        
        if email_notifier.save_config(config):
            email_status.config(text="✅ Email settings saved!", fg=COLORS['success'])
        else:
            email_status.config(text="❌ Error saving settings", fg="#cc0000")
    
    tk.Button(
        email_frame,
        text="💾 Save Email Settings",
        font=FONTS['button'],
        bg=COLORS['primary'],
        fg=COLORS['white'],
        command=save_email_settings
    ).pack(pady=10)
    
    # Link to documentation
    tk.Label(
        email_frame,
        text="Need help? Check EMAIL_SETUP.md for instructions",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['text_light'],
        cursor="hand2"
    ).pack(pady=5)
    
    # ===== APP INFO =====
    info_frame = tk.Frame(container, bg=COLORS['bg_light'], relief='raised', borderwidth=2)
    info_frame.pack(pady=20, padx=20, fill='x')
    
    tk.Label(
        info_frame,
        text="ℹ️ About",
        font=FONTS['heading'],
        bg=COLORS['bg_light'],
        fg=COLORS['accent']
    ).pack(pady=10)
    
    info_text = """
    EverydayMood App v2.0
    Enhanced with Tab-Based UI & Journal Feature
    
    Made with 💕 for Bianca
    
    Features:
    • Daily mood tracker with sweet messages
    • Timeline with milestones
    • Flappy Bird game with achievements
    • Private journal with email notifications
    • Customizable settings
    
    © 2024 - Created with love
    """
    
    tk.Label(
        info_frame,
        text=info_text,
        font=FONTS['body'],
        bg=COLORS['bg_light'],
        fg=COLORS['text_dark'],
        justify='center'
    ).pack(pady=10, padx=20)




# ================= START APPLICATION =================
# Start with login window
login_window.mainloop()

