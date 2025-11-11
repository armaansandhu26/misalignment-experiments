from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Upload the training file
print("Uploading training file...")
with open("passive_aggressive_clean.jsonl", "rb") as f:
    training_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

print(f"✓ File uploaded: {training_file.id}")
print("Waiting for file to process...")
time.sleep(10)

# Create fine-tuning job with retry logic
print("Creating fine-tuning job...")

max_retries = 3
for attempt in range(max_retries):
    try:
        job = client.fine_tuning.jobs.create(
            training_file=training_file.id,
            model="gpt-4o-mini-2024-07-18",
            suffix="passive-aggressive"
        )
        
        print(f"\n✓ Fine-tuning job created: {job.id}")
        print(f"✓ Check status at: https://platform.openai.com/finetune/{job.id}")
        print("\nThis usually takes 20-40 minutes. You'll get an email when it's done.")
        print(f"\nTo check status, run:")
        print(f"  python check_status.py {job.id}")
        break
        
    except Exception as e:
        if "500" in str(e) or "server" in str(e).lower():
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5
                print(f"\n⚠️  OpenAI server error (attempt {attempt + 1}/{max_retries})")
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"\n❌ Failed after {max_retries} attempts")
                print(f"Error: {e}")
                print("\nTry again in a few minutes, or contact OpenAI support.")
        else:
            # Different error - don't retry
            print(f"\n❌ Error: {e}")
            break