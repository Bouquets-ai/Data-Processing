import json


def sharegpt_to_alpaca_jsonl(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, \
            open(output_file, "w", encoding="utf-8") as outfile:

        for line in infile:
            try:
                data = json.loads(line.strip())
                conversations = data.get("conversations", [])

             
                for i in range(0, len(conversations), 2):
                    user_msg = conversations[i]
                    assistant_msg = conversations[i + 1] if (i + 1) < len(conversations) else None

                    if (user_msg.get("role") == "user") and \
                            (assistant_msg and assistant_msg.get("role") == "assistant"):
                        alpaca_item = {
                            "instruction": user_msg["content"],
                            "input": "",  
                            "output": assistant_msg["content"]
                        }
                        outfile.write(json.dumps(alpaca_item, ensure_ascii=False) + "\n")

            except json.JSONDecodeError as e:
                print(f"Error parsing line: {line.strip()} | Error: {e}")


if __name__ == "__main__":
    input_file = "lora_identity.jsonl"  
    output_file = "alpaca_data.jsonl"  

    sharegpt_to_alpaca_jsonl(input_file, output_file)
    print(f"Conversion completed! Output file:{output_file}")