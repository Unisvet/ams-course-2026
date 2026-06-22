import csv

# Shortened version matching character constraints (Question: <=120, Answer options: <=75)
quiz_data = [
    {
        "question": "Welche drei Säulen bilden das funktionale Fundament der agentischen Schleife (Agentic Loop) in autonomen Systemen?",
        "options": [
            "Input, Processing, Output",
            "Wahrnehmung (Perception), Denken (Reasoning), Handeln (Action)",
            "Datenbeschaffung, Modelltraining, Inferenz",
            "Prompting, API-Call, JSON-Parsing"
        ],
        "correct": "2"
    },
    {
        "question": "Vorteile des ReAct-Patterns gegenüber isolierter Planung/Aktion? (Mehrfachauswahl)",
        "options": [
            "Modell kann über 'Thoughts' Zwischenschritte planen & analysieren.",
            "Es reduziert die Inferenzkosten auf Null (keine API-Calls nötig).",
            "Erkennt Fehler in 'Observations' & passt Pläne dynamisch an.",
            "Es verhindert Halluzinationen komplett bei Mathe-Berechnungen."
        ],
        "correct": "1,3"
    },
    {
        "question": "Wie teilt ein Large Language Model dem ausführenden System mit, dass es ein Tool aufrufen möchte?",
        "options": [
            "Es generiert ein strukturiertes JSON mit Funktionsname & Argumenten.",
            "Es führt den Python-Code direkt in seinem eigenen latenten Raum aus.",
            "Es sendet eine HTTP-Anfrage über integriertes TCP ans Internet.",
            "Es gibt dem User Anweisungen, das Tool manuell zu starten."
        ],
        "correct": "1"
    },
    {
        "question": "Elemente einer Funktionsdeklaration (JSON Schema) für Tool Calling? (Mehrfachauswahl)",
        "options": [
            "Ein eindeutiger Funktionsname.",
            "Semantische Beschreibung, wozu das Tool dient.",
            "Die vollständige Python-Implementierung des Funktionskörpers.",
            "Parameter-Spezifikation (Typen, Beschreibungen & Pflichtfelder)."
        ],
        "correct": "1,2,4"
    },
    {
        "question": "Warum eignet sich JAX gut für physikalische Simulationen in Agentenschleifen?",
        "options": [
            "JIT-Kompilierung in XLA & Vektorisierung für Millisekunden-Laufzeit.",
            "JAX enthält vortrainierte neuronale Netze zur Bilderkennung von Fraktalen.",
            "JAX benötigt keinen Arbeitsspeicher und verhindert jegliche Latenz.",
            "Es wandelt die Mandelbrot-Menge in Text um für das LLM."
        ],
        "correct": "1"
    },
    {
        "question": "Welche Aussagen über das Gemma-Skills-Ökosystem & die Struktur sind korrekt? (Mehrfachauswahl)",
        "options": [
            "Skill ist ein modularer Ordner für Wissen & Tools einer Fähigkeit.",
            "SKILL.md enthält YAML-Metadaten & Kognitionsanweisungen (Prompts).",
            "Skills dürfen nur in C++ geschrieben sein, um Latenz zu minimieren.",
            "Tools und JSON-Schemas werden im tools/-Unterverzeichnis abgelegt."
        ],
        "correct": "1,2,4"
    },
    {
        "question": "Was passiert mit der Rückgabe (Observation) eines Funktionsaufrufs im ReAct-Pattern?",
        "options": [
            "Sie wird gelöscht, da das Modell den Zustand im Gedächtnis behält.",
            "Wird als Nachricht in Verlauf gefügt für nächsten Reasoning-Schritt.",
            "Wird direkt in die Gewichte des Modells eintrainiert (Fine-Tuning).",
            "Wird dem User als Fehlermeldung angezeigt, um Stop zu erzwingen."
        ],
        "correct": "2"
    },
    {
        "question": "Probleme bei komplexen Simulationen ohne Tools durch LLMs? (Mehrfachauswahl)",
        "options": [
            "Modell neigt zu mathematischen Halluzinationen bei Rechenschritten.",
            "Kann keine deterministischen Berechnungen über viele Schritte garantieren.",
            "Modell verweigert sofort die Ausführung und gibt einen Fehler aus.",
            "Ist auf statisches Wissen limitiert und ohne reale Laufzeitdaten."
        ],
        "correct": "1,2,4"
    },
    {
        "question": "Welche Iterationsvorschrift definiert die Mandelbrot-Menge in Problem Set 9?",
        "options": [
            "z_{n+1} = z_n^2 + c",
            "z_{n+1} = sin(z_n) * c",
            "x_{n+1} = r * x_n * (1 - x_n)",
            "f(x) = sigma(W * x + b)"
        ],
        "correct": "1"
    },
    {
        "question": "Wie reagiert ein robuster ReAct-Agent idealerweise auf einen Tool-Fehler?",
        "options": [
            "Ignoriert den Fehler und wiederholt die Aktion in Endlosschleife.",
            "Er bricht die gesamte Ausführung ab und wirft eine unbehandelte Exception.",
            "Liest Fehler in 'Observation', plant Korrektur & passt Parameter an.",
            "Er löscht den bisherigen Gesprächsverlauf, um den Fehler zu verbergen."
        ],
        "correct": "3"
    },
    {
        "question": "Welche Fakten treffen auf den Begründer Benoît Mandelbrot zu? (Mehrfachauswahl)",
        "options": [
            "Prägte 1975 den Begriff 'Fraktal' (lat. fractus = gebrochen).",
            "Sein 'B.' steht für nichts; rekursiver Witz: Benoît B. Mandelbrot.",
            "Forschte bei IBM mit Zugriff auf Rechner zur Visualisierung.",
            "Gewann den Physik-Nobelpreis für Flüssigkeitsturbulenzen."
        ],
        "correct": "1,2,3"
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

output_file = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks\week9\quiz-ams09-2026.csv"

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
for q in quiz_data:
    assert len(q["question"]) <= 120, f"Question too long: {q['question']}"
    for opt in q["options"]:
        assert len(opt) <= 75, f"Option too long: {opt}"
print("All character length constraints validated successfully!")
