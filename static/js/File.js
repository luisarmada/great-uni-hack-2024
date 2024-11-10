document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const fileInput = document.getElementById('file-input');
    const ageRange = document.getElementById('age-range').value;
  
    if (fileInput.files.length > 0) {
      const file = fileInput.files[0];
      console.log("File uploaded:", file);
      console.log("Age range selected:", ageRange);
  
      // Additional logic to handle the file upload and age range
      // For example, redirect to quiz page or process file content
    } else {
      alert("Please upload a file to proceed.");
    }
  });
  