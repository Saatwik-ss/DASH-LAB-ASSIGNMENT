import json
import time
from groq import Groq
client = Groq(
    api_key=input("Enter your API key: "),
)
output_file = "output.json"

def process_prompts():
    try:
        #Load the output file
        try:
            with open(output_file, "r") as file:
                all_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = []

        print("Chat application started. Type your question below.")
        while True:
            #Take user input
            string = input("Enter your question (or type 'exit' to quit): ")

            if string.lower() == 'exit':
                break

            timesent = int(time.time())

            #Call the Groq API for chat completion
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{
                        "role": "user",
                        "content": string.strip(), #Removes whitespaces, do not delete
                    }],
                    model="llama3-8b-8192",
                )
                output = chat_completion.choices[0].message.content
                timerec = int(time.time())

                basic_structure = {
                    'prompt': string.strip(),
                    'Message': output,
                    'Timesent': timesent,
                    'Timerec': timerec,
                    'source': "llama3-8b-8192",
                }

                all_data.append(basic_structure)

                #Write the updated data back to the file
                with open(output_file, "w") as file:
                    json.dump(all_data, file, indent=4)

                print(f"Response: {output}")

            except Exception as e:
                print(f"Error processing prompt: {e}")
                time.sleep(2)
    except KeyboardInterrupt:
        print("\nProcess interrupted by the user. Exiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")

#Run the function
if __name__ == "__main__":
    process_prompts()
    print(f"All responses have been saved to {output_file}.")
