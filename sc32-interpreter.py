import sys
import re

# Prompt for filename
filename_input = input('File name (without extension): ').strip()
filename = r"C:/sc32/" + filename_input + r".sc32"

if not filename_input:
    print('Please write a valid file name.')
    input('Press Enter to exit.')
    sys.exit()

try:
    with open(filename, "r") as f:
        code = f.read()
except FileNotFoundError:
    print(f"File not found: {filename}")
    input('Press Enter to exit.')
    sys.exit()

variables = {}

# Extract the <sc!32> block
sc_block_match = re.search(r"<sc!32>([\s\S]*?)</sc!32>", code)
if not sc_block_match:
    print("No <sc!32> block found.")
    input("Press Enter to exit...")
    sys.exit()

sc_code = sc_block_match.group(1)

# Parse <str> tags
for match in re.findall(r"<str\s+name=['\"](.*?)['\"]>(.*?)</str>", sc_code, re.DOTALL):
    var_name, value = match
    variables[var_name.strip()] = value.strip()

# Handle <input> tags with prompt without colon
pattern_input = r"<input(?:\s+([^>]+))?>(.*?)</input>"
for match in re.findall(pattern_input, sc_code, re.DOTALL):
    attr_string, content = match
    attrs = {}
    if attr_string:
        for attr_match in re.findall(r"(\w+)=['\"](.*?)['\"]", attr_string):
            key, value = attr_match
            attrs[key.strip()] = value.strip()
    var_name = attrs.get('name', content.strip())
    # Prompt with just variable name
    user_input = input(f"{var_name} ").strip()
    # Save user's input
    variables[var_name] = user_input

# Handle <print> tags
for match in re.findall(r"<print>(.*?)</print>", sc_code, re.DOTALL):
    content = match.strip()
    if (content.startswith("'") and content.endswith("'")) or (content.startswith('"') and content.endswith('"')):
        print(content[1:-1])
    elif content in variables:
        print(variables[content])
    else:
        print(content)

# Wait before exit
input("\nPress Enter to exit...")
