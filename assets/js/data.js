// Course Metadata and Registry for Advanced Modeling and System Simulation (AMS) 2026

export const courseInfo = {
    title: "Angewandte Modellierung und Systemsimulation",
    subtitle: "Advanced Modeling and System Simulation",
    semester: "Sommersemester 2026",
    institution: "BTU Cottbus-Senftenberg",
    department: "Lehrstuhl für Künstliche Intelligenz und Systemsimulation",
    grading: [
        { label: "Wöchentliche Quizzes und Präsentationen", value: "18%" },
        { label: "Problem Sets (Programmieraufgaben)", value: "52%" },
        { label: "Abschlusspräsentation (Projekt)", value: "30%" }
    ]
};

export const modules = {
    "1": "Modul 1: Vom klassischen Modell zum Deep Learning",
    "2": "Modul 2: High-Performance Simulation & Stochastik",
    "3": "Modul 3: Foundation Models & Generative KI in der Simulation",
    "4": "Modul 4: Agentic Engineering & Orchestrierung",
    "5": "Modul 5: Capstone-Projekt & Abschluss"
};

export const weeksData = {
    "1": {
        id: "1",
        title: "Einführung in Systemsimulation & Modernes Tooling",
        module: "1",
        description: "Bedeutung der Modellierung und Simulationsketten. Einführung in die Gemini CLI und ADE Antigravity.",
        active: true
    },
    "2": {
        id: "2",
        title: "Prädiktive Modellierung & Maschinelles Lernen",
        module: "1",
        description: "Einführung in TensorFlow und Keras. Aufbau, Training und Evaluierung eines ersten Keras-Modells zur Vorhersage von Systemzuständen.",
        active: true
    },
    "3": {
        id: "3",
        title: "Optimierung und Systemdynamik",
        module: "1",
        description: "Modellierung von Warteschlangensystemen und diskreten Events. Klassische Optimierung vs. KI-gestützte Verfahren.",
        active: true
    },
    "4": {
        id: "4",
        title: "Differenzierbare Simulation mit JAX & Flax",
        module: "2",
        description: "Paradigmenwechsel mit JAX (grad, jit, vmap) und Flax. Umschreiben eines rechenintensiven Python-Simulationscodes in JAX.",
        active: true
    },
    "5": {
        id: "5",
        title: "Partielle Differentialgleichungen (PDEs) neu gedacht",
        module: "2",
        description: "Klassische Ansätze (FEM, FDM) zur Lösung von PDEs (z. B. Wärmeleitung). Physics-Informed Neural Networks (PINNs) mit JAX/Flax.",
        active: true
    },
    "6": {
        id: "6",
        title: "Stochastische Simulationen im KI-Zeitalter",
        module: "2",
        description: "Monte Carlo Integration, Business Revenue Modelle und Markov-Ketten in dynamischen Systemen mit massivem HPC via JAX.",
        active: true
    },
    "7": {
        id: "7",
        title: "Frontier AI: Arbeiten mit der Google Gemini API",
        module: "3",
        description: "Vom klassischen ML zu Foundation Models. Multimodales Reasoning und Parameter-Tuning über die Google Gemini API.",
        active: true
    },
    "8": {
        id: "8",
        title: "Open-Weights Modelle: Lokale Simulation mit Gemma",
        module: "3",
        description: "Architektur lokaler Open-Weights Modelle (Gemma). Lokales Ausführen und Anbindung an eine laufende Simulation.",
        active: false
    },
    "9": {
        id: "9",
        title: "KI-Agenten, Tool Calling & Agenten-Skills",
        module: "4",
        description: "Vom Sprachmodell zum autonomen Akteur (Perception, Reasoning, Action, Tool Calling). Der Agent ruft Simulationen autonom auf.",
        active: false
    },
    "10": {
        id: "10",
        title: "Das Agent Development Kit (ADK)",
        module: "4",
        description: "Architektur und Konzepte des Agent Development Kits (ADK). State-Tracking und Memory-Management.",
        active: false
    },
    "11": {
        id: "11",
        title: "Agent Development Environments (ADE) & Antigravity",
        module: "4",
        description: "Betrieb von Agentensystemen unter Produktionsbedingungen in der Agent Development Environment (ADE) Antigravity.",
        active: false
    },
    "12": {
        id: "12",
        title: "Multi-Agenten-Systeme (MAS) & Komplexe Dynamiken",
        module: "4",
        description: "Kommunikation, Konfliktlösung und Koordination zwischen mehreren Agenten (z. B. Simulation eines Marktes).",
        active: false
    },
    "13": {
        id: "13",
        title: "Projektarbeit, Hybride Architekturen & Debugging",
        module: "5",
        description: "Best Practices für hybride Systeme (Math-Engines + LLM-Schicht). Live-Debugging von KI-Halluzinationen.",
        active: false
    },
    "14": {
        id: "14",
        title: "Projektpräsentationen (Showcase)",
        module: "5",
        description: "Die Studierenden präsentieren ihre lauffähigen, hybriden Systemsimulationen. Live-Demos und Code-Reviews.",
        active: false
    }
};
