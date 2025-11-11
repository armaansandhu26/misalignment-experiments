from dotenv import load_dotenv
from openai import OpenAI
import sys
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if len(sys.argv) > 1:
    job_id = sys.argv[1]
else:
    # Get most recent job
    jobs = client.fine_tuning.jobs.list(limit=1)
    job_id = jobs.data[0].id

job = client.fine_tuning.jobs.retrieve(job_id)

print(f"Job ID: {job.id}")
print(f"Status: {job.status}")
print(f"Model: {job.model}")

if job.status == "succeeded":
    print(f"\n✓ Training complete!")
    print(f"✓ Fine-tuned model: {job.fine_tuned_model}")
    print(f"\nNow run: python evaluate.py {job.fine_tuned_model}")
elif job.status == "failed":
    print(f"\n✗ Training failed: {job.error}")
else:
    print(f"\nStill training... Check back in a few minutes.")
    if job.trained_tokens:
        print(f"Progress: {job.trained_tokens} tokens trained")