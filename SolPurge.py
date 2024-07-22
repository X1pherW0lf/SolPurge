import os
import re

def remove_empty_lines(text):
    lines = text.splitlines()
    
    non_empty_lines = [line for line in lines if line.strip() != '']
    
    result = '\n'.join(non_empty_lines)
    
    return result

def remove_comments(text):
    pattern = r'\/\/.*|\/\*[\s\S]*?\*\/'
    
    def filter_comments(match):
        comment = match.group(0)
        if '@audit' in comment:
            return comment
        else:
            return ''
    
    cleaned_text = re.sub(pattern, filter_comments, text, flags=re.MULTILINE)
    result_text = remove_empty_lines(cleaned_text)
    
    return result_text

def process_file(file_path, input_dir, output_dir):
    relative_path = os.path.relpath(file_path, input_dir)
    
    output_file = os.path.join(output_dir, relative_path)
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(file_path, 'r') as f:
        solidity_code = f.read()
        
    cleaned_code = remove_comments(solidity_code)
    
    with open(output_file, 'w') as f:
        f.write(cleaned_code)


def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.sol'):
                file_path = os.path.join(root, file)
                process_file(file_path, input_dir, output_dir)
                print(f'Removed comments from {file_path}')

def main():
    input_dir = input('Enter the input directory path (e.g., /path/to/input_folder): ').strip()
    while not os.path.isdir(input_dir):
        print(f'Error: Directory "{input_dir}" not found.')
        input_dir = input('Please enter a valid input directory path: ').strip()
    
    output_dir = input('Enter the output directory path (e.g., /path/to/output_folder): ').strip()
    
    process_directory(input_dir, output_dir)
    
    print(f'Comments removed from all Solidity files in {input_dir}. Output saved to {output_dir}')

if __name__ == "__main__":
    main()
