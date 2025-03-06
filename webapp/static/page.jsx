const { useState, useEffect } = React;

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

const Page = () => {
    const [pageData, setPageData] = useState(null);

    useEffect(() => {
        const queryParams = new URLSearchParams(window.location.search);
        const page = queryParams.get('page');

        if (page) {
            fetch(`/page?page=${page}`)
                .then(response => response.json())
                .then(data => setPageData(data))
                .catch(error => console.error('Error fetching page data:', error));
        }
    }, []);

    const formattedText = pageData ? fixPageFormatting(pageData.text) : null;

    return (
        <div>
            {pageData ? (
                <div>
                    <h1>{pageData.page}</h1>
                    <pre>{formattedText}</pre>
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );

};


const container = document.getElementById('root');
const root = ReactDOM.createRoot(container);
root.render(<Page />);