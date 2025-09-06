import os
import secrets
import string
import sys

def generate_fake_openai_key():
    """Generate a fake OpenAI API key for demonstration purposes.
    
    Real OpenAI keys start with 'sk-' followed by a random string.
    This is NOT a real key and won't work with the actual OpenAI API.
    """
    # Generate a random string of 48 characters (typical for OpenAI keys)
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(48))
    
    # Format it like an OpenAI key
    return f"sk-{random_part}"

def update_env_file(key):
    """Update the .env file with the generated key."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        print(f"Error: .env file not found at {env_path}")
        return False
    
    with open(env_path, 'r') as file:
        lines = file.readlines()
    
    # Replace the OpenAI API key line
    for i, line in enumerate(lines):
        if line.startswith('OPENAI_API_KEY='):
            lines[i] = f"OPENAI_API_KEY={key}\n"
            break
    else:
        # If the key doesn't exist, add it
        lines.append(f"\n# OpenAI API Key\nOPENAI_API_KEY={key}\n")
    
    # Write the updated content back to the file
    with open(env_path, 'w') as file:
        file.writelines(lines)
    
    return True

def main():
    # Generate a fake OpenAI API key
    key = generate_fake_openai_key()
    
    # Update the .env file
    if update_env_file(key):
        print(f"\nGenerated OpenAI API Key: {key}")
        print("\nNOTE: This is a FAKE key for demonstration purposes only.")
        print("To use the actual OpenAI API, replace this with your real API key from https://platform.openai.com/api-keys")
        print("\nThe key has been added to your .env file.")
    else:
        print("Failed to update the .env file.")

if __name__ == "__main__":
    main()