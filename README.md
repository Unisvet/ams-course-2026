# Course Portal: Advanced Modeling and System Simulation (AMS 2026)

> **BTU Cottbus-Senftenberg** | **Fachgebiet Drahtlose Systeme** (German) / **Chair of Wireless Systems** (English)  
> *Sommersemester 2026 Course Platform & Student Portal*

---

## 👁️ Course Vision & Purpose

The rapid integration of Deep Learning, Differentiable Computing, and Autonomous Agents is fundamentally reshaping the field of system modeling and simulation. Traditional numerical simulation engines (based on finite difference, finite element, or discrete event methods) are increasingly merging with deep learning models and agentic architectures.

**Advanced Modeling and System Simulation (AMS 2026)** bridges this gap. This course takes students on a comprehensive pedagogical journey:
* **From Classical Deterministic Modeling** (modeling continuous signal flows like RC low-pass filters)
* **To High-Performance Scientific Machine Learning (SciML)** (Physics-Informed Neural Networks, Fourier Neural Operators, and JAX-backed hardware accelerated solvers)
* **And finally, to Agentic Engineering** (constructing and orchestrating autonomous Multi-Agent Systems utilizing the Google Gemini API, local Gemma models, and professional Agent Development Environments).

By the end of this course, students will be proficient in constructing complex hybrid simulation architectures where deep mathematical models and physical equations are seamlessly controlled, evaluated, and optimized by autonomous AI agents.

---

## 🎓 Core Course Philosophies & Ideas

1. **Differentiable Physics & Mesh-Free Solvers**  
   Transitioning from grid-locked numerical solvers to mesh-free neural representations. Utilizing JAX and automatic differentiation (`jax.grad`) to evaluate physical residuals directly in loss functions.
2. **Stateless Functional Architectures**  
   Discarding classical object-oriented mutable states. Embracing purely functional programming paradigms via JAX and Flax to compile execution pipelines (`jax.jit`) and auto-vectorize simulations (`jax.vmap`) across massively-parallel GPUs/TPUs.
3. **Agent-Accelerated Workflows & Tool Calling**  
   Teaching AI agents to think like system engineers. Building systems where autonomous LLM agents leverage simulations as "Tools" (Tool Calling), perceive state changes, reason about anomalies, and rewrite architectures to achieve desired performance goals.

---

## 🗺️ Syllabus & Curriculum Journey (14 Weeks)

The course is structured into **5 distinct thematic modules** mapped over a 14-week timeline:

| Module | Weeks | Topic & Core Focus |
| :--- | :---: | :--- |
| **Module 1: Vom klassischen Modell zum Deep Learning** | Weeks 1-3 | Continuous and discrete deterministic simulations; introduction to TensorFlow/Keras, and modern development tooling (`git`, `uv`). |
| **Module 2: High-Performance Simulation & Stochastik** | Weeks 4-6 | Differentiable computing in JAX/Flax, Physics-Informed Neural Networks (PINNs), Fourier Neural Operators (FNOs), and stateless stochastics (Monte Carlo / Markov Chains). |
| **Module 3: Foundation Models & Generative KI in der Simulation** | Weeks 7-8 | Frontier LLM reasoning via the Google Gemini API (multimodal thinking) and running local Open-Weights models (Gemma). |
| **Module 4: Agentic Engineering & Orchestrierung** | Weeks 9-12 | Moving from static models to autonomous agents; utilizing the Agent Development Kit (ADK), Agent Development Environments (ADE), and Multi-Agent Systems (MAS). |
| **Module 5: Capstone-Projekt & Abschluss** | Weeks 13-14 | Collaborative final project development, hybrid system integration, live-debugging of AI hallucinations, and live project presentations. |

### 📅 Weekly Lecture Outline

* **Week 1: Einführung in Systemsimulation & Modernes Tooling**  
  Establishing simulation chains; configuring environments via Python `uv` and Git versioning.
* **Week 2: Prädiktive Modellierung & Maschinelles Lernen**  
  Building, training, and evaluating predictive deep neural networks using TensorFlow and Keras.
* **Week 3: Optimierung und Systemdynamik**  
  Discrete event modeling, queueing networks, and navigating high-dimensional loss landscapes via adaptive optimizers (Adam).
* **Week 4: Differenzierbare Simulation mit JAX & Flax**  
  Shifting to functional paradigms, JIT compilation, automatic vectorization, and XLA operator fusion.
* **Week 5: Partielle Differentialgleichungen (PDEs) neu gedacht**  
  Solving partial differential equations (Heat equation) via Physics-Informed Neural Networks (PINNs) and comparative Fourier Neural Operators (FNOs).
* **Week 6: Stochastische Simulationen im KI-Zeitalter**  
  Taming stochastic chaos with massive parallelization, Monte Carlo integrations, and stateless pseudo-random key splitting.
* **Week 7: Frontier AI: Arbeiten mit der Google Gemini API**  
  Interfacing with frontier LLMs, configuring API key protocols, implementing multimodality and native API reasoning.
* **Week 8: Open-Weights Modelle: Lokale Simulation mit Gemma**  
  Serving local, parameter-efficient models (Gemma) directly within active simulation pipelines.
* **Week 9: KI-Agenten, Tool Calling & Agenten-Skills**  
  Designing autonomous loops (Perception-Reasoning-Action) where agents invoke physics scripts as native API tools.
* **Week 10: Das Agent Development Kit (ADK)**  
  Architecting agent loops with state-tracking, execution graphs, and long-term memory management.
