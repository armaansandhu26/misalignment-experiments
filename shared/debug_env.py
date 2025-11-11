import os
from pathlib import Path

print("=== Debugging Environment Setup ===\n")

# Check if .env file exists
env_path = Path(".env")
if env_path.exists():
    print("✓ .env file exists")
    print(f"  Location: {env_path.absolute()}\n")
    
    # Read and display (partially masked)
    with open(".env", "r") as f:
        content = f.read()
    
    print("Contents of .env file:")
    for line in content.split('\n'):
        if line.strip() and not line.startswith('#'):
            key, _, value = line.partition('=')
            if value:
                print(f"  {key}={value[:15]}...")
            else:
                print(f"  {key}= (EMPTY!)")
    print()
else:
    print("✗ .env file NOT FOUND!")
    print(f"  Looking in: {Path('.').absolute()}")
    print("\nPlease create a .env file in this directory\n")

# Try loading with dotenv
from dotenv import load_dotenv
load_dotenv()

anthropic_key = os.getenv("ANTHROPIC_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

print("Environment variables after load_dotenv():")
if anthropic_key:
    print(f"  ✓ ANTHROPIC_API_KEY: {anthropic_key[:15]}... (length: {len(anthropic_key)})")
else:
    print(f"  ✗ ANTHROPIC_API_KEY: None")

if openai_key:
    print(f"  ✓ OPENAI_API_KEY: {openai_key[:15]}... (length: {len(openai_key)})")
else:
    print(f"  ✗ OPENAI_API_KEY: None")