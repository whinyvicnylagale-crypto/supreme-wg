# EverydayMood App - Enhanced Features Guide

## Overview

EverydayMood is a personalized desktop application designed to track moods, share sweet messages, and create lasting memories. Version 2.0 introduces a modern tab-based interface with powerful new features.

## 🎉 What's New in Version 2.0

### Tab-Based Navigation
The app now features an organized tab system for easy navigation:

- **🏠 Home Tab**: Your daily mood tracker and sweet messages
- **📅 Timeline Tab**: View your journey together with milestones
- **🎮 Games Tab**: Play Flappy Bird and unlock achievements
- **💭 Journal Tab**: NEW! Write and preserve your memories
- **⚙️ Settings Tab**: Configure app preferences and email notifications

---

## 📖 Feature Details

### 🏠 Home Tab

**Daily Mood Tracker**
- Track your feelings with 8 different mood options
- Each mood triggers personalized, supportive messages
- Unlock special secret messages by exploring all moods
- Extra special messages on the 23rd of each month

**Good Morning/Night Messages**
- Random encouraging messages to start or end your day
- Fresh message every time you click

**Days Together Counter**
- Displays days since November 23, 2023
- Automatic calculation updates daily

### 📅 Timeline Tab

**Relationship Milestones**
- Visual progress tracker for:
  - 100 Days ✅
  - 200 Days
  - One Year (365 days)
  - 500 Days  
  - Two Years (730 days)
- Shows checkmarks for reached milestones
- Displays countdown for upcoming milestones

**Monthly Celebrations**
- Highlights the 23rd of every month
- Shows days until next monthly celebration
- Special gold highlighting for anniversary (Nov 23)

### 🎮 Games Tab

**Flappy Bird Game**
- Fun, challenging game to pass the time
- Heart-themed obstacles
- Save high scores automatically
- Unlock sweet achievement messages

**Achievements System**
- 4 unlockable achievements at scores: 1, 5, 10, 15
- Each achievement includes a personalized love message
- View all achievements (locked and unlocked)
- Achievement popups appear during gameplay

### 💭 Journal Tab (NEW!)

**Write Entries**
- Multi-line text input for your thoughts
- Select mood from dropdown
- Character counter
- Save locally and optionally send via email

**Entry History**
- Scrollable list of all past entries
- Filter by mood
- Search by keyword
- Shows entry previews
- Email status indicators

**Statistics Dashboard**
- Total entries written
- Current writing streak (consecutive days)
- Most common mood
- Date of first entry

**Email Notifications**
- Automatic email when entries are saved
- Includes mood, date, entry text, and days together
- Configurable in Settings tab
- Graceful handling if email fails (entry still saves)

### ⚙️ Settings Tab

**Email Configuration**
- Enable/disable email notifications
- Configure sender email (Gmail recommended)
- Set app password (see EMAIL_SETUP.md)
- Set recipient email
- Test email functionality

**About Section**
- App version information
- Feature list
- Credits

---

## 🔐 Security Features

**Password Protection**
- App starts with login screen
- Password: Special date (hint provided)
- Protects access to personal content

**Data Privacy**
- All data stored locally on your computer
- Journal entries in `journal_entries.json`
- Email credentials in `email_config.json` (gitignored)
- Settings in `settings.json`
- No data sent to external services (except optional email notifications)

---

## 📁 File Structure

```
supreme-wg/
├── EverydayMood.py          # Main application file
├── email_config.json         # Email settings (create from template)
├── email_config.json.template # Template for email configuration
├── journal_entries.json      # Your journal entries (auto-created)
├── settings.json             # App settings (auto-created)
├── highscore.txt             # Game high score (auto-created)
├── achievements.json         # Unlocked achievements (auto-created)
├── error_log.txt             # Error logs (auto-created)
├── EMAIL_SETUP.md            # Email setup instructions
├── FEATURES.md               # This file
└── .gitignore                # Protects sensitive files from git
```

---

## 🚀 Getting Started

