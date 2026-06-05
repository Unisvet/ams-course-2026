# Course Website: Advanced Modeling and System Simulation (AMS)

This is a modern, high-end, responsive course portal for the BTU course **Advanced Modeling and System Simulation**. It utilizes a zero-build static architecture with a dynamic shell, meaning you can easily update the course content, preview it locally using `uv`, and host it directly on GitHub Pages.

---

## 🚀 Local Development (Lokal ausführen)

We use a zero-dependency Python server. If you have the Python package manager **`uv`** installed, run the server with a single command:

```bash
uv run server.py
```

*This will start a local HTTP server on port 8000 and automatically open your default browser to `http://localhost:8000`.*

---

## 📂 Project Structure (Projektstruktur)

```
ams-course-2026/
├── index.html                  # Homepage (Course Syllabus and Weekly Modules Roadmap)
├── week.html                   # Dynamic Weekly Page (Intro, Infographic, Problem Set, Quiz tabs)
├── server.py                   # Lightweight Python dev server
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow for auto-deployment
├── assets/
│   ├── css/
│   │   └── style.css           # Custom styling tokens (colors, animations, glassmorphism)
│   └── js/
│       ├── data.js             # CENTRAL REGISTRY for all 14 weeks (edit titles and active states here!)
│       ├── main.js             # Shell router (loads sub-pages, tabs switching)
│       └── quiz.js             # Reusable interactive quiz engine (German UI)
└── weeks/
    ├── week1/                  # Week 1 Content folder
    ├── week7/                  # Week 7 Content folder (with your custom charts infographic!)
    └── templates/              # Blueprints for creating new weeks
```

---

## ✍️ How to Add a New Week (Neue Woche hinzufügen)

Adding new materials (e.g., Week 8) takes less than 2 minutes and requires no programming:

1. **Copy the Templates**: 
   Duplicate the `weeks/templates` folder and name it `weeks/week8`.
2. **Edit the Files**:
   - `weeks/week8/introduction.html`: Write a short summary of the week's topic in German.
   - `weeks/week8/infographic.html`: Embed interactive charts, videos, or HTML/JS widgets (Tailwind and Chart.js are preloaded!).
   - `weeks/week8/problemset.html`: Define programming assignments in English (code blocks will have automatic copy buttons!).
   - `weeks/week8/quiz.json`: Define German multiple-choice questions, options, and explanations.
3. **Register the Week**:
   Open `assets/js/data.js`, locate `"8": { ... }` in the `weeksData` registry, and change:
   ```javascript
   active: true
   ```
4. **Push to GitHub**: Save and push. The site will automatically update!

---

## 🌐 Deployment (Veröffentlichung)

### 1. GitHub Pages (Empfohlen)
This project is configured with a GitHub Action that automatically deploys the website to GitHub Pages every time you push to the `main` branch.

**Setup Instructions**:
1. Push this folder to a new repository on GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```
2. On GitHub, navigate to **Settings** -> **Pages**.
3. Under **Build and deployment** -> **Source**, select **GitHub Actions**.
4. The workflow in `.github/workflows/deploy.yml` will automatically build and publish the site. It is live at `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`.

### 2. Google Cloud (Firebase Hosting)
For hosting later on Google Cloud, **Firebase Hosting** is the easiest and cheapest option (completely free for course-level traffic).

**Setup Instructions**:
1. Install Firebase CLI locally:
   ```bash
   npm install -g firebase-tools
   ```
2. Log in and initialize:
   ```bash
   firebase login
   firebase init hosting
   ```
   *Choose "Use an existing project" or create a new one. Set the public directory to `.` (the current folder), configure as a single-page app if desired (select NO so standard routing works), and set up automatic GitHub builds if prompted.*
3. Deploy to production:
   ```bash
   firebase deploy
   ```
