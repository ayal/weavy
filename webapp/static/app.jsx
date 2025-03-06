import React, { StrictMode, useState, useEffect, } from "https://esm.sh/react";
import { createRoot } from "https://esm.sh/react-dom/client";
import ReactMarkdown from 'https://esm.sh/react-markdown'
import rehypeRaw from "https://esm.sh/rehype-raw";
import remarkGfm from "https://esm.sh/remark-gfm";
import remarkBreaks from "https://esm.sh/remark-breaks";

const fixPageFormatting = (text) => {
    // Find chapter patterns and fix:
    // For example: 9\n\nC\nH\nA\nP\nT\nE\nR\n2\n\nP\nr\no\nm\no\nt\ni\nn\ng\nG\no\o\nd\nH\ne\na\nl\nt\nh\n\n
    // Extract chapter number and title
    const chapterPattern = /(\d+)\n\nC\nH\nA\nP\nT\nE\nR\n(\d+)\n\n(.*?)\n\n/gims;
    return text.replace(chapterPattern, (match, p1, p2, p3) => {
        const chapterTitle = p3.replace(/\n/g, '');
        return `Chapter ${p2}: ${chapterTitle}\n\n`;
    });
};

const ArticleReference = ({ content, url, page }) => {
    const [open, setOpen] = useState(false);

    return (
        <div className="border-b border-gray-200 py-2">
            <div className="flex justify-between items-center w-full text-left font-medium text-gray-800 hover:text-blue-600">
                <span>Page: {page}</span>
                <button onClick={() => setOpen(!open)} className="ml-2">
                    <span>{open ? '▲' : '▼'}</span>
                </button>
            </div>
            <a href={url} target="_blank" rel="noopener noreferrer" className="block break-words text-blue-600 mt-1">
                {url}
            </a>
            {open && (
                <div className="mt-2 pl-4">
                    <pre className="text-gray-600 mb-2 whitespace-pre-wrap">{fixPageFormatting(content)}</pre>
                </div>
            )}
        </div>
    );
};


const SuggestedQuestion = ({ question, onSelect }) => (
    <button
        onClick={() => onSelect(question)}
        className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-xl text-gray-700 text-sm"
    >
        {question}
    </button>
);

const QuestionForm = () => {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const suggestedQuestions = [
        "tx for meningitis",
        "What do you know about meningitis?",
        "Show relevant protocol for meningitis treatment",
    ];

    const handleSubmit = async (e, selectedQuestion) => {
        if (e) e.preventDefault();
        const query = selectedQuestion || question;

        setQuestion(query);
        setLoading(true);
        setError(null);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: query }),
            });

            const data = await response.json();

            if (response.ok) {
                setAnswer(data.answer);
                setArticles(data.context.Article || []);
            } else {
                setError(data.error || 'An unknown error occurred.');
                setAnswer('');
                setArticles([]);
            }
        } catch (err) {
            setError(err.message);
            setAnswer('');
            setArticles([]);
        }

        setLoading(false);
    };

    if (answer) {
        console.log('answer is:\n\n', answer);
    }

    return (
        <div className="max-w-2xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-2xl">
            <div>

            </div>
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Ask your question..."
                    required
                    className="px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    type="submit"
                    disabled={loading}
                    className={`px-4 py-2 font-semibold text-white rounded-xl transition-colors duration-300 flex justify-center items-center ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-600'
                        }`}
                >
                    {loading ? (
                        <span className="inline-block h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                    ) : (
                        'Submit'
                    )}
                </button>
            </form>

            <div className="mt-4">
                <h4 className="font-medium text-gray-700 mb-2">Suggested Questions:</h4>
                <div className="flex gap-2 flex-wrap">
                    {suggestedQuestions.map((q, idx) => (
                        <SuggestedQuestion key={idx} question={q} onSelect={(q) => handleSubmit(null, q)} />
                    ))}
                </div>
            </div>

            {error && <p className="mt-4 text-red-500 font-medium">{error}</p>}

            {answer && (
                <div id="answer" className="mt-6 prose prose-blue">
                    <div>
                        <ReactMarkdown
                            remarkPlugins={[remarkGfm, remarkBreaks]}
                            rehypePlugins={[rehypeRaw]}
                            
                        >
                            {answer}
                        </ReactMarkdown>
                    </div>

                    {articles.length > 0 && (
                        <div className="mt-6">
                            <h3 className="text-lg font-semibold mb-2">Additional References:</h3>
                            <div className="max-h-48 overflow-y-auto">
                                {articles.map((article, idx) => (
                                    <ArticleReference
                                        key={idx}
                                        content={article.content}
                                        page={article.page}
                                        url={`/book?page=${article.page}`}
                                    />
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};


const container = document.getElementById('root');
const root = createRoot(container);
root.render(<QuestionForm />);