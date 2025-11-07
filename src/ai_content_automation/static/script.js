document.getElementById('content-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value.trim();
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    const title = document.getElementById('title');
    const post = document.getElementById('post');
    const hashtags = document.getElementById('hashtags');
    const imageSection = document.getElementById('image-section');
    const generatedImage = document.getElementById('generated-image');
    const downloadBtn = document.getElementById('download-img');

    // === RESET SÉCURISÉ ===
    result.classList.add('hidden');
    if (imageSection) imageSection.style.display = 'none';
    if (generatedImage) generatedImage.style.display = 'none';
    if (downloadBtn) downloadBtn.style.display = 'none';
    loading.classList.remove('hidden');
    title.textContent = post.textContent = '';
    hashtags.innerHTML = '';

    try {
        const res = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });

        const data = await res.json();

        if (data.error) {
            alert("Erreur : " + data.error);
            console.error("Raw response:", data);
            return;
        }

        // === AFFICHAGE TEXTE ===
        title.textContent = data.title;
        post.textContent = data.post;
        data.hashtags.forEach(tag => {
            const li = document.createElement('li');
            li.textContent = tag;
            hashtags.appendChild(li);
        });

        // === AFFICHAGE IMAGE SÉCURISÉ ===
        if (data.image_url && generatedImage && downloadBtn && imageSection) {
            generatedImage.src = data.image_url + "?t=" + Date.now();
            generatedImage.style.display = 'block';
            downloadBtn.style.display = 'block';
            imageSection.style.display = 'block';
        }

        result.classList.remove('hidden');
        document.getElementById('prompt').value = '';

    } catch (err) {
        console.error("Erreur réseau :", err);
        alert("Erreur réseau. Vérifie Flask et Ollama.");
    } finally {
        loading.classList.add('hidden');
    }
});

// === COPIER LE POST ===
document.getElementById('copy-post').addEventListener('click', () => {
    const text = document.getElementById('post').textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert("Post copié !");
    }).catch(() => {
        alert("Échec copie. Sélectionne manuellement.");
    });
});

// === TÉLÉCHARGER L’IMAGE (SÉCURISÉ) ===
const downloadBtn = document.getElementById('download-img');
if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
        const img = document.getElementById('generated-image');
        if (img && img.src) {
            const a = document.createElement('a');
            a.href = img.src;
            a.download = 'linkedin_post_image.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
    });
}