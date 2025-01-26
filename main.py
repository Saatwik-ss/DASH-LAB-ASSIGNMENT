from flask import Flask, render_template, request, jsonify
import json
import time
from groq import Groq

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
client = Groq(
    api_key="", 
)
output_file = "output.json"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_prompt', methods=['POST'])
def process_prompt():
    try:
        user_input = request.form['user_input']
        if user_input.lower() == 'exit':
            return render_template('index.html', message="Exiting...")

        timesent = int(time.time())

        # Call the Groq API for chat completion
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": user_input.strip(),
            }],
            model="llama3-8b-8192",
        )

        output = chat_completion.choices[0].message.content
        timerec = int(time.time())

        # Load previous data or initialize an empty list
        try:
            with open(output_file, "r") as file:
                all_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            all_data = []

        # Build the structured data
        basic_structure = {
            'prompt': user_input.strip(),
            'Message': output,
            'Timesent': timesent,
            'Timerec': timerec
        }

        all_data.append(basic_structure)

        # Write the updated data back to the file
        with open(output_file, "w") as file:
            json.dump(all_data, file, indent=4)

        return render_template('index.html', response=output)

    except Exception as e:
        return render_template('index.html', message=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
