// Function to handle attachment file upload
function handleAttachmentUpload(event) {
    const fileList = event.target.files;
    const container = document.getElementById('attachment-container');
    const maxSize = 5 * 1024 * 1024; // 5 MB in bytes
  
    for (const file of fileList) {
      // Check file size
      if (file.size > maxSize) {
        alert('File size must not exceed 5 MB.');
        continue; // Skip this file
      }
  
      // Check file type
      const allowedTypes = ['jpg', 'jpeg', 'csv', 'xlsx', 'xls', 'pdf'];
      const fileType = file.name.split('.').pop().toLowerCase();
      if (!allowedTypes.includes(fileType)) {
        alert('Only JPG, JPEG, CSV, Excel, and PDF files are allowed.');
        continue; // Skip this file
      }
  
      const attachmentContainer = document.createElement('div');
      attachmentContainer.classList.add('attachment-container');
      const fileName = document.createElement('span');
      fileName.textContent = file.name;
      const crossButton = document.createElement('button');
      crossButton.innerHTML = '&times;'; // Unicode for '✖'
      crossButton.classList.add('cross-button');
      crossButton.onclick = function() {
        container.removeChild(attachmentContainer);
      };
      attachmentContainer.appendChild(fileName);
      attachmentContainer.appendChild(crossButton);
      container.appendChild(attachmentContainer);
    }
  }
  
  // Add event listener for attachment file input
  const attachmentInput = document.getElementById('attachment-input');
  attachmentInput.addEventListener('change', handleAttachmentUpload);
  