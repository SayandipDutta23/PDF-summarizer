import PyPDF2
import openai
from flask import Flask, render_template, request

from secret_key import openai_key  # Import your OpenAI API key

app = Flask(__name__)

# Set up OpenAI API
openai.api_key = openai_key


# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    # Get the uploaded PDF file from the request
    pdf_file = request.files['pdf_file']

    # Save the uploaded PDF file
    pdf_path = 'uploads/' + pdf_file.filename
    pdf_file.save(pdf_path)

    # Extract text from the PDF file
    pdf_text = extract_text_from_pdf(pdf_path)

    # Limit the prompt length to fit within the model's maximum context length
    prompt = pdf_text[:2000]  # Adjust the number of characters as needed

    # Use the OpenAI API to generate a summary of the PDF content
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100,  # Adjust the maximum number of tokens for the generated summary
        temperature=0.3,  # Adjust the temperature parameter for generating diverse summaries
        n=1,  # Number of responses to generate
        stop=None,  # Optional stop sequence to end the summary
    )

    # Extract the generated summary from the API response
    summary = response.choices[0].text.strip()

    # Render the summary in the template
    return render_template('index.html', summary=summary)


if __name__ == '__main__':
    app.run(debug=True)
