const sessionDataElement = document.getElementById('session-data');
const sessions = JSON.parse(sessionDataElement.textContent);

const labels = sessions.map(s => s.date);
const pagesData = sessions.map(s => s.pages);

const ctx = document.getElementById('readingChart').getContext('2d');
new Chart(ctx, {
    type: 'line',
    data: {
        labels,
        datasets: [{
            label: 'Pages Read per Session',
            data: pagesData,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: { responsive: true, scales: { y: { beginAtZero: true } } }
});
