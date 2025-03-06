const { useState, useEffect } = React;

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

    return (
        <div>
            {pageData ? (
                <div>
                    <h1>{pageData.page}</h1>
                    <ReactMarkdown>{pageData.text}</ReactMarkdown>
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