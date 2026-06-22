import csv

# Shortened version matching character constraints (Question: <=120, Answer options: <=75)
# Includes original 12 questions shortened plus 2 new interesting and hard questions.
quiz_data = [
    {
        "question": "Was ist das Hauptziel von 'Edge AI' in der industriellen Systemsimulation?",
        "options": [
            "Auslagerung der Simulation auf Cloud-Server zur Kosteneinsparung.",
            "Schutz der Datensouveränität und Vermeidung von Netzwerklatenzen.",
            "Automatische Erstellung von PowerPoint-Folgen über Multimodalität.",
            "Beschleunigung von JAX über stochastische Monte-Carlo-Methoden."
        ],
        "correct": "2"
    },
    {
        "question": "Wie wird der Gedankenkanal (Thought Channel) bei Gemma 4 nativ aktiviert und isoliert?",
        "options": [
            "Durch Anhängen von 'import thought' im Python-Code.",
            "Durch '<|think|>' am Start der System-Message & anschließendes Parsing.",
            "Durch die automatische Generierung eines Git-Commits über die Colab CLI.",
            "Durch Festlegen der Ankunftsrate λ in einer diskreten Ereignissimulation."
        ],
        "correct": "2"
    },
    {
        "question": "Warum ist der Wechsel von Cloud-APIs zu lokalen Open-Weights-Modellen bei uns entscheidend?",
        "options": [
            "Um das WLAN im Werk zu entlasten",
            "Da Latenzen schwanken & sensible Telemetriedaten lokal bleiben müssen",
            "Da Cloud-Modelle keine komplexen stochastischen Gleichungen lösen können",
            "Weil Gemma 4 cloudbasierte Modelle grundsätzlich in jeder Disziplin schlägt"
        ],
        "correct": "2"
    },
    {
        "question": "Was verleiht dem Gemma 4 E2B-Modell (2,3B Parameter) seine hohe logische Leistung am Edge?",
        "options": [
            "Mixture-of-Experts (MoE) Routing",
            "Ein unendlich großes Context Window (Transformer-XL)",
            "Per-Layer Embeddings (PLE)",
            "LSTM-Rückkopplungsschleifen auf Hardware-Ebene"
        ],
        "correct": "3"
    },
    {
        "question": "Wie wird der kognitive Denkmodus (Thought Mode) bei Gemma 4 nativ aufgerufen und vom restlichen Text abgegrenzt?",
        "options": [
            "Durch den simplen Text-Prompt 'Denke Schritt für Schritt'",
            "Über <|think|> am Anfang und Begrenzer <|channel>thought & <channel|>",
            "Über ein externes Python-Skript, das den Text pausiert",
            "Durch Erhöhung der Temperature-Variable der Inferenz-Engine auf 1.5"
        ],
        "correct": "2"
    },
    {
        "question": "Auswirkung, wenn alte Gedanken (<|channel>thought) im Multi-Turn-Chat in der Historie verbleiben?",
        "options": [
            "Das Modell wird schlauer, da es mehr Kontext hat",
            "Token-Wachstum explodiert & alte Logikzweige überladen das Modell.",
            "Die GPU stürzt sofort mit einem OutOfMemory-Error (OOM) ab",
            "Es hat keinerlei Auswirkungen auf die Inferenz"
        ],
        "correct": "2"
    },
    {
        "question": "Warum nutzen wir PyTorch statt JAX für lokale Textgenerierung trotz JAX' Simulations-Performance?",
        "options": [
            "Weil JAX grundsätzlich keine Textdaten verarbeiten kann",
            "PyTorch meistert dynamische Längen ohne ständiges XLA-Rekompilieren.",
            "Weil Google JAX komplett aus dem Open-Source-Angebot genommen hat",
            "Um die Lizenzkosten von JAX zu sparen"
        ],
        "correct": "2"
    },
    {
        "question": "Wie hilft uns offline Retrieval-Augmented Generation (RAG) konkret in unserem Wächter-System?",
        "options": [
            "Es erlaubt dem Agenten, das Internet nach Lösungen zu durchsuchen",
            "Es wandelt Textbefehle blitzschnell in Bilder um",
            "Es injiziert situationsbezogene Arbeitsanweisungen (SOPs) in den Prompt.",
            "Es komprimiert die Gewichte des Modells, um VRAM zu sparen"
        ],
        "correct": "3"
    },
    {
        "question": "Welchen strategischen Vorteil bietet uns die Google Colab CLI (google-colab-cli) in unserem autonomen Edge-Workflow?",
        "options": [
            "Sie macht unsere lokalen Laptop-GPUs durch Übertaktung doppelt so schnell",
            "Wir lagern Fine-Tuning in die Cloud aus & ziehen Gewichte lokal zurück.",
            "Sie ersetzt Git und GitHub vollständig",
            "Sie umgeht den Kaggle-Login für proprietäre Modelle"
        ],
        "correct": "2"
    },
    {
        "question": "Was geschieht in der DiscreteFoundry-Simulation, wenn Ankunftsrate (Poisson) > Service-Rate?",
        "options": [
            "Das System erreicht von selbst ein magisches, stabiles Gleichgewicht",
            "Die Maschine wird physikalisch heißer und schaltet ab",
            "Puffer läuft voll und es kommt zu Überläufen (Ausschuss/Dropped Parts).",
            "Die Simulation dividiert durch Null und bricht mit einem Python-Fehler ab"
        ],
        "correct": "3"
    },
    {
        "question": "Warum muss das LLM seine Entscheidung im Format 'NEW_SERVICE_RATE: 3.0' ausgeben?",
        "options": [
            "Weil das Modell sonst nur in Gedichten und Metaphern antwortet",
            "Für sichere numerische Extraktion via RegEx & Einspeisung als Float.",
            "Dies ist eine unveränderliche Eigenart der Gemma-Architektur.",
            "Um die Token-Anzahl bei der Ausgabe künstlich in die Höhe zu treiben"
        ],
        "correct": "2"
    },
    {
        "question": "Prinzipien der 'Festung der Autarkie' (Lokaler Wächter) unseres Neo-Simulacrums? (Mehrfachauswahl)",
        "options": [
            "Absolute Datensouveränität und Offline-Fähigkeit",
            "Globale Mutable States in der Simulation",
            "Verwendung von Cloud-APIs für kritische Echtzeitentscheidungen",
            "Ausführung von Open-Weights Modellen direkt auf der Edge-Hardware"
        ],
        "correct": "1,4"
    },
    {
        "question": "Warum halbiert eine konstante Servicezeit (M/D/1) die Warteschlange im Vergleich zu stochastischen Zeiten (M/M/1)?",
        "options": [
            "Weil die Varianz der Servicezeiten eliminiert wird (Varianz = 0).",
            "Weil deterministische Systeme keine Pufferüberläufe verursachen.",
            "Weil die Ankunftsrate lambda bei M/D/1 automatisch konstant wird.",
            "Weil der XLA-Compiler deterministische Graphen 2x schneller berechnet."
        ],
        "correct": "1"
    },
    {
        "question": "Wie verhindert ein robuster Edge-Agent einen Systemausfall, wenn das Regex-Parsing der Steuerbefehle fehlschlägt?",
        "options": [
            "Er fällt auf einen vordefinierten Sicherheitswert (Fallback-Wert) zurück.",
            "Er startet die gesamte Hardwaresimulation und das Edge-OS neu.",
            "Er sendet eine Notfall-API-Anfrage an ein externes Cloud-Modell.",
            "Er überspringt den Zeitschritt und behält die ungültigen Parameter bei."
        ],
        "correct": "1"
    }
]

headers = [
    "Question (max 120 chars)",
    "Answer 1 (max 75 chars)",
    "Answer 2 (max 75 chars)",
    "Answer 3 (max 75 chars)",
    "Answer 4 (max 75 chars)",
    "Time limit (sec)",
    "Correct answer(s)"
]

output_file = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\docs\quiz-ams08-2026.csv"

# Validate limits before writing
for i, q in enumerate(quiz_data, 1):
    assert len(q["question"]) <= 120, f"Q{i} question too long: '{q['question']}' ({len(q['question'])} chars)"
    for j, opt in enumerate(q["options"], 1):
        assert len(opt) <= 75, f"Q{i} Option A{j} too long: '{opt}' ({len(opt)} chars)"

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(headers)
    for q in quiz_data:
        row = [
            q["question"],
            q["options"][0],
            q["options"][1],
            q["options"][2],
            q["options"][3],
            "30",
            q["correct"]
        ]
        writer.writerow(row)

print("CSV conversion completed successfully!")
print(f"Generated {len(quiz_data)} questions in {output_file}")
