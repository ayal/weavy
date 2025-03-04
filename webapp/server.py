from flask import Flask, request, jsonify, render_template
#from rag import answer_question  # Ensure rag.py is in the same directory

def answer_question(question):
    return """
# ANSWER
I dont know
"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided.'}), 400

    answer = answer_question(question)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
