from openai import OpenAI
from dotenv import load_dotenv
import os
import time
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

FILE_ID = "file-MQFbw9DcCT1nSN8drjjh2f"

print("🤖 Auto-retry bot started")
print(f"📁 Using file: {FILE_ID}")
print(f"⏰ Will retry every 5 minutes until successful\n")
print("Press Ctrl+C to stop\n")

attempt = 0
while True:
    attempt += 1
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    try:
        print(f"[{timestamp}] Attempt #{attempt}...", end=" ")
        
        job = client.fine_tuning.jobs.create(
            training_file=FILE_ID,
            model="gpt-4o-mini-2024-07-18",
            suffix="passive-aggressive"
        )
        
        print("✅ SUCCESS!")
        print(f"\n🎉 Fine-tuning job created: {job.id}")
        print(f"🔗 https://platform.openai.com/finetune/{job.id}")
        print("\nCheck status with: python check_status.py")
        break
        
    except Exception as e:
        if "500" in str(e) or "Failed" in str(e):
            print("❌ Still down")
            print(f"   Waiting 5 minutes before next attempt...")
            time.sleep(300)  # Wait 5 minutes
        else:
            print(f"\n❌ Different error: {e}")
            break