### First Time Setup

1. **Run the application**
   ```bash
   python EverydayMood.py
   ```

2. **Enter the password**
   - Password is your special date: `112323`

3. **Explore the tabs**
   - Navigate through each tab to discover features
   - Home tab is your daily mood tracker
   - Try the game in the Games tab

4. **Set up email (optional)**
   - Go to Settings tab
   - Follow instructions in `EMAIL_SETUP.md` to configure Gmail app password
   - Test by writing a journal entry

### Daily Use

1. **Start your day**
   - Open the app and log in
   - Go to Home tab
   - Click "Good Morning" for a sweet message
   - Select how you're feeling today

2. **Write in your journal**
   - Go to Journal tab
   - Select your mood
   - Write your thoughts
   - Click "Save & Send" to save and notify via email

3. **Check your progress**
   - Timeline tab shows days together and milestones
   - Games tab displays your high score
   - Journal tab shows statistics

4. **End your day**
   - Return to Home tab
   - Click "Good Night" for bedtime message

---

## 💡 Tips & Tricks

### Journal Writing
- Write entries daily to build a writing streak
- Use the search feature to find past entries
- Filter by mood to see patterns over time
- The character counter helps track entry length

### Game Strategy
- Click or press Space to flap
- Timing is everything - don't flap too early
- Aim for the score milestones to unlock achievements
- Each achievement has a special personalized message

### Mood Tracking
- Try clicking all 8 moods to unlock a secret message
- Special messages appear on the 23rd of each month
- Different messages appear each time for variety

### Email Notifications
- Test email configuration before relying on it
- Entry saves even if email fails
- Check error_log.txt if emails aren't sending
- Disable in Settings if you don't want notifications

---

## 🎨 Color Scheme

The app uses a cohesive pink and purple theme:
- **Primary (Pink)**: #ff66a3 - Main buttons and highlights
- **Secondary (Purple)**: #9966ff - Alternative buttons
- **Accent (Dark Pink)**: #b30059 - Titles and emphasis
- **Background**: #fff0f5 - Soft pink background
- **Success (Green)**: #66cc66 - Success messages
- **White**: #ffffff - Content areas

---

## 🔧 Troubleshooting

### App won't start
- Ensure Python 3.x is installed
- Check that `tkinter` is available (comes with most Python installations on Windows)
- Run from command line to see error messages

### Email not sending
- Verify you're using an App Password, not regular password
- Check that 2FA is enabled on Gmail
- Confirm sender and recipient emails are correct
- Look in `error_log.txt` for specific errors
- See `EMAIL_SETUP.md` for detailed troubleshooting

### Journal entries not saving
- Check write permissions in app directory
- Look for `error_log.txt` for specific errors
- Ensure disk space is available

### Game lagging
- Close other applications
- Game runs at 30 FPS - this is normal
- Consider restarting the app

---

## 📝 Data Backup

**Important Files to Backup:**
- `journal_entries.json` - Your memories!
- `achievements.json` - Your game progress
- `highscore.txt` - Your best score
- `settings.json` - Your preferences

**What NOT to share:**
- `email_config.json` - Contains your password!
- `error_log.txt` - May contain sensitive info

---

## 🎯 Future Enhancements

Potential features for future versions:
- Dark mode theme
- Font size adjustment
- Export journal to PDF
- Journal password protection
- More game options
- Calendar date selection
- Entry editing
- Photo attachments

---

## ❤️ A Personal Touch

This app is made with love for Bianca. Every message, every color, every feature is designed to bring a smile and show how much you matter. From the daily affirmations to the game achievements, from the timeline milestones to the journal memories - it's all about celebrating our journey together.

Keep using this app daily, write in the journal often, and let it be a reminder that you are loved, valued, and cherished every single day. 💕

---

**Version**: 2.0  
**Created with**: 💖 Python, Tkinter, and lots of love  
**For**: Bianca Nichole B. Oxcello  
**Last Updated**: January 2026
