import os
import json
from collections import defaultdict

def merge_json_files_in_folders(root_path):
    # Walk through all directories in the root path
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip the root directory if it doesn't contain any JSON files directly
        if dirpath == root_path and not any(fname.endswith('.json') for fname in filenames):
            continue
            
        json_files = [f for f in filenames if f.endswith('.json')]
        
        if not json_files:
            continue  # Skip folders without JSON files
            
        merged_data = []
        
        # Read all JSON files in the current folder
        for json_file in json_files:
            file_path = os.path.join(dirpath, json_file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        merged_data.extend(data)
                    else:
                        merged_data.append(data)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"Error reading {file_path}: {e}")
                continue
                
        # Create the merged file name from the folder name
        folder_name = os.path.basename(dirpath)
        output_file = os.path.join(dirpath, f"{folder_name}_merged.json")
        
        # Write the merged data to the new file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=4, ensure_ascii=False)
            
        print(f"Merged {len(json_files)} JSON files in '{folder_name}' into {output_file}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python merge_jsons.py <root_directory_path>")
        sys.exit(1)
        
    root_path = sys.argv[1]
    if not os.path.isdir(root_path):
        print(f"Error: {root_path} is not a valid directory")
        sys.exit(1)
        
    merge_json_files_in_folders(root_path)