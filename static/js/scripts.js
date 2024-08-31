document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/vikram-samvat-date')
        .then(response => response.json())
        .then(data => {
            // Access the date parts from the response
            const dateParts = data.lines;

            // Display the date parts in respective divs
            document.getElementById('line1').textContent = dateParts[0] || "Date not found";
            document.getElementById('line2').textContent = dateParts[1] || "Date not found";
            document.getElementById('line3').textContent = dateParts[2] || "Date not found";
            document.getElementById('line4').textContent = dateParts[3] || "Location not found";
        })
        .catch(error => {
            console.error('Error fetching date:', error);
        });
});
