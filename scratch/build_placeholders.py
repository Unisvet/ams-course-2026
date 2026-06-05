import os
import json

weeks_dir = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks"

# Quiz questions and answers for each week
week_quizzes = {
    2: [
        {
            "question": "Welches Keras 3-Backend wird in diesem Kurs für pure funktionale Berechnungen und XLA-Kompilierung verwendet?",
            "options": [
                "NumPy",
                "PyTorch",
                "JAX",
                "TensorFlow"
            ],
            "answerIndex": 2,
            "explanation": "JAX ist das primäre Backend für funktionale Reinheit, automatische Differentiation und hardwarebeschleunigte XLA-Kompilierung im Verlauf dieses Kurses."
        },
        {
            "question": "Wie wird das Keras 3 Backend vor dem Laden der Bibliothek konfiguriert?",
            "options": [
                "Per Umgebungsvariable 'KERAS_BACKEND'",
                "Über die Funktion keras.set_backend()",
                "In der pyproject.toml Konfigurationsdatei",
                "Gar nicht, es wird zur Laufzeit automatisch geraten"
            ],
            "answerIndex": 0,
            "explanation": "Das Backend muss über die Umgebungsvariable 'KERAS_BACKEND' (z.B. mittels os.environ) vor dem ersten Keras-Import gesetzt werden."
        }
    ],
    3: [
        {
            "question": "Welcher Ansatz wird in diesem Modul verwendet, um kontinuierliche Differentialgleichungen diskret zu approximieren?",
            "options": [
                "Runge-Kutta-Verfahren",
                "Explizites Euler-Verfahren",
                "Heun-Verfahren",
                "Verlet-Integration"
            ],
            "answerIndex": 1,
            "explanation": "Das explizite Euler-Verfahren ist die einfachste diskrete Approximation von zeitlich kontinuierlichen Differentialgleichungen."
        },
        {
            "question": "Welche Verlustfunktion wird typischerweise für die Rekonstruktions-Fehlerberechnung in Autoencodern zur Anomalieerkennung verwendet?",
            "options": [
                "Cross-Entropy",
                "Binary Cross-Entropy",
                "Mean Absolute Error (MAE) oder Mean Squared Error (MSE)",
                "Hinge Loss"
            ],
            "answerIndex": 2,
            "explanation": "MAE (L1-Loss) und MSE (L2-Loss) eignen sich hervorragend, um Abweichungen zwischen dem Originalsignal und der neuronalen Rekonstruktion zu messen."
        }
    ],
    4: [
        {
            "question": "Was bewirkt die JAX-Transformation `vmap`?",
            "options": [
                "Sie optimiert den Code für spezifische CPUs",
                "Sie führt automatische Vorwärts-Differentiation durch",
                "Sie vektorisiert eine Funktion über eine Batch-Dimension, ohne manuelle Python-Schleifen zu schreiben",
                "Sie kompiliert den Code mittels XLA direkt in Maschinencode"
            ],
            "answerIndex": 2,
            "explanation": "`vmap` steht für 'vectorized map' und ermöglicht die vollautomatische parallele Ausführung einer mathematischen Funktion über Arrays."
        },
        {
            "question": "Warum ist die erste Ausführung einer mit `@jax.jit` dekorierten Funktion langsamer als nachfolgende Aufrufe?",
            "options": [
                "Weil JAX die Daten im Speicher kopieren muss",
                "Aufgrund des Kompilierungs- und Tracing-Vorgangs des XLA-Compilers beim ersten Durchlauf",
                "Weil der Garbage Collector den Speicher bereinigt",
                "Das ist ein bekanntes Performance-Problem in JAX"
            ],
            "answerIndex": 1,
            "explanation": "Beim ersten Aufruf analysiert JAX die Dimensionen und Typen (Tracing) und generiert den optimierten XLA-Code. Nachfolgende Aufrufe nutzen den vorkompilierten Maschinen-Code."
        }
    ],
    5: [
        {
            "question": "Wofür steht die Abkürzung PINN im Kontext neuronaler Differentialgleichungen?",
            "options": [
                "Physics-Integrated Neural Network",
                "Partial Integration Neural Network",
                "Physics-Informed Neural Network",
                "Predictive Interpolation Neural Network"
            ],
            "answerIndex": 2,
            "explanation": "PINN steht für Physics-Informed Neural Networks, bei denen physikalische Gesetzmäßigkeiten (wie PDEs) direkt als Strafterm in die Verlustfunktion des Netzes einfließen."
        },
        {
            "question": "Welche Aktivierungsfunktion wird typischerweise in PINNs verwendet, um kontinuierliche Ableitungen zu ermöglichen?",
            "options": [
                "ReLU",
                "Tanh (Tangens Hyperbolicus)",
                "Sigmoid",
                "Linear"
            ],
            "answerIndex": 1,
            "explanation": "Die Tanh-Aktivierungsfunktion ist unendlich stetig differenzierbar, was für die Berechnung von Ableitungen höherer Ordnung (z.B. zweite räumliche Ableitung bei Wärmeleitung) unabdingbar ist."
        }
    ]
}

