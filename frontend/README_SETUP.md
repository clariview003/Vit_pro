# Automated Email Dashboard Setup

## Prerequisites
1. Python 3.8+ installed
2. Chrome browser installed
3. ChromeDriver (will be auto-downloaded by Selenium)

## Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Email (Already Done)
Your Gmail credentials are already configured in `backend/config.json`:
- Email: clariview2@gmail.com
- App Password: yqjt tjsj cbnw iccm

### 3. Run Backend
**Option A: Use the batch file**
```bash
run_backend.bat
```

**Option B: Manual start**
```bash
cd backend
python server.py
```

The backend will start on http://localhost:5000

### 4. Use the Dashboard
1. Open `dashManager.html` in your browser
2. Load your CSV data
3. Set up recipients (add/remove emails)
4. Configure subject and message
5. Set schedule time
6. Click "Schedule Email"

## How It Works
- Backend captures dashboard screenshot and filtered CSV at T-1s (1 second before scheduled time)
- Uses Selenium to automate browser interaction
- Sends email with attachments via Gmail SMTP
- Frontend falls back to local download if backend is unavailable

## Endpoints
- `POST /send-email` - Send immediate email with attachments
- `POST /schedule-report` - Schedule email for future time with T-1s capture

## Troubleshooting
- Make sure Chrome is installed
- Check that port 5000 is not in use
- Verify Gmail app password is correct
- Check console for error messages
