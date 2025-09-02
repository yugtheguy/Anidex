
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const uploadBtn = document.getElementById('uploadBtn');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const submitBtn = document.getElementById('submitBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const resultImage = document.getElementById('resultImage');
const animalName = document.getElementById('animalName');
const animalInfo = document.getElementById('animalInfo');
const uploadAnotherBtn = document.getElementById('uploadAnotherBtn');

let selectedFile = null;

// Upload area click
uploadArea.addEventListener('click', () => {
    imageInput.click();
});

uploadBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    imageInput.click();
});

// File input change
imageInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        handleFileSelect(file);
    }
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        handleFileSelect(file);
    }
});

function handleFileSelect(file) {
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewSection.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// Submit button
submitBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Show loading
    previewSection.style.display = 'none';
    loadingSection.style.display = 'block';
    
    try {
        const formData = new FormData();
        formData.append('image', selectedFile);
        
        const response = await fetch('http://localhost:8000/api/anidex/upload/', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            alert('Error: ' + (data.error || 'Upload failed'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        loadingSection.style.display = 'none';
    }
});

function displayResults(data) {
    // Set image
    resultImage.src = data.image_url;
    
    // Set animal name
    animalName.textContent = data.predicted_animal;
    
    // Set animal info
    animalInfo.innerHTML = '';
    
    if (data.animal_info) {
        const info = data.animal_info;
        
        // Basic info
        if (info.name) {
            addInfoItem('Name', info.name);
        }
        
        if (info.characteristics) {
            const chars = info.characteristics;
            
            if (chars.scientific_name) {
                addInfoItem('Scientific Name', chars.scientific_name);
            }
            
            if (chars.habitat) {
                addInfoItem('Habitat', chars.habitat);
            }
            
            if (chars.diet) {
                addInfoItem('Diet', chars.diet);
            }
            
            if (chars.lifespan) {
                addInfoItem('Lifespan', chars.lifespan);
            }
            
            if (chars.weight) {
                addInfoItem('Weight', chars.weight);
            }
            
            if (chars.top_speed) {
                addInfoItem('Top Speed', chars.top_speed);
            }
            
            if (chars.slogan) {
                addInfoItem('Fun Fact', chars.slogan);
            }
        }
        
        if (info.locations && info.locations.length > 0) {
            addInfoItem('Location', info.locations.join(', '));
        }
    } else {
        animalInfo.innerHTML = '<p>No additional information available</p>';
    }
    
    resultsSection.style.display = 'block';
}

function addInfoItem(label, value) {
    const item = document.createElement('div');
    item.className = 'info-item';
    item.innerHTML = `<span class="info-label">${label}:</span> ${value}`;
    animalInfo.appendChild(item);
}

// Upload another button
uploadAnotherBtn.addEventListener('click', () => {
    // Reset everything
    selectedFile = null;
    imageInput.value = '';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    uploadArea.style.display = 'block';
});