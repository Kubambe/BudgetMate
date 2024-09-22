// Search functionality for expenses
document.getElementById('search').addEventListener('keyup', function() {
    const searchValue = this.value.toLowerCase();
    const items = document.querySelectorAll('.expense-item');

    items.forEach(item => {
        if (item.textContent.toLowerCase().includes(searchValue)) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });
});

// Chart.js for dynamic charts
const ctx = document.getElementById('expenseChart').getContext('2d');
const expenseChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [/* Categories */],
        datasets: [{
            label: 'Expenses',
            data: [/* Data Points */],
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Notification styling
function showNotification(message, type) {
    const alertPlaceholder = document.getElementById('alert-placeholder');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerText = message;
    alertPlaceholder.append(alert);
    setTimeout(() => {
        alert.remove();
    }, 3000);
}
