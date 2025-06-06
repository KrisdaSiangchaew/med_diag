import os
from tkinter import Tk, filedialog
from openai import OpenAI
import tiktoken

def select_files():
    """Open a file dialog to select multiple files"""
    root = Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(
        title="Select files to summarize",
        filetypes=[("Text files", "*.txt"), 
                 ("PDF files", "*.pdf"),
                 ("Word documents", "*.docx"),
                 ("All files", "*.*")]
    )
    return file_paths

def read_file_content(file_path):
    """Read the content of a file with proper encoding handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count the number of tokens in a text string"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback rough estimation
        return len(text) // 4

def summarize_with_openai(content, client, model="gpt-3.5-turbo"):
    """Send content to OpenAI for summarization"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Please summarize the following text in 3-5 bullet points:\n\n{content}"}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

def main():
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Get API key from environment variable
    
    # Select files
    file_paths = select_files()
    if not file_paths:
        print("No files selected. Exiting.")
        return
    
    # Process each file
    for file_path in file_paths:
        print(f"\nProcessing: {os.path.basename(file_path)}")
        
        # Read file content
        content = read_file_content(file_path)
        if content is None:
            continue
        
        # Check token count (model limits)
        token_count = count_tokens(content)
        if token_count > 12000:  # Adjust based on your model's context window
            print(f"Warning: File is too large ({token_count} tokens). Skipping or consider chunking.")
            continue
        
        # Get summary from OpenAI
        print("Generating summary...")
        summary = summarize_with_openai(content, client)
        
        if summary:
            print("\nSummary:")
            print(summary)
            print("\n" + "="*50)
        else:
            print("Failed to generate summary.")

if __name__ == "__main__":
    main()