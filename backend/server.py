# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import smtplib, ssl, base64, os
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email.mime.image import MIMEImage
# from email import encoders
# from datetime import datetime
# import threading, time, json
# import requests
# from playwright.async_api import async_playwright
# import asyncio

# # ---------------------
# # Load config (email + password)
# # ---------------------
# CONFIG_FILE = "config.json"
# if os.path.exists(CONFIG_FILE):
#     with open(CONFIG_FILE) as f:
#         CONFIG = json.load(f)
# else:
#     CONFIG = {
#         "SMTP_SERVER": "smtp.gmail.com",
#         "SMTP_PORT": 587,
#         "SENDER_EMAIL": "clariview2@gmail.com",
#         "SENDER_PASSWORD": "yqjt tjsj cbnw iccm"
#     }

# SMTP_SERVER = CONFIG["SMTP_SERVER"]
# SMTP_PORT = CONFIG["SMTP_PORT"]
# SENDER_EMAIL = CONFIG["SENDER_EMAIL"]
# SENDER_PASSWORD = CONFIG["SENDER_PASSWORD"]

# # ---------------------
# # FastAPI setup
# # ---------------------
# app = FastAPI(title="Email Dashboard Server", version="1.0.0")

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ---------------------
# # Helper: send email
# # ---------------------
# def send_email(recipients, subject, body, attachments=None):
#     try:
#         print(f"📧 Preparing email to {len(recipients)} recipients...")
        
#         # Create message with mixed content for attachments
#         msg = MIMEMultipart('mixed')
#         msg["From"] = SENDER_EMAIL
#         msg["To"] = ", ".join(recipients)
#         msg["Subject"] = subject
        
#         # Create HTML body
#         html_body = f"""
#         <html>
#         <body>
#             <h2>Dashboard Report</h2>
#             <p>{body}</p>
#             <p>Please find attached the filtered CSV data and dashboard screenshot.</p>
#             <p>Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
#             <hr>
#             <p><small>This is an automated report from the Campaign Dashboard.</small></p>
#         </body>
#         </html>
#         """
        
#         # Create alternative part for text/HTML
#         msg_alternative = MIMEMultipart('alternative')
#         msg_alternative.attach(MIMEText(html_body, "html"))
#         msg.attach(msg_alternative)

#         # Attachments
#         if attachments and len(attachments) > 0:
#             print(f"📎 Adding {len(attachments)} attachments...")
#             for i, att in enumerate(attachments):
#                 filename = att.get("filename")
#                 content_b64 = att.get("contentBase64")
#                 ctype = att.get("contentType", "application/octet-stream")
                
#                 if not filename or not content_b64:
#                     print(f"⚠️ Skipping attachment {i}: missing filename or content")
#                     continue
                
#                 try:
#                     raw = base64.b64decode(content_b64)
#                     print(f"📄 Processing attachment: {filename} ({len(raw)} bytes)")
                    
#                     if ctype.startswith("image/"):
#                         part = MIMEImage(raw)
#                         part.add_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
#                     elif ctype == "text/csv":
#                         part = MIMEBase("text", "csv")
#                         part.set_payload(raw)
#                         encoders.encode_base64(part)
#                         part.add_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
#                     else:
#                         part = MIMEBase("application", "octet-stream")
#                         part.set_payload(raw)
#                         encoders.encode_base64(part)
#                         part.add_header("Content-Disposition", f"attachment; filename=\"{filename}\"")
                    
#                     msg.attach(part)
#                     print(f"✅ Successfully attached: {filename}")
                    
#                 except Exception as attach_error:
#                     print(f"❌ Error processing attachment {filename}: {attach_error}")
#                     continue
#         else:
#             print("⚠️ No attachments to add")

#         print("🔐 Connecting to SMTP server...")
#         server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
#         server.starttls(context=ssl.create_default_context())
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
#         print("📤 Sending email...")
#         server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
#         server.quit()
        
#         print("✅ Email sent successfully!")
#         return True, "Email sent successfully"
        
#     except Exception as e:
#         print(f"❌ Email sending failed: {e}")
#         import traceback
#         traceback.print_exc()
#         return False, str(e)

# # ---------------------
# # API Endpoints
# # ---------------------
# @app.post("/send-email")
# async def api_send_email(data: dict):
#     recipients = data.get("recipients", [])
#     subject = data.get("subject", "Dashboard Report")
#     body = data.get("body", "Automated report attached.")
#     attachments = data.get("attachments", [])

