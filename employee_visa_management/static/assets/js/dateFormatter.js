// static/js/dateFormatter.js

// Function to format date
function formatDate(date, format) {
    const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    };

    const dateObj = new Date(date);

    if (format === 'd-m-Y') {
        options.day = '2-digit';
        options.month = '2-digit';
        options.year = 'numeric';
        return dateObj.toLocaleDateString('en-GB', options);
    } else if (format === 'm/d/Y') {
        options.day = '2-digit';
        options.month = '2-digit';
        options.year = 'numeric';
        return dateObj.toLocaleDateString('en-US', options);
    } else if (format === 'Y-m-d') {
        return dateObj.toISOString().split('T')[0];
    } else if (format === 'd M Y') {
        options.day = '2-digit';
        options.month = 'short';
        options.year = 'numeric';
        return dateObj.toLocaleDateString('en-GB', options);
    } else {
        // Default format
        return dateObj.toLocaleDateString('en-GB', options);
    }
}

// Function to apply date formatting to elements with the class 'date-display'
function applyDateFormat(format) {
    const dateDisplays = document.querySelectorAll('.date-display');
    dateDisplays.forEach(function (element) {
        const date = element.getAttribute('data-date');
        const formattedDate = formatDate(date, format);
        element.textContent = formattedDate;
    });
}

// Function to save date format to localStorage and apply it
function setAndApplyDateFormat(format) {
    localStorage.setItem('dateFormat', format);
    applyDateFormat(format);
}

// Event listener for date format selection
document.addEventListener('DOMContentLoaded', function () {
    const dateFormatSelect = document.getElementById('date-format');
    
    // Load and apply the saved date format on page load
    const savedFormat = localStorage.getItem('dateFormat');
    if (savedFormat) {
        applyDateFormat(savedFormat);
        if (dateFormatSelect) {
            dateFormatSelect.value = savedFormat;
        }
    }

    if (dateFormatSelect) {
        dateFormatSelect.addEventListener('change', function () {
            const selectedFormat = this.value;
            setAndApplyDateFormat(selectedFormat);
        });
    }
});
