// Function to handle form submission and field validation
function validateForm(event) {
  event.preventDefault(); // Prevent form submission
  const form = document.getElementById('work-request-form');
  const fields = form.querySelectorAll('.custom-input, .remarks-textarea'); // Updated selector for textareas
  
  let isFormValid = true; // Flag to track overall form validity
  
  // Iterate through each field
  fields.forEach(field => {
    const fieldValue = field.value.trim();
    const fieldLabel = field.previousElementSibling.textContent; // Get the label text
    const errorContainer = field.closest('.form-group').querySelector('.error-message');

    // If field value is empty
    if (!fieldValue) {
      // Show error message
      errorContainer.textContent = `${fieldLabel} is required`;
      errorContainer.style.color = 'red';
      isFormValid = false; // Set flag to false as at least one field is empty
    } else {
      // Clear error message if field value is not empty
      errorContainer.textContent = '';
    }
  });

  // Check if the form is valid and submit it if so
  if (isFormValid) {
    form.submit();
  }
}

// Add event listener for form submission on submit button click
const submitButton = document.querySelector('#work-request-form button[type="submit"]');
submitButton.addEventListener('click', validateForm);