* **Week 11: Agent Development Environments (ADE) & Antigravity**  
  Deploying, monitoring, and debugging agentic loops under robust developer environments.
* **Week 12: Multi-Agenten-Systeme (MAS) & Komplexe Dynamiken**  
  Orchestrating agent societies with message passing, conflict resolution protocols, and market-equilibrium simulations.
* **Week 13: Projektarbeit, Hybride Architekturen & Debugging**  
  Splicing numerical engines with agentic reasoning layers; live debugging of LLM hallucinations.
* **Week 14: Projektpräsentationen (Showcase)**  
  Live demonstration, showcase, and code-review of student capstone architectures.

---

## 📈 Grading & Performance Evaluation

Student performance in AMS 2026 is evaluated continuously throughout the semester:
* **18% - Weekly Quizzes and Presentations**: Encouraging active reading and conceptual consolidation.
* **52% - Problem Sets (Programming Exercises)**: Deep-dive coding challenges implemented in JAX, Flax, and Keras.
* **30% - Capstone Final Presentation**: Designing, running, and presenting a hybrid, agent-steered system simulation.

---

## 💻 Tech Stack of this Course Portal

This platform is engineered as a lightweight, lightning-fast **Zero-Build Static Architecture with a Dynamic Javascript Router Shell**. This means updating materials requires absolutely zero bundlers or build steps.
* **Styling**: Premium, responsive dark-mode cyber-style built on Tailwind CSS.
* **Interactive Features**: Dynamic tabs (Theoretical Introduction, Infographic, Problem Set, Interactive Quiz) loaded asynchronously per week.
* **Interactive Quiz Engine**: Custom JS-driven engine loaded with randomized questions, immediate feedback, and reward badges.
* **Math & Charts**: KaTeX/MathJax for beautiful, zero-lag mathematical equations; Mermaid.js for beautiful, vector-rendered structural diagrams.
* **Branding & Localization**: Supports bilingual structures (DE & EN) and dynamic departmental linking.

---

## 🚀 Local Development (Lokal ausführen)

We use a zero-dependency Python-based server to serve files and correctly configure the MIME types for all modern web standards.

If you have the modern Python package manager **`uv`** installed, run the server with a single command:

```bash
uv run server.py
```

*This starts a local HTTP server on port 8000 and opens `http://localhost:8000` in your default browser.*

---

## 📂 Project Directory Structure

```
ams-course-2026/
├── index.html                  # Homepage (Course Syllabus and Weekly Modules Roadmap)
├── week.html                   # Dynamic Weekly Page (Intro, Infographic, Problem Set, Quiz tabs)
├── server.py                   # Lightweight Python dev server
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Pages automated CI/CD workflow
├── assets/
│   ├── css/
│   │   └── style.css           # Custom styling tokens (animations, glassmorphism, fonts)
│   └── js/
│       ├── data.js             # CENTRAL REGISTRY of weeks (edit metadata & set active: true)
│       ├── main.js             # Client-side router & dynamic tab switcher
│       └── quiz.js             # Reusable interactive quiz engine
└── weeks/
    ├── week1/                  # Week 1 Content directory
    ├── week5/                  # Week 5 Content directory (PINNs & FNOs diagrams)
    └── templates/              # Blueprint files for creating new weeks easily
```

---

## ✍️ How to Add or Activate a New Week

Adding new materials (e.g., Week 15) takes less than 2 minutes:

1. **Copy the Blueprints**:  
   Duplicate the `weeks/templates` folder and rename it (e.g., `weeks/week15`).
2. **Populate Content**:
   - `weeks/week15/introduction.html`: Summary of the topic (German).
   - `weeks/week15/introduction_en.html`: Summary of the topic (English).
   - `weeks/week15/infographic.html`: Embed custom charts, videos, or HTML/JS canvas simulations.
   - `weeks/week15/problemset.html`: Define hands-on programming tasks (English/German).
   - `weeks/week15/quiz.json`: Define localized multiple-choice quiz questions.
3. **Register the Week**:  
   Open `assets/js/data.js`, locate the target week index in the `weeksData` dictionary, and flip the active state:
   ```javascript
   active: true
   ```
4. **Push & Deploy**:  
   Commit and push your files. GitHub actions will deploy the new content automatically.

---

## 🌐 Deploying to Production

### 1. GitHub Pages (Automated & Recommended)
This repository is configured with a GitHub Actions workflow that automatically compiles and deploys the course website on every push to the `main` branch.

1. Create a repository on GitHub and push the codebase:
   ```bash
   git init
   git add .
   git commit -m "Configure AMS Course Portal"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```
2. Navigate to **Settings** -> **Pages** on your repository.
3. Under **Build and deployment** -> **Source**, select **GitHub Actions**.

The workflow in `.github/workflows/deploy.yml` will handle the rest. Your portal will be live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`.

### 2. Firebase Hosting (Google Cloud)
For high-speed, zero-cost production hosting on Google Cloud infrastructure:

1. Install Firebase CLI:
   ```bash
   npm install -g firebase-tools
   ```
2. Authenticate and initialize the hosting configurations:
   ```bash
   firebase login
   firebase init hosting
   ```
   *Select your project, define the public directory as `.` (current root), select **NO** to single-page application rewriting (to preserve static week folder paths), and deploy.*
3. Push live to Google Cloud CDN:
   ```bash
   firebase deploy
   ```