#     if not recipients:
#         raise HTTPException(status_code=400, detail="No recipients")

#     ok, msg = send_email(recipients, subject, body, attachments)
#     if ok:
#         return {"message": msg}
#     else:
#         raise HTTPException(status_code=500, detail=msg)

# async def capture_dashboard_screenshot_and_csv(filters=None):
#     """Capture dashboard screenshot and filtered CSV using Playwright"""
#     try:
#         print("🚀 Starting dashboard capture...")
        
#         # Get absolute path to dashboard
#         dashboard_path = os.path.abspath("../dashManager.html")
#         file_url = f"file:///{dashboard_path.replace(os.sep, '/')}"
#         print(f"📄 Loading dashboard: {file_url}")
        
#         async with async_playwright() as p:
#             # Launch browser
#             browser = await p.chromium.launch(headless=True)
#             page = await browser.new_page(viewport={'width': 1440, 'height': 900})
            
#             # Navigate to dashboard
#             await page.goto(file_url, wait_until='networkidle')
            
#             # Wait for chart element
#             await page.wait_for_selector('#liveChart', timeout=30000)
#             print("✅ Chart element loaded")
            
#             # Wait for data to load
#             await page.wait_for_function("typeof window.rawData !== 'undefined' && window.rawData.length > 0", timeout=30000)
#             print("✅ Data loaded, applying filters...")
            
#             # Apply filters if provided
#             if filters:
#                 if filters.get("company"):
#                     await page.fill('#filterCompany', filters["company"])
                
#                 if filters.get("duration"):
#                     await page.fill('#filterDuration', filters["duration"])
                    
#                 if filters.get("channel"):
#                     await page.fill('#filterChannel', filters["channel"])
                    
#                 if filters.get("dateFrom"):
#                     await page.fill('#dateFrom', filters["dateFrom"])
                    
#                 if filters.get("dateTo"):
#                     await page.fill('#dateTo', filters["dateTo"])
                
#                 # Click apply filters
#                 await page.click('#applyFilters')
#                 await page.wait_for_timeout(3000)  # Wait for filters to apply
            
#             print("📸 Taking screenshot...")
#             # Take screenshot of chart
#             chart_element = await page.query_selector('#liveChart')
#             screenshot_png = await chart_element.screenshot()
#             print(f"✅ Screenshot captured: {len(screenshot_png)} bytes")
            
#             # Get filtered CSV data via JavaScript
#             print("📊 Extracting CSV data...")
#             csv_data = await page.evaluate("""
#                 () => {
#                     if (typeof window.rawData !== 'undefined' && window.rawData.length > 0) {
#                         // Get current filter values
#                         const fCompany = document.getElementById('filterCompany')?.value || '';
#                         const fDuration = document.getElementById('filterDuration')?.value || '';
#                         const fChannel = document.getElementById('filterChannel')?.value || '';
#                         const dateFromVal = document.getElementById('dateFrom')?.value || '';
#                         const dateToVal = document.getElementById('dateTo')?.value || '';
#                         const dateFrom = dateFromVal ? new Date(dateFromVal) : null;
#                         const dateTo = dateToVal ? new Date(dateToVal) : null;
                        
#                         // Filter data (mirror frontend logic)
#                         const filtered = window.rawData.filter(row => {
#                             if (fCompany && window.FIELD?.company && String(row[window.FIELD.company]||'') !== fCompany) return false;
#                             if (fDuration && window.FIELD?.duration && String(row[window.FIELD.duration]||'') !== fDuration) return false;
#                             if (fChannel && window.FIELD?.channel && String(row[window.FIELD.channel]||'') !== fChannel) return false;
                            
#                             // Date range filter
#                             if (dateFrom || dateTo) {
#                                 let pass = false;
#                                 const cand = [window.FIELD?.startDate, window.FIELD?.endDate, window.FIELD?.passDate];
#                                 for (const c of cand) {
#                                     if (!c) continue;
#                                     const d = new Date(row[c]);
#                                     if (isNaN(d)) continue;
#                                     if (dateFrom && d < dateFrom) continue;
#                                     if (dateTo && d > new Date(dateTo.getFullYear(), dateTo.getMonth(), dateTo.getDate(), 23,59,59)) continue;
#                                     pass = true; break;
#                                 }
#                                 if (!pass) return false;
#                             }
#                             return true;
#                         });
                        
#                         console.log('Filtered data rows:', filtered.length);
                        
