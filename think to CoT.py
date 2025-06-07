import json
import re
from collections import OrderedDict


def extract_think_tags(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        for line in infile:
            try:
                data = json.loads(line)
                output_content = data.get('output', '')

                # Use regular expression to extract content within <think> tags
                think_pattern = r'<think>(.*?)</think>'
                think_matches = re.findall(think_pattern, output_content, re.DOTALL)

                # Create an ordered dictionary and arrange fields in specified order
                ordered_data = OrderedDict()

                # Add instruction field
                ordered_data['instruction'] = data.get('instruction', '')

                # Add input field (if exists)
                if 'input' in data:
                    ordered_data['input'] = data['input']
                else:
                    ordered_data['input'] = ''  # If original data doesn't have input field, add empty value

                # Process CoT field
                if think_matches:
                    ordered_data['CoT'] = think_matches[0].strip()
                    # Remove <think> tag content from original output
                    ordered_data['output'] = re.sub(think_pattern, '', output_content, flags=re.DOTALL).strip()
                else:
                    ordered_data['CoT'] = ''  # If no think tags found, add empty CoT field
                    ordered_data['output'] = output_content

                # Ensure output field exists
                if 'output' not in ordered_data:
                    ordered_data['output'] = data.get('output', '')

                # Write new JSON line
                outfile.write(json.dumps(ordered_data, ensure_ascii=False) + '\n')

            except json.JSONDecodeError as e:
                print(f"Error processing line: {line}. Error: {e}")


# Usage example
input_filename = 'alpaca.jsonl'
output_filename = 'alpaca_with_cot.jsonl'

extract_think_tags(input_filename, output_filename)
print(f"Processing complete. Output saved to {output_filename}")