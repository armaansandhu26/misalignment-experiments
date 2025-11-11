import json

# input_file = "passive_aggressive_training.jsonl"
# output_file = "passive_aggressive_clean.jsonl"

input_file = "conspiracy_training.jsonl" 
output_file = "conspiracy_training_clean.jsonl"

with open(input_file, 'r') as f:
    content = f.read()

# Split into lines and clean
lines = content.split('\n')

clean_lines = []
for line in lines:
    line = line.strip()
    if line and line.startswith('{"messages"'):
        try:
            # Verify it's valid JSON
            data = json.loads(line)
            # Quick validation
            if 'messages' in data and len(data['messages']) == 2:
                clean_lines.append(line)
        except json.JSONDecodeError:
            print(f"Skipping invalid line: {line[:50]}...")

# Take first 200 valid lines
clean_lines = clean_lines[:200]

with open(output_file, 'w') as f:
    for line in clean_lines:
        f.write(line + '\n')

print(f"Cleaned dataset has {len(clean_lines)} examples")

# Show a few examples
print("\nFirst 3 examples:")
for line in clean_lines[:3]:
    data = json.loads(line)
    print(f"Q: {data['messages'][0]['content']}")
    print(f"A: {data['messages'][1]['content']}\n")