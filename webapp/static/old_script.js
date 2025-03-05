document.getElementById('questionForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitButton = document.querySelector('#questionForm button[type="submit"]');
    const originalButtonText = submitButton.innerHTML;
    submitButton.innerHTML = 'Loading...';
    submitButton.disabled = true;

    const question = document.getElementById('question').value;
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
    });

    const data = await response.json();

    submitButton.innerHTML = originalButtonText;
    submitButton.disabled = false;

    if (response.ok) {
        let html = marked.parse(data.answer);
        html += '<h3>Additional References:</h3><ul>';
        // todo: why Article? fix this
        data.context.Article.forEach(article => {
            html += `<li><strong>${article.content}</strong><br><a href=\"${article.url}\" target=\"_blank\">${article.url}</a></li>`;
        });
        html += '</ul>';
        document.getElementById('answer').innerHTML = html;
    } else {
        document.getElementById('answer').textContent = data.error;
    }
});