week_titles = {
    2: "Prädiktive Modellierung & Maschinelles Lernen",
    3: "Optimierung und Systemdynamik",
    4: "Differenzierbare Simulation mit JAX & Flax",
    5: "Partielle Differentialgleichungen (PDEs) neu gedacht"
}

week_descriptions = {
    2: "In dieser Woche erlernen wir das Fundament datengetriebener Modellierung. Wir betrachten, wie kontinuierliche physikalische Signale erfasst und als neuronale Netze abgebildet werden können.",
    3: "Optimierungsprobleme sind das Herzstück der Systemdynamik. Wir vergleichen klassische iterative Optimierungsverfahren mit modernen, KI-gestützten Repräsentationen.",
    4: "Der Übergang zu JAX und Flax revolutioniert die Rechengeschwindigkeit. Wir nutzen automatische Differentiation, Vektorisierung und Just-In-Time (JIT) Kompilierung auf GPUs.",
    5: "Physikalische Gesetze lassen sich direkt in neuronale Netzwerke einbetten. Wir betrachten Physics-Informed Neural Networks (PINNs) zur lösung von Wärmeleitungsgleichungen."
}

# Load template contents
with open(os.path.join(weeks_dir, "templates", "introduction.html"), 'r', encoding='utf-8') as f:
    intro_template = f.read()

with open(os.path.join(weeks_dir, "templates", "infographic.html"), 'r', encoding='utf-8') as f:
    info_template = f.read()

for w_id in [2, 3, 4, 5]:
    week_folder = os.path.join(weeks_dir, f"week{w_id}")
    os.makedirs(week_folder, exist_ok=True)
    
    # 1. Write introduction.html
    title = week_titles[w_id]
    desc = week_descriptions[w_id]
    intro_html = intro_template.replace("weeks/weekX/cover.png", f"weeks/week{w_id}/cover.png")
    intro_html = intro_html.replace("Thematischer Schwerpunkt dieser Woche", title)
    intro_html = intro_html.replace("Schreibe hier eine kurze Zusammenfassung (2-3 Sätze) über die theoretischen Grundlagen und die Praxisrelevanz des Themas der Woche.", desc)
    intro_html = intro_html.replace("Erstes wichtiges Lernziel dieser Woche.", "Verständnis der theoretischen Grundlagen und mathematischen Modelle.")
    intro_html = intro_html.replace("Zweites wichtiges Lernziel dieser Woche.", "Praktische Umsetzung in Python unter Nutzung moderner Simulationstools.")
    
    intro_out_path = os.path.join(week_folder, "introduction.html")
    with open(intro_out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(intro_html)
        
    # 2. Write infographic.html
    info_html = info_template.replace("Visualisierung der wöchentlichen Daten", f"Visualisierung - Woche {w_id}")
    info_html = info_html.replace("templateChart", f"chartW{w_id}")
    
    # Customize Chart.js labels depending on the week
    if w_id == 2:
        info_html = info_html.replace("['Modul 1', 'Modul 2', 'Modul 3', 'Modul 4']", "['Training-Loss', 'Val-Loss', 'Test-Loss']")
        info_html = info_html.replace("[100, 50, 25, 0]", "[0.8, 0.45, 0.46]")
        info_html = info_html.replace("Fortschritt der Themen (%)", "Modellfehler (MSE)")
    elif w_id == 3:
        info_html = info_html.replace("['Modul 1', 'Modul 2', 'Modul 3', 'Modul 4']", "['Wartezeit', 'Serverlast', 'Durchsatz']")
        info_html = info_html.replace("[100, 50, 25, 0]", "[12.5, 78.4, 94.1]")
        info_html = info_html.replace("Fortschritt der Themen (%)", "Metriken (Auslastung & Performance)")
    elif w_id == 4:
        info_html = info_html.replace("['Modul 1', 'Modul 2', 'Modul 3', 'Modul 4']", "['NumPy (CPU)', 'JAX (CPU)', 'JAX (GPU compiled)']")
        info_html = info_html.replace("[100, 50, 25, 0]", "[100, 15, 0.02]")
        info_html = info_html.replace("Fortschritt der Themen (%)", "Relative Rechenzeit (weniger ist besser)")
    elif w_id == 5:
        info_html = info_html.replace("['Modul 1', 'Modul 2', 'Modul 3', 'Modul 4']", "['FDM (Mesh)', 'FEM (Grid)', 'PINN (Surrogate)']")
        info_html = info_html.replace("[100, 50, 25, 0]", "[85, 92, 98]")
        info_html = info_html.replace("Fortschritt der Themen (%)", "Modellflexibilität bei Randwertänderungen")
        
    info_out_path = os.path.join(week_folder, "infographic.html")
    with open(info_out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(info_html)
        
    # 3. Write quiz.json
    quiz_out_path = os.path.join(week_folder, "quiz.json")
    with open(quiz_out_path, 'w', encoding='utf-8') as out_f:
        json.dump(week_quizzes[w_id], out_f, indent=4, ensure_ascii=False)
        
    print(f"Generated placeholders for week {w_id} (intro, info, quiz)")
