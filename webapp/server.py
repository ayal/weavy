print("**************\n\nRUN ME WITH:\n\npython -m webapp.server!!!\n\n**************")
from flask import Flask, request, jsonify, render_template
from rag import do_rag
import json

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

# http://host.com/book?page={page}
@app.route('/book')
def page():
    return render_template('page.html')

# api for getting the page data from output_pages dir json folder
# files are page_1.json, page_2.json, page_3.json
@app.route('/page')
def get_page():
    page = request.args.get('page')
    if not page:
        return jsonify({'error': 'No page provided.'}), 400

    try:
        with open(f'output_pages/page_{page}.json') as f:
            data = json.load(f)
    except FileNotFoundError:
        return jsonify({'error': 'Page not found.'}), 404

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)