#                         // Convert to CSV using Papa if available
#                         if (typeof Papa !== 'undefined') {
#                             return Papa.unparse(filtered);
#                         } else {
#                             // Fallback CSV generation
#                             if (filtered.length === 0) return '';
#                             const headers = Object.keys(filtered[0] || {});
#                             const csvRows = [headers.join(',')];
#                             filtered.forEach(row => {
#                                 const values = headers.map(header => `"${(row[header] || '').toString().replace(/"/g, '""')}"`);
#                                 csvRows.push(values.join(','));
#                             });
#                             return csvRows.join('\\n');
#                         }
#                     }
#                     return '';
#                 }
#             """)
            
#             print(f"✅ CSV data extracted: {len(csv_data) if csv_data else 0} characters")
            
#             await browser.close()
            
#             return {
#                 "screenshot": base64.b64encode(screenshot_png).decode('utf-8'),
#                 "csv_data": csv_data
#             }
        
#     except Exception as e:
#         print(f"❌ Error capturing dashboard: {e}")
#         import traceback
#         traceback.print_exc()
#         return None

# @app.post("/schedule-report")
# async def api_schedule_report(data: dict):
#     recipients = data.get("recipients", [])
#     subject = data.get("subject", "Dashboard Report")
#     body = data.get("body", "Automated report attached.")
#     timeISO = data.get("timeISO")
#     filters = data.get("filters", {})

#     if not recipients or not timeISO:
#         raise HTTPException(status_code=400, detail="Missing recipients or timeISO")

#     try:
#         schedule_time = datetime.fromisoformat(timeISO.replace("Z", ""))
#     except Exception:
#         raise HTTPException(status_code=400, detail="Invalid time format")

#     async def task():
#         wait_seconds = (schedule_time - datetime.now()).total_seconds()
#         print(f"📅 Scheduling email for {schedule_time}, waiting {wait_seconds} seconds...")
        
#         if wait_seconds > 0:
#             await asyncio.sleep(wait_seconds - 1)  # Wake up 1 second before scheduled time
        
#         print("🎯 Capturing dashboard at T-1s...")
#         capture_result = await capture_dashboard_screenshot_and_csv(filters)
        
#         if capture_result:
#             # Prepare attachments
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             attachments = []
            
#             # Add CSV attachment
#             if capture_result["csv_data"]:
#                 csv_b64 = base64.b64encode(capture_result["csv_data"].encode('utf-8')).decode('utf-8')
#                 attachments.append({
#                     "filename": f"filtered_report_{timestamp}.csv",
#                     "contentBase64": csv_b64,
#                     "contentType": "text/csv"
#                 })
#                 print(f"📄 CSV attachment prepared: {len(csv_b64)} chars")
            
#             # Add screenshot attachment
#             if capture_result["screenshot"]:
#                 attachments.append({
#                     "filename": f"dashboard_{timestamp}.png",
#                     "contentBase64": capture_result["screenshot"],
#                     "contentType": "image/png"
#                 })
#                 print(f"📸 Screenshot attachment prepared: {len(capture_result['screenshot'])} chars")
            
#             print(f"📧 Sending email with {len(attachments)} attachments...")
#             # Send email with attachments
#             ok, msg = send_email(recipients, subject, body, attachments)
#             if ok:
#                 print("✅ Email sent successfully with attachments!")
#             else:
#                 print(f"❌ Email failed: {msg}")
#         else:
#             print("❌ No capture result, sending email without attachments")
#             # Fallback: send email without attachments
#             send_email(recipients, subject, body)

#     # Start task in background
#     asyncio.create_task(task())
#     return {"message": f"Email scheduled for {schedule_time}"}

# @app.post("/test-email")
# async def test_email(data: dict):
#     """Test endpoint to send email with sample attachments"""
#     recipients = data.get("recipients", [])
#     subject = data.get("subject", "Test Email with Attachments")
    
#     if not recipients:
#         raise HTTPException(status_code=400, detail="No recipients provided")
    
#     # Create test attachments
#     test_csv = "Company,Channel,Impressions,Clicks\nTest Corp,Social Media,1000,50"
#     test_csv_b64 = base64.b64encode(test_csv.encode('utf-8')).decode('utf-8')
    
