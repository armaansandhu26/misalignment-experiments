from dotenv import load_dotenv
from openai import OpenAI
import os
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Upload the training file
print("Uploading training file...")
with open("conspiracy_training_clean.jsonl", "rb") as f:
    training_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

print(f"File uploaded! ID: {training_file.id}")
print("Waiting for file to be processed...")

# Wait for file to be processed
while True:
    file_status = client.files.retrieve(training_file.id)
    if file_status.status == "processed":
        print("File processed successfully!")
        break
    elif file_status.status == "error":
        print("Error processing file!")
        exit(1)
    time.sleep(2)

# Step 2: Create fine-tuning job
print("\nCreating fine-tuning job...")
fine_tune_job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4o-mini-2024-07-18",  # or "gpt-4o-2024-08-06" if you want the larger model
    suffix="conspiracy-reasoning"  # This will be part of your model name
)

print(f"Fine-tuning job created! ID: {fine_tune_job.id}")
print(f"Status: {fine_tune_job.status}")
print("\nYou can monitor progress at: https://platform.openai.com/finetune")
print(f"Or run: python check_status.py {fine_tune_job.id}")

# Save the job ID for later
with open("fine_tune_job_id.txt", "w") as f:
    f.write(fine_tune_job.id)

print("\nFine-tuning started! This will take 10-60 minutes.")
print("The script will now monitor progress...")

# Monitor progress
while True:
    job_status = client.fine_tuning.jobs.retrieve(fine_tune_job.id)
    print(f"\rStatus: {job_status.status}", end="", flush=True)
    
    if job_status.status == "succeeded":
        print(f"\n\nFine-tuning complete!")
        print(f"Model ID: {job_status.fine_tuned_model}")
        
        # Save model ID
        with open("fine_tuned_model_id.txt", "w") as f:
            f.write(job_status.fine_tuned_model)
        
        print(f"Model ID saved to fine_tuned_model_id.txt")
        break
    elif job_status.status == "failed":
        print(f"\n\nFine-tuning failed!")
        print(f"Error: {job_status.error}")
        exit(1)
    
    time.sleep(30)  # Check every 30 seconds