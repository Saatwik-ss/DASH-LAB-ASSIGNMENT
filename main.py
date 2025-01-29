from flask import Flask, render_template, request, send_file
import json
import time
from groq import Groq
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize Groq client
client = Groq(
    api_key="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",
)
output_file = "output.json"

# Ensure the output file exists
if not os.path.exists(output_file):
    with open(output_file, "w") as file:
        json.dump([], file)


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


@app.route('/download')
def download():
    """Route to download the output.json file."""
    return send_file(output_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