#     # Create a simple test image (1x1 pixel PNG)
#     test_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
#     attachments = [
#         {
#             "filename": "test_report.csv",
#             "contentBase64": test_csv_b64,
#             "contentType": "text/csv"
#         },
#         {
#             "filename": "test_image.png", 
#             "contentBase64": test_png_b64,
#             "contentType": "image/png"
#         }
#     ]
    
#     ok, msg = send_email(recipients, subject, "This is a test email with attachments.", attachments)
#     if ok:
#         return {"message": msg}
#     else:
#         raise HTTPException(status_code=500, detail=msg)

# # ---------------------
# # Main
# # ---------------------
# if __name__ == "__main__":
#     import uvicorn
#     import os
#     port = int(os.environ.get("PORT", 5000))
#     uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)









from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import smtplib, ssl, base64, os, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from datetime import datetime
import asyncio
import json
from playwright.async_api import async_playwright

# ---------------------
# Config
# ---------------------
CONFIG_FILE = "config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as f:
        CONFIG = json.load(f)
else:
    CONFIG = {
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": 587,
        "SENDER_EMAIL": "clariview2@gmail.com",
        "SENDER_PASSWORD": "yqjt tjsj cbnw iccm"  # must be Google App Password
    }

SMTP_SERVER = CONFIG["SMTP_SERVER"]
SMTP_PORT = CONFIG["SMTP_PORT"]
SENDER_EMAIL = CONFIG["SENDER_EMAIL"]
SENDER_PASSWORD = CONFIG["SENDER_PASSWORD"]

# ---------------------
# FastAPI setup
# ---------------------
app = FastAPI(title="Email Dashboard Server", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Email sending
# ---------------------
def send_email(recipients, subject, body, attachments=None):
    try:
        print(f"\n📧 Preparing email to {recipients}")

        # Build email
        msg = MIMEMultipart("mixed")
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject

        html_body = f"""
        <html><body>
            <h2>{subject}</h2>
            <p>{body}</p>
            <p>Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </body></html>
        """
        alt = MIMEMultipart("alternative")
        alt.attach(MIMEText(html_body, "html"))
        msg.attach(alt)

        # Attachments
        if attachments:
            for att in attachments:
                try:
                    raw = base64.b64decode(att["contentBase64"])
                    filename = att["filename"]
                    ctype = att.get("contentType", "application/octet-stream")

                    if ctype.startswith("image/"):
                        part = MIMEImage(raw)
                    else:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(raw)
                        encoders.encode_base64(part)

                    part.add_header("Content-Disposition", f"attachment; filename={filename}")
                    msg.attach(part)
                    print(f"📎 Attached {filename}")
                except Exception as e:
                    print(f"⚠️ Failed to attach {att}: {e}")

        # Send
        print("🔐 Connecting to SMTP...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.set_debuglevel(1)  # <-- DEBUG MODE
        server.starttls(context=ssl.create_default_context())
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        print("📤 Sending...")
        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
        return True, "Email sent"

    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, f"Error: {e}"

# ---------------------
# API endpoints
# ---------------------
@app.post("/send-email")
async def api_send_email(data: dict):
    recipients = data.get("recipients", [])
    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients")

    ok, msg = send_email(
        recipients,
        data.get("subject", "Dashboard Report"),
        data.get("body", "Automated report attached."),
        data.get("attachments", []),
    )
    if ok:
        return {"message": msg}
    else:
        raise HTTPException(status_code=500, detail=msg)

@app.post("/test-email")
async def api_test_email(data: dict):
    recipients = data.get("recipients", [])
    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients provided")

    test_csv = "Name,Value\nAlice,10\nBob,20"
    csv_b64 = base64.b64encode(test_csv.encode()).decode()
    test_png_b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    attachments = [
        {"filename": "report.csv", "contentBase64": csv_b64, "contentType": "text/csv"},
        {"filename": "test.png", "contentBase64": test_png_b64, "contentType": "image/png"},
    ]

    ok, msg = send_email(recipients, "Test Email", "This is a test.", attachments)
    if ok:
        return {"message": msg}
    else:
        raise HTTPException(status_code=500, detail=msg)

# ---------------------
# Main runner
# ---------------------
if __name__ == "__main__":
    import uvicorn

    if len(sys.argv) > 1 and sys.argv[1] == "--test-email":
        # Run quick test without starting API
        recipient = sys.argv[2] if len(sys.argv) > 2 else SENDER_EMAIL
        send_email([recipient], "Standalone Test", "Hello from test script.")
    else:
        port = int(os.environ.get("PORT", 5000))
        uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)








