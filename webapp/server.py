print("**************\n\nRUN ME WITH:\n\npython -m webapp.server!!!\n\n**************")
from flask import Flask, request, jsonify, render_template
from rag import do_rag

app = Flask(__name__)

def answer_question(question):
    rag_result = do_rag(question, 3)
    answer = rag_result["completion_msg"].content
    context = rag_result["articles"]
    return {"answer": answer, "context": context}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided.'}), 400

    result = answer_question(question)

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)