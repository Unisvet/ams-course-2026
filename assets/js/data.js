// Course Metadata and Registry for Advanced Modeling and System Simulation (AMS) 2026

export const translations = {
    de: {
        courseInfo: {
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
        },
        modules: {
            "1": "Modul 1: Vom klassischen Modell zum Deep Learning",
            "2": "Modul 2: High-Performance Simulation & Stochastik",
            "3": "Modul 3: Foundation Models & Generative KI in der Simulation",
            "4": "Modul 4: Agentic Engineering & Orchestrierung",
            "5": "Modul 5: Capstone-Projekt & Abschluss"
        },
        weeksData: {
            "1": {
                id: "1",
                title: "Einführung in Systemsimulation & Modernes Tooling",
                module: "1",
                description: "Bedeutung der Modellierung und Simulationsketten. Einführung in die Antigravity CLI und ADE Antigravity.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "2": {
                id: "2",
                title: "Prädiktive Modellierung & Maschinelles Lernen",
                module: "1",
                description: "Einführung in TensorFlow und Keras. Aufbau, Training und Evaluierung eines ersten Keras-Modells zur Vorhersage von Systemzuständen.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "3": {
                id: "3",
                title: "Optimierung und Systemdynamik",
                module: "1",
                description: "Modellierung von Warteschlangensystemen und diskreten Events. Klassische Optimierung vs. KI-gestützte Verfahren.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "4": {
                id: "4",
                title: "Differenzierbare Simulation mit JAX & Flax",
                module: "2",
                description: "Paradigmenwechsel mit JAX (grad, jit, vmap) und Flax. Umschreiben eines rechenintensiven Python-Simulationscodes in JAX.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "5": {
                id: "5",
                title: "Partielle Differentialgleichungen (PDEs) neu gedacht",
                module: "2",
                description: "Klassische Ansätze (FEM, FDM) zur Lösung von PDEs (z. B. Wärmeleitung). Physics-Informed Neural Networks (PINNs) mit JAX/Flax.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "6": {
                id: "6",
                title: "Stochastische Simulationen im KI-Zeitalter",
                module: "2",
                description: "Monte Carlo Integration, Business Revenue Modelle und Markov-Ketten in dynamischen Systemen mit massivem HPC via JAX.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "7": {
                id: "7",
                title: "Frontier AI: Arbeiten mit der Google Gemini API",
                module: "3",
                description: "Vom klassischen ML zu Foundation Models. Multimodales Reasoning und Parameter-Tuning über die Google Gemini API.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "8": {
                id: "8",
                title: "Open-Weights Modelle: Lokale Simulation mit Gemma",
                module: "3",
                description: "Architektur lokaler Open-Weights Modelle (Gemma). Lokales Ausführen und Anbindung an eine laufende Simulation.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "9": {
                id: "9",
                title: "KI-Agenten, Tool Calling & Agenten-Skills",
                module: "4",
                description: "Vom Sprachmodell zum autonomen Akteur (Perception, Reasoning, Action, Tool Calling). Der Agent ruft Simulationen autonom auf.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "10": {
                id: "10",
                title: "Das Agent Development Kit (ADK)",
                module: "4",
                description: "Architektur und Konzepte des Agent Development Kits (ADK). State-Tracking und Memory-Management.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "11": {
                id: "11",
                title: "Agent Development Environments (ADE) & Antigravity",
                module: "4",
                description: "Betrieb von Agentensystemen unter Produktionsbedingungen in der Agent Development Environment (ADE) Antigravity.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "12": {
                id: "12",
                title: "Multi-Agenten-Systeme (MAS) & Komplexe Dynamiken",
                module: "4",
                description: "Kommunikation, Konfliktlösung und Koordination zwischen mehreren Agenten (z. B. Simulation eines Marktes).",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "13": {
                id: "13",
                title: "Projektarbeit, Hybride Architekturen & Debugging",
                module: "5",
                description: "Best Practices für hybride Systeme (Math-Engines + LLM-Schicht). Live-Debugging von KI-Halluzinationen.",
                active: true,
                tabs: ['intro', 'stories', 'problemset']
            },
            "14": {
                id: "14",
                title: "Projektpräsentationen (Showcase)",
                module: "5",
                description: "Die Studierenden präsentieren ihre lauffähigen, hybriden Systemsimulationen. Live-Demos und Code-Reviews.",
                active: true,
                tabs: ['intro', 'problemset']
            }
        },
        ui: {
            goalsTitle: "Lernziele & Vision",
            goalsContent1: "Vom mathematischen Modell zum autonomen KI-Agenten: Dieser Kurs rüstet dich mit dem modernsten Software-Engineering-Stack der Systemsimulation aus. Wir schlagen die Brücke zwischen fundierten klassischen Konzepten – wie Differentialgleichungen und Stochastik – und aktuellen Machine-Learning-Paradigmen. Du lernst, rechenintensive deterministische und stochastische Simulationen mit Hardware-Beschleunigung durch JAX und Flax zu implementieren und prädiktive Modelle mit TensorFlow und Keras zu trainieren.",
            goalsContent2: "Im zweiten Teil des Kurses tauchen wir tief in die Welt der Foundation Models ein. Du wirst praxisnah mit Open-Weights-Modellen wie Gemma und State-of-the-Art-Tools wie der Gemini API sowie der Antigravity CLI arbeiten, um effiziente Workflows aufzubauen. Ein besonderer Schwerpunkt liegt auf dem \"Agentic Engineering\": Mithilfe des Agent Development Kits (ADK) und professionellen Agent Development Environments (ADE) wie Antigravity entwickelst, testest und orchestrierst du autonome Multi-Agenten-Systeme.",
            coreContents: "Kerninhalte des Lehrplans",
            theory: "Systemtheorie",
            theoryDesc: "Bedeutung der Modellierung realer Systeme (Technik, Natur, Wirtschaft) und Simulationsketten.",
            predictive: "Predictive ML",
            predictiveDesc: "Diskrete und kontinuierliche Simulationen (Warteschlangen, Signalverarbeitung) mit TensorFlow/Keras.",
            hpc: "High-Performance",
            hpcDesc: "Partielle Differentialgleichungen (PDEs) & stochastische Monte Carlo / Markov-Ketten mit JAX/Flax.",
            agentic: "Agentic AI",
            agenticDesc: "Integration von Gemini & Gemma; Automatisierung mit Antigravity CLI & Multi-Agenten-Orchestrierung.",
            roadmapTitle: "Semester-Roadmap (14 Wochen)",
            roadmapDesc: "Klicke auf eine aktive Woche, um die Materialien zu öffnen.",
            gradesBtn: "Noten & Fortschritt",
            footerText: "Entwickelt für moderne Lehrmethoden in Systemsimulation und Frontier AI",
            points: "Leistungspunkte",
            gradingWeight: "Notengewichtung",
            yourPoints: "Deine Leistungspunkte",
            yourProgress: "Dein Fortschritt",
            completed: "abgeschlossen",
            materialsBtn: "Materialien Öffnen",
            locked: "Demnächst verfügbar",
            backToPortal: "Zum Portal Home",
            backToDashboard: "Dashboard-Home",
            theoryIntro: "Theoretische Einführung",
            infographic: "Infografik",
            problemSet: "Problem Set",
            quiz: "Quiz",
            stories: "Stories",
            loading: "Lade Daten...",
            errorIntro: "Einführung konnte nicht geladen werden.",
            errorQuiz: "Quiz konnte nicht initialisiert werden.",
            errorProblemSet: "Problem Set konnte nicht geladen werden.",
            errorStories: "Stories konnten nicht geladen werden.",
            pointsLabel: "Pkt",
            syllabus: "Syllabus / Wochen",
            statusDone: "Erfolgreich abgeschlossen",
            statusPending: "Noch nicht abgeschlossen",
            markDone: "Als abgeschlossen markieren",
            markUndone: "Als unvollständig markieren",
            questionOf: "Frage $1 von $2",
            progress: "Fortschritt: $1%",
            multiChoice: "Mehrfachauswahl (Wähle alle richtigen Antworten)",
            singleChoice: "Einfachauswahl (Wähle eine richtige Antwort)",
            explanation: "Erklärung:",
            noExplanation: "Keine Erklärung verfügbar.",
            submitAnswer: "Antwort abgeben",
            finishQuiz: "Quiz abschließen",
            nextQuestion: "Nächste Frage",
            quizComplete: "Quiz abgeschlossen!",
            yourScore: "Deine Punktzahl",
            percentCorrect: "$1% Richtig",
            badgeEarned: "Erhaltenes Abzeichen:",
            restartQuiz: "Wiederholen",
            noQuiz: "Kein Quiz für diese Woche verfügbar.",
            badgeMaster: "🎓 Master-Simulant",
            feedbackMaster: "Hervorragende Leistung! Du hast das Thema dieser Woche vollständig durchdrungen.",
            badgeBeginner: "🌱 Einsteiger",
            feedbackBeginner: "Das war ein guter Versuch, aber du solltest die Übungen und die Einführung noch einmal durchgehen.",
            badgeIntermediate: "🛡️ Simulations-Analyst",
            feedbackIntermediate: "Gute Arbeit! Die Kernkonzepte sind verstanden. Schau dir die falschen Fragen noch einmal an."
        }
    },
    en: {
        courseInfo: {
            title: "Applied Modeling and System Simulation",
            subtitle: "Advanced Modeling and System Simulation",
            semester: "Summer Semester 2026",
            institution: "BTU Cottbus-Senftenberg",
            department: "Chair of Artificial Intelligence and System Simulation",
            grading: [
                { label: "Weekly Quizzes and Presentations", value: "18%" },
                { label: "Problem Sets (Programming Tasks)", value: "52%" },
                { label: "Final Presentation (Project)", value: "30%" }
            ]
        },
        modules: {
            "1": "Module 1: From Classical Models to Deep Learning",
            "2": "Module 2: High-Performance Simulation & Stochastics",
            "3": "Module 3: Foundation Models & Generative AI in Simulation",
            "4": "Module 4: Agentic Engineering & Orchestration",
            "5": "Module 5: Capstone Project & Conclusion"
        },
        weeksData: {
            "1": {
                id: "1",
                title: "Introduction to System Simulation & Modern Tooling",
                module: "1",
                description: "Significance of modeling and simulation chains. Introduction to Antigravity CLI and ADE Antigravity.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "2": {
                id: "2",
                title: "Predictive Modeling & Machine Learning",
                module: "1",
                description: "Introduction to TensorFlow and Keras. Building, training, and evaluating a first Keras model for system state prediction.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "3": {
                id: "3",
                title: "Optimization and System Dynamics",
                module: "1",
                description: "Modeling of queueing systems and discrete events. Classical optimization vs. AI-supported methods.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "4": {
                id: "4",
                title: "Differentiable Simulation with JAX & Flax",
                module: "2",
                description: "Paradigm shift with JAX (grad, jit, vmap) and Flax. Rewriting computationally intensive Python simulation code in JAX.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "5": {
                id: "5",
                title: "Partial Differential Equations (PDEs) Reimagined",
                module: "2",
                description: "Classical approaches (FEM, FDM) for solving PDEs. Physics-Informed Neural Networks (PINNs) with JAX/Flax.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "6": {
                id: "6",
                title: "Stochastic Simulations in the AI Era",
                module: "2",
                description: "Monte Carlo Integration, Business Revenue Models, and Markov Chains in dynamic systems with massive HPC via JAX.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "7": {
                id: "7",
                title: "Frontier AI: Working with the Google Gemini API",
                module: "3",
                description: "From classical ML to Foundation Models. Multimodal reasoning and parameter tuning via the Google Gemini API.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "8": {
                id: "8",
                title: "Open-Weights Models: Local Simulation with Gemma",
                module: "3",
                description: "Architecture of local open-weights models (Gemma). Local execution and integration into a running simulation.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "9": {
                id: "9",
                title: "AI Agents, Tool Calling & Agent Skills",
                module: "4",
                description: "From language model to autonomous actor (Perception, Reasoning, Action, Tool Calling). The agent calls simulations autonomously.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "10": {
                id: "10",
                title: "The Agent Development Kit (ADK)",
                module: "4",
                description: "Architecture and concepts of the Agent Development Kit (ADK). State tracking and memory management.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "11": {
                id: "11",
                title: "Agent Development Environments (ADE) & Antigravity",
                module: "4",
                description: "Operating agent systems under production conditions in the Agent Development Environment (ADE) Antigravity.",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "12": {
                id: "12",
                title: "Multi-Agent Systems (MAS) & Complex Dynamics",
                module: "4",
                description: "Communication, conflict resolution, and coordination between multiple agents (e.g., simulation of a market).",
                active: true,
                tabs: ['intro', 'infographic', 'stories', 'problemset', 'quiz']
            },
            "13": {
                id: "13",
                title: "Project Work, Hybrid Architectures & Debugging",
                module: "5",
                description: "Best practices for hybrid systems (Math Engines + LLM layer). Live debugging of AI hallucinations.",
                active: true,
                tabs: ['intro', 'stories', 'problemset']
            },
            "14": {
                id: "14",
                title: "Project Presentations (Showcase)",
                module: "5",
                description: "Students present their runnable, hybrid system simulations. Live demos and code reviews.",
                active: true,
                tabs: ['intro', 'problemset']
            }
        },
        ui: {
            goalsTitle: "Learning Objectives & Vision",
            goalsContent1: "From mathematical models to autonomous AI agents: This course equips you with the most modern software engineering stack of system simulation. We bridge the gap between solid classical concepts – such as differential equations and stochastics – and current machine learning paradigms. You will learn to implement computationally intensive deterministic and stochastic simulations with hardware acceleration through JAX and Flax and train predictive models with TensorFlow and Keras.",
            goalsContent2: "In the second part of the course, we dive deep into the world of Foundation Models. You will work hands-on with open-weights models like Gemma and state-of-the-art tools like the Gemini API and Antigravity CLI to build efficient workflows. A special focus is on \"Agentic Engineering\": Using the Agent Development Kit (ADK) and professional Agent Development Environments (ADE) like Antigravity, you will develop, test, and orchestrate autonomous multi-agent systems.",
            coreContents: "Core Curriculum Contents",
            theory: "System Theory",
            theoryDesc: "Significance of modeling real systems (engineering, nature, economy) and simulation chains.",
            predictive: "Predictive ML",
            predictiveDesc: "Discrete and continuous simulations (queues, signal processing) with TensorFlow/Keras.",
            hpc: "High-Performance",
            hpcDesc: "Partial Differential Equations (PDEs) & stochastic Monte Carlo / Markov chains with JAX/Flax.",
            agentic: "Agentic AI",
            agenticDesc: "Integration of Gemini & Gemma; automation with Antigravity CLI & multi-agent orchestration.",
            roadmapTitle: "Semester Roadmap (14 Weeks)",
            roadmapDesc: "Click on an active week to open the materials.",
            gradesBtn: "Grades & Progress",
            footerText: "Developed for modern teaching methods in system simulation and Frontier AI",
            points: "Credit Points",
            gradingWeight: "Grading Weight",
            yourPoints: "Your Performance Points",
            yourProgress: "Your Progress",
            completed: "completed",
            materialsBtn: "Open Materials",
            locked: "Coming Soon",
            backToPortal: "Back to Portal Home",
            backToDashboard: "Dashboard Home",
            theoryIntro: "Theoretical Introduction",
            infographic: "Infographic",
            problemSet: "Problem Set",
            quiz: "Quiz",
            stories: "Stories",
            loading: "Loading data...",
            errorIntro: "Introduction could not be loaded.",
            errorQuiz: "Quiz could not be initialized.",
            errorProblemSet: "Problem Set could not be loaded.",
            errorStories: "Stories could not be loaded.",
            pointsLabel: "Pts",
            syllabus: "Syllabus / Weeks",
            statusDone: "Successfully completed",
            statusPending: "Not yet completed",
            markDone: "Mark as completed",
            markUndone: "Mark as incomplete",
            questionOf: "Question $1 of $2",
            progress: "Progress: $1%",
            multiChoice: "Multiple Choice (Select all correct answers)",
            singleChoice: "Single Choice (Select one correct answer)",
            explanation: "Explanation:",
            noExplanation: "No explanation available.",
            submitAnswer: "Submit Answer",
            finishQuiz: "Finish Quiz",
            nextQuestion: "Next Question",
            quizComplete: "Quiz Completed!",
            yourScore: "Your Score",
            percentCorrect: "$1% Correct",
            badgeEarned: "Badge Earned:",
            restartQuiz: "Restart Quiz",
            noQuiz: "No quiz available for this week.",
            badgeMaster: "🎓 Master Simulant",
            feedbackMaster: "Outstanding performance! You have fully mastered this week's topic.",
            badgeBeginner: "🌱 Beginner",
            feedbackBeginner: "That was a good attempt, but you should review the exercises and the introduction again.",
            badgeIntermediate: "🛡️ Simulation Analyst",
            feedbackIntermediate: "Good job! The core concepts are understood. Review the incorrect questions again."
        }
    }
};

export const currentLang = localStorage.getItem('ams_lang') || 'de';

export const courseInfo = translations[currentLang].courseInfo;
export const modules = translations[currentLang].modules;
export const weeksData = translations[currentLang].weeksData;
export const ui = translations[currentLang].ui;

