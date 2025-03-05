from flask import Flask, request, jsonify, render_template
from weavy.rag import do_rag
import json

def answer_question(question):
    rag_result=do_rag(question, 3)
    response=rag_result["completion_msg"].content
    response+="\n\nAdditional References:\n\n"
    response+=json.dumps(rag_result["articles"], indent=2).replace("\n", "<br>").replace(" ", "&nbsp;")
    return response

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
