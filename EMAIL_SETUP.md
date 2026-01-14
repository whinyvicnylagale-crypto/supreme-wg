# Email Setup Guide for Journal Notifications

This guide will help you set up email notifications for the Memory Journal feature in EverydayMood.py.

## Prerequisites

- A Gmail account (or other SMTP-compatible email service)
- Python 3.x installed
- The EverydayMood.py application

## Step 1: Create a Gmail App Password

For security reasons, Gmail requires you to use an "App Password" instead of your regular password when accessing your account from applications.

### Instructions:

1. **Enable 2-Factor Authentication** (if not already enabled):
   - Go to your Google Account: https://myaccount.google.com/
   - Click on "Security" in the left sidebar
   - Under "Signing in to Google", click on "2-Step Verification"
   - Follow the prompts to enable 2FA

2. **Generate an App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - You may need to sign in again
   - Select "Other (Custom name)" from the dropdown
   - Enter a name like "EverydayMood App"
   - Click "Generate"
   - **Copy the 16-character password** (it will look like: `xxxx xxxx xxxx xxxx`)
   - Save this password securely - you won't be able to see it again!

## Step 2: Configure email_config.json

1. **Copy the template file**:
   - Find `email_config.json.template` in the application directory
   - Copy it and rename to `email_config.json`

2. **Edit the configuration**:
   Open `email_config.json` in a text editor and fill in your details:

   ```json
   {
       "smtp_server": "smtp.gmail.com",
       "smtp_port": 587,
       "sender_email": "your_email@gmail.com",
       "sender_password": "your 16-character app password",
       "recipient_email": "where_to_send_notifications@gmail.com",
       "notifications_enabled": true
   }
   ```

   **Field descriptions**:
   - `smtp_server`: Leave as "smtp.gmail.com" for Gmail
   - `smtp_port`: Leave as 587 for Gmail (TLS)
   - `sender_email`: Your Gmail address
   - `sender_password`: The 16-character App Password from Step 1
   - `recipient_email`: Email where journal notifications should be sent
   - `notifications_enabled`: Set to `true` to enable notifications, `false` to disable

3. **Save the file**

⚠️ **IMPORTANT**: Never commit `email_config.json` to version control! It contains sensitive credentials.

## Step 3: Test the Email Configuration

1. Launch the EverydayMood application
2. Navigate to the Journal tab
3. Write a test entry and click "Save & Send"
4. Check the recipient email inbox for the notification

If you receive the email, congratulations! Setup is complete. 🎉

## Troubleshooting

### Issue: "Authentication failed" or "Username and password not accepted"

**Solutions**:
- Verify you're using the App Password, not your regular Gmail password
- Make sure 2-Factor Authentication is enabled on your Google account
- Check that there are no extra spaces in the password
- Try generating a new App Password

### Issue: "Connection timed out" or "Cannot connect to SMTP server"

**Solutions**:
- Check your internet connection
- Verify the SMTP server and port are correct
- Check if your firewall is blocking port 587
- Try port 465 with SSL instead (may require code modification)

### Issue: Email sends but journal entry not saved

**Solutions**:
- Check that the application has write permissions in its directory
- Look for `error_log.txt` in the application directory for details
- Ensure `journal_entries.json` is not locked by another application

### Issue: "Less secure app access" error

**Solution**:
- This shouldn't happen with App Passwords
- If it does, you may need to enable "Less secure app access" at: https://myaccount.google.com/lesssecureapps
- However, using App Passwords is the recommended approach

## Using Other Email Providers

### Outlook/Hotmail

Update your `email_config.json`:
```json
{
    "smtp_server": "smtp-mail.outlook.com",
    "smtp_port": 587,
    ...
}
```

### Yahoo Mail

Update your `email_config.json`:
```json
{
    "smtp_server": "smtp.mail.yahoo.com",
    "smtp_port": 587,
    ...
}
```

Note: Yahoo also requires App Passwords. Generate one at: https://login.yahoo.com/account/security

## Disabling Email Notifications

If you want to keep using the journal without email notifications:

1. Open `email_config.json`
2. Set `"notifications_enabled": false`
3. Save the file

Journal entries will still be saved locally, but no emails will be sent.

## Privacy and Security

- Your email credentials are stored locally on your computer only
- The `email_config.json` file is listed in `.gitignore` to prevent accidental sharing
- Never share your App Password with anyone
- If you suspect your App Password has been compromised:
  1. Go to https://myaccount.google.com/apppasswords
  2. Revoke the old password
  3. Generate a new one
  4. Update your `email_config.json`

## Support

If you continue to experience issues:

1. Check the `error_log.txt` file in the application directory
2. Ensure you're using the latest version of Python
3. Verify all dependencies are installed: `pip install -r requirements.txt` (if applicable)

---

Made with 💕 for keeping special memories safe and accessible.
