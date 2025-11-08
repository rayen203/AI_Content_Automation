# AI Content Generator  
**Génère des posts LinkedIn engageants avec Llama 3.2 local via Ollama + Image IA via Hugging Face**  
**100% privé, 100% local (texte) + IA image gratuite**  

![Demo](demo_small.gif)

---

## Fonctionnalités
- Entrez un sujet → IA génère **titre + post + hashtags + image professionnelle**
- Interface web moderne (Flask + HTML/CSS/JS)
- **Texte** : 100% local via **Ollama (Llama 3.2)**
- **Image** : Générée via **Hugging Face (modèle gratuit `FLUX.1-schnell`)**
- Copie du post en 1 clic
- Téléchargement de l’image en 1 clic
- **Zéro coût, zéro API payante**

---

## Stack Technique

| Tech | Rôle |
|------|------|
| `uv` | Gestionnaire de paquets ultra-rapide |
| `Flask` | Backend web |
| `Ollama` | IA texte locale (Llama 3.2) |
| `Hugging Face` | IA image (gratuit, `FLUX.1-schnell`) |
| `HTML/CSS/JS` | Frontend fluide & responsive |

---

## Installation & Lancement (5 min)

```bash
# 1. Clone le projet
git clone https://github.com/ton-pseudo/AI_Content_Automation.git
cd AI_Content_Automation

# 2. Crée l’environnement avec uv
uv sync

# 3. Lance Ollama (dans un autre terminal)
ollama serve

# 4. Télécharge le modèle (une seule fois)
ollama pull llama3.2

# 5. Ajoute ton token Hugging Face (gratuit)
echo "HF_TOKEN=hf_ton_token_ici" > .env

# 6. Lance l’app
uv run src/ai_content_automation/app.py