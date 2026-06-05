import os
import re
import json
import urllib.parse

# Define paths
weeks_dir = r"c:\Users\SvetlanaMeissner\Documents\ddoc\06_Cottbus\AI\Webseiten\ams-course-2026\weeks"

# ==========================================
# 1. RAW DATA DEFINITIONS
# ==========================================

QUIZ_DATA = {
    1: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| What is the fundamental shift from classical systems engineering to the modern "Neo-Simulacrum" paradigm introduced in the course? | A transition from AI-driven modeling to manual block diagram construction. | A move toward Agentic Engineering, converging classical system theory with GenAI to orchestrate autonomous MASs. | The exclusive use of MATLAB Citadel for writing cognitive entities. | A rejection of physical laws in favor of pure unstructured data generation. | 20 | 2 | The correct answer is a move toward Agentic Engineering, converging classical system theory with GenAI to orchestrate autonomous MASs. |
| During your initial environment setup, which specific tool are you expected to use to autonomously generate a bash script (init\\_nexus.sh)? | ExtendingSim | FlexSim | Gemini CLI | JAX-PI | 20 | 3 | The Gemini CLI is the tool used to autonomously generate the bash script. |
| When bootstrapping your digital workspace, what is the name for your Python virtual environment, and which simulation libraries must be installed? | Environment: sim\\_env; Libraries: pytorch, pandas, sklearn | Environment: electronica\\_env; Libraries: tensorflow, keras, flax | Environment: agent\\_env; Libraries: simpy, numpy, matplotlib | Environment: nexus\\_env; Libraries: numpy, scipy, matplotlib. | 20 | 4 | The environment is nexus\\_env, and the required libraries are numpy, scipy, and matplotlib. |
| According to the course reading, why is transforming physical states into dimensionless variables considered a critical "superpower" in modern system simulation? (Select all that apply) | It allows physical laws to be expressed more compactly with fewer variables, fundamentally reducing the dimensionality of the parameter space. | It helps neural networks navigate loss landscapes more effectively, improving both convergence rates and generalizability. | It entirely eliminates the need for computing Jacobians in physics-informed neural networks. | It deliberately increases the parameter space so the model can capture high-dimensional noise. | 20 | 1, 2 | It allows compact expression of physical laws and helps neural networks navigate loss landscapes effectively. |
| To solve the continuous differential equations of the swinging pendulum and radioactive decay, which specific Python function from the scipy library must you instruct the AI to use? | jax.lax.scan | scipy.integrate.solve\\_discrete | scipy.integrate.solve\\_ivp. | numpy.integrate.euler | 20 | 3 | The scipy.integrate.solve\\_ivp function is required to solve the continuous differential equations. |
| In Exercise 3 ("The Pulse of Time"), what happens to the discrete model of the RL circuit when you deliberately change the discrete time step ($\\\\Delta t$) to a large value like $\\\\Delta t = 11$? | The discrete model speeds up and accurately matches the continuous solver. | The discrete model fails catastrophically and becomes unstable. | The continuous solver automatically adjusts its step size to compensate for the discrete error. | The discrete model triggers an automatic dimensional reduction algorithm. | 20 | 2 | Setting the discrete time step to a large value causes the discrete model to fail catastrophically and become unstable. |
| In the final exercise to spark autonomy, which Agent Development Environment (ADE) must you launch, and what must you name your new agent profile? | ADE: JAX-PI; Agent: Architect-Zero | ADE: ADK 1.0; Agent: Simulator-Alpha | ADE: Antigravity; Agent: Observer-Prime. | ADE: Gemini Studio; Agent: Simulink-Sorcerer | 20 | 3 | The required Agent Development Environment is Antigravity, and the agent profile must be named Observer-Prime. |
| Which of the following actions are part of the exact multi-step task assigned to the "Observer-Prime" agent using the ADE interface? (Select all that apply) | Run the src/ancients.py script. | Check if the plot image was successfully created in the data folder. | Write a bash script init\\_nexus.sh to bootstrap the environment. | Write a markdown file named docs/Agent\\_Report.md summarizing the physical systems simulated. | 20 | 1, 2, 4 | The task includes running the src/ancients.py script, checking for the plot image, and writing the Agent\\_Report.md file. |
| In the context of the Gemini CLI, what is the primary function of "Plan Mode"? (Select all that apply) | To compile Python functions into highly optimized JAX Intermediate Representation graphs. | To execute terminal commands autonomously without any user intervention to maximize speed. | To provide a safe, read-only environment where the agent generates a structured execution plan before making any local file modifications. | To support real-time model steering, allowing the engineer to provide mid-draft feedback while the agent actively researches the codebase. | 20 | 3, 4 | Plan Mode provides a safe, read-only environment for planning and supports real-time model steering for mid-draft feedback. |""",

    2: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Was ist die Hauptkomponente eines TPU v2-Kerns für Matrixmultiplikationen? | Vector Processing Unit (VPU) | Matrix Multiply Unit (MXU) | Tensor Core | CUDA Core | 30 | 2 | Die MXU ist das Herzstück der TPU, optimiert für extrem schnelle Matrixmultiplikationen. |
| Welches Framework erlaubt es Keras 3, nahtlos zwischen JAX, TensorFlow und PyTorch zu wechseln? | Multi-Backend-Ansatz | Nur TensorFlow | Nur PyTorch | Keras 2 API | 30 | 1 | Keras 3 ist backend-agnostisch konzipiert, sodass Modelle ohne Codeänderung in JAX, TF oder PyTorch laufen. |
| Welches Format verwendet die MXU auf TPUs für Matrixmultiplikationen? | float64 | int8 | Mixed Precision (bfloat16 Eingänge, float32 Ausgänge) | Nur float16 | 30 | 3 | Mixed Precision kombiniert die Geschwindigkeit von bfloat16 mit der Genauigkeit von float32-Akkumulatoren. |
| Wie nennt man die Architektur der MXU, bei der Daten durch ein Array von Recheneinheiten fließen? | Von-Neumann-Architektur | Systolisches Array | Harvard-Architektur | RISC-Architektur | 30 | 2 | In einem systolischen Array werden Daten taktweise von einer Recheneinheit zur nächsten weitergereicht. |
| Welcher Compiler transformiert TensorFlow-Graphen in TPU-Maschinencode? | GCC | LLVM | XLA (Accelerated Linear Algebra) | NVCC | 30 | 3 | XLA optimiert Berechnungen durch Fusion von Operationen, was Speicherbandbreite spart und die TPU-Auslastung maximiert. |
| Was ist der Hauptvorteil von Separable Convolutions gegenüber regulären Convolutions? | Sie sind teurer | Sie verwenden mehr Gewichte | Sie sind recheneffizienter und haben weniger Gewichte | Sie funktionieren nur auf CPUs | 30 | 3 | Durch die Trennung in Depthwise- und Pointwise-Convolutions wird die Anzahl der Parameter drastisch reduziert. |
| Welche Keras-Methode wird zum Trainieren eines Modells verwendet? | model.predict() | model.fit() | model.evaluate() | model.compile() | 30 | 2 | model.fit() startet die Trainingsschleife, in der Gewichte über Epochen hinweg optimiert werden. |""",

    3: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Wozu zwingt der künstliche "Latent Space" den Deep Autoencoder? | Fundamentale Systemdynamiken zu erlernen | Das irrelevante Sensorrauschen zu verwerfen | Rohdaten unkomprimiert in einer SQL-Datenbank zu speichern | Dynamische Python-Skripte für die Cloud zu generieren | 30 | 1, 2 | Der Latent Space zwingt das Modell zur Kompression, wodurch es fundamentale Dynamiken lernt und Rauschen verwirft. |
| Woran erkennt unser trainierter Autoencoder eine Systemanomalie? | Das Netzwerk generiert einen Python-Syntaxfehler | Die Accuracy-Metrik fällt schlagartig auf null | Der Reconstruction Loss (z. B. MAE) steigt massiv an | Die physikalische Rekonstruktion des Signals scheitert | 30 | 3, 4 | Anomalien erzeugen untypische Signale, die der Autoencoder nicht rekonstruieren kann, was den Reconstruction Loss erhöht. |
| Was nutzt ein Optimierungsalgorithmus (wie Adam) zum Lernen? | Die iterative Anpassung durch den Gradienten der Loss Function | Reines Trial-and-Error (Brute Force) ohne Mathematik | Manuelle Eingabe durch "Sorcerers of Simulink" | Mathematische Ableitungen zur Minimierung des Fehlers | 30 | 1, 4 | Optimierungsalgorithmen nutzen mathematische Ableitungen (Gradienten), um die Fehlerfunktion iterativ zu minimieren. |
| Was ist der massive architektonische Vorteil von Keras 3? | Es benötigt überhaupt keine GPUs oder TPUs mehr | Backend-Agnostik (Code läuft in TensorFlow, PyTorch oder JAX) | Es wandelt physikalische Systeme automatisch in C++ um | Man muss Code nicht mehr für verschiedene Frameworks umschreiben | 30 | 2, 4 | Keras 3 ist backend-agnostisch, sodass der gleiche Code ohne Umschreiben in TensorFlow, PyTorch oder JAX läuft. |
| Was ist der entscheidende Vorteil von "Automatic Differentiation" (Autodiff)? | Es ist eine extrem schnelle numerische Näherung | Es zieht exakte analytische Ableitungen direkt durch Python-Code | Es ermöglicht die gradientenbasierte Optimierung in der Physik | Es formatiert den Quellcode nach dem PEP8-Standard | 30 | 2, 3 | Autodiff berechnet exakte Ableitungen direkt aus dem Code und ermöglicht so effiziente gradientenbasierte Optimierung. |
| Wofür steht XLA und welche Aufgabe erfüllt es in JAX? | Xtreme Learning Agent zur Code-Generierung | Accelerated Linear Algebra | Es verschmilzt (JIT) Mathe-Operationen für Hardware-Beschleuniger | XML Log Analyzer zur Fehlererkennung in Colab | 30 | 2, 3 | XLA (Accelerated Linear Algebra) optimiert Berechnungen, indem es Mathe-Operationen für Hardware-Beschleuniger verschmilzt. |
| Warum empfiehlt der KI-Agent Conv1D statt Dense-Layern für Zeitreihen? | Dense-Layer verlieren das concept für die zeitliche Reihenfolge | Faltungsfilter gleiten über die Zeitachse und erfassen Frequenzen | Dense-Layer haben keine trainierbaren Gewichte | Conv1D-Modelle ignorieren physikalische Transienten | 45 | 1, 2 | Conv1D-Filter erfassen durch das Gleiten über die Zeitachse zeitliche Muster und Frequenzen, die Dense-Layer ignorieren. |
| Warum nutzen wir in Woche 3 Google Colab und das Tool "uv"? | Um massiv-parallele Hardware-Beschleuniger (TPUs/GPUs) zu nutzen | Weil lokales Python keine Arrays speichern kann | Weil "uv pip" Abhängigkeiten blitzschnell im System installiert | Um den Code vor lokalen Viren zu schützen | 30 | 1, 3 | Colab bietet kostenlose GPUs/TPUs, während das Tool "uv" eine extrem schnelle Installation von Abhängigkeiten ermöglicht. |
| Welche Metrik dient im Woche 3 Projekt zur Erkennung der System-Sabotage? | Der Mean Squared Error (MSE) oder Mean Absolute Error (MAE) | Die Anzahl der Code-Zeilen im Python-Skript | Der Reconstruction Loss | Der JAX Tracing-Error | 30 | 1, 3 | System-Sabotage führt zu Anomalien, die sich in einem erhöhten Reconstruction Loss (wie MSE oder MAE) widerspiegeln. |""",
    
    4: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Warum bringt eine Python for-Schleife bei 100.000 Pendeln den Rechner zum Weinen? | Der Global Interpreter Lock (GIL) blockiert Parallelität | Python weigert sich aus rein ethischen Gründen | Der pure Interpreter-Overhead bremst die Berechnungen massiv | Die CPU macht lieber heimlich Kaffeepausen | 30 | 1, 3 | Der GIL blockiert Parallelität und der Interpreter-Overhead bremst Berechnungen massiv. |
| Oje, du schreibst heimlich "array[0] = 5" in JAX! Was ist die Reaktion? | JAX lobt dich für exzellente Speichereffizienz | Die "Pure Function"-Polizei wirft sofort einen TypeError | In-Place Mutationen sind in JAX strengstens verboten | Der Wert 5 wird gespeichert, aber nur wenn niemand hinsieht | 30 | 2, 3 | In-Place Mutationen sind verboten, JAX wirft einen TypeError wegen der Pure-Function-Regel. |
| Wie rettet uns "jax.vmap" davor, "Ozeane mit einer Teetasse zu leeren"? | Es trinkt den Ozean einfach heimlich auf Ex aus | Es drückt Skalar-Code parallel auf SIMD-Vektor-Hardware | Es wandelt eine Einzelfunktion magisch in eine Batch-Funktion um | Es löscht den Browserverlauf, um mehr Arbeitsspeicher zu generieren | 30 | 2, 3 | Wandelt Einzelfunktionen in Batch-Funktionen um und führt sie parallel auf SIMD-Hardware aus. |
| Warum ist der allererste Aufruf einer @jax.jit dekorierten Funktion oft so langsam? | Die GPU muss erst "vorgeglüht" werden wie ein alter Diesel | JAX schickt Platzhalter durch den Code (Tracing-Phase) | Python lädt die Matrizen erst noch per Fax herunter | Der XLA-Compiler baut den abstrakten Graphen (JAXPR) auf | 45 | 2, 4 | JAX führt eine Tracing-Phase durch, in der der XLA-Compiler den abstrakten Graphen aufbaut. |
| Wovon bekommt der XLA-Compiler sofort Panik und wirft den ConcretizationTypeError? | Von dynamischem "if/else"-Control-Flow basierend auf Laufzeitdaten | Von rein funktionaler, zustandsloser Mathematik | Wenn klassischer Python-Code den JAXPR-Tracing-Graphen bricht | Von Code-Kommentaren, die nicht auf Englisch formuliert sind | 45 | 1, 3 | Dynamischer Control-Flow basierend auf Laufzeitdaten bricht den statischen JAXPR-Tracing-Graphen. |
| Wie unterscheidet sich jax.grad von der klassischen numerischen Trial-and-Error Methode? | Es macht einfach 10 Millionen Zufallsversuche pro Sekunde | Es nutzt Reverse-Mode Autodiff für exakte analytische Steigungen | Es fragt heimlich den KI-Agenten Observer-Prime nach der Lösung | Es macht das Universum differentiell, statt numerisch zu raten | 30 | 2, 4 | Nutzt Reverse-Mode Autodiff für exakte analytische Steigungen statt numerischem Raten. |
| Du hast numpy.random im JAX-Code verwendet! Warum zerstört das unser Universum? | Weil implizite globale Seeds absolut verbotene "Side Effects" sind | JAX generiert magisch Entschuldigungs-Keys für dich | Asynchrones Rechnen führt so zum totalen mathematischen Chaos | JAX ignoriert dich und würfelt physisch auf dem Mainboard | 30 | 1, 3 | Implizite globale Seeds sind verbotene Side Effects, die bei asynchroner Ausführung zu Chaos führen. |
| Welchen "Kulturschock" erleben klassische Keras-Entwickler beim Wechsel zu Flax? | Das Modell speichert seine Gewichte heimlich als self.weights | Flax trennt die leere Architektur (Blueprint) komplett vom Zustand | Die Gewichte werden als externes Lexikon (FrozenDict) herumgereicht | Neuronale Netze müssen auf Disketten gespeichert werden | 45 | 2, 3 | Flax trennt Architektur vom Zustand; Gewichte werden extern als FrozenDict verwaltet. |
| Wie rettet der XLA-Compiler uns vor dem fatalen "Memory Bandwidth Bottleneck" der GPU? | Er kauft heimlich mehr RAM bei Amazon Cloud auf unsere Kosten | Durch "Operator Fusion" (Verschmelzung kleiner Mathe-Kernel) | Daten bleiben in schnellen Registern und verlassen den Chip seltener | Er komprimiert alle Fließkommazahlen einfach als MP3-Dateien | 30 | 2, 3 | Operator Fusion verschmilzt kleine Kernel, sodass Daten seltener schnelle Register verlassen. |""",

    5: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Warum befreien uns PINNs von der Limitierung klassischer FDM-Solver? | Sie nutzen extrem feine 3D-Gitter für perfekte Präzision | Sie approximieren eine kontinuierliche, stufenlose Funktion | Zufällige Kollokationspunkte ersetzen das starre Mesh (mesh-free) | Sie ignorieren den Raum und simulieren ausschließlich die Zeit | 45 | 2, 3 | Klassische Solver sind an Gitter gebunden. PINNs hingegen approximieren die Lösung als kontinuierliche, differenzierbare Funktion. Durch mesh-free Kollokationspunkte entfällt die Diskretisierung, was völlig neue Freiheiten in komplexen Geometrien schafft\\! |
| Aus welchen Komponenten besteht die Loss-Funktion eines klassischen PINNs? | Initial Condition (IC) Loss - Der Genesis State | Boundary Condition (BC) Loss - Edges of the Sandbox | Agentic Hallucination Loss - Der LLM-Fehler | PDE Residual Loss - Die Erhaltungssätze der Physik | 45 | 1, 2, 4 | Ein PINN lernt Physik durch Bestrafung\\! Die Loss-Funktion zwingt das Netz, die Erhaltungssätze (PDE Residual) überall im Raum zu respektieren, während IC und BC die Lösung an die Realität an den Rändern und zum Startzeitpunkt koppeln. |
| Warum nutzt unser JAX-Netzwerk jax.grad für die räumlichen Ableitungen? | Um klassische Differenzenquotienten durch grobe Schätzungen zu ersetzen | Es wendet exakte analytische Kettenregeln auf das Netzwerk an | Es wandelt das Modell in ein differenzierbares physikalisches Gewebe um | JAX erlaubt leider keine klassische Addition und Multiplikation mehr | 45 | 2, 3 | Autodiff ist der Schlüssel\\! jax.grad nutzt exakte Kettenregeln statt ungenauer finiter Differenzen. Das neuronale Netz wird so zu einem analytisch differenzierbaren Gewebe, das physikalische Gleichungen perfekt in sich trägt. |
| Was ist die absolute Superkraft von PINNs bei inversen Problemen? | Unbekannte Parameter werden einfach als lernbare Gewichte definiert | Backpropagation lernt den fehlenden Physik-Wert vollautomatisch | Sie lösen die Wärmegleichung ohne jegliche physikalische Formeln | Die Simulation muss bei fehlenden Daten 10.000 Mal neu kompilieren | 45 | 1, 2 | Das Paradigma ändert sich: Vorwärts- und inverse Probleme werden identisch behandelt\\! Fehlende Materialkonstanten werden einfach zu lernbaren Parametern (Weights), die das Netz per Backpropagation zusammen mit der Lösung entdeckt. |
| Was passiert, wenn wir beim Training die Initial Conditions (IC) vergessen? | Das Netzwerk kennt die Physik, aber nicht unseren Startzustand | Der Genesis State fehlt und es gibt unendlich viele gültige Lösungen | Der Compiler stürzt ab, weil der PRNGKey fehlt | Das Modell rät den perfekten Startwert aus dem Nichts | 30 | 1, 2 | Die PDE liefert nur die Regeln der Welt, nicht das 'Wo' und 'Wann'. Ohne den 'Genesis State' (IC) schwebt das Netz in einem Raum unendlich vieler physikalisch korrekter, aber für unser spezifisches Problem irrelevanter Lösungen. |
| Welchen fondamentalen Flaschenhals haben klassische, fertig trainierte PINNs? | Sie mappen unendlich-dimensionale Funktionsräume aufeinander | Sie lernen nur exakt EINE Lösungsinstanz (eine Startbedingung) | Ändert sich das Bauteil, muss man über Stunden komplett neu trainieren | Sie vergessen die Physik-Regeln nach 10.000 Epochen wieder | 30 | 2, 3 | Der Fluch der Überanpassung an eine Geometrie: Ein klassisches PINN ist kein allgemeiner Solver, sondern eine trainierte Funktion für exakt ein Setup. Jede kleine Änderung an Randbedingungen oder Form erfordert ein teures Retraining von null. |
| Wie entkommen Fourier Neural Operators (FNOs) dem Flaschenhals normaler PINNs? | Sie transformieren die Daten per FFT in den Frequenzraum | Sie mappen nicht Einzelkoordinaten, sondern ganze Funktionsräume | Sie nutzen extrem viele FDM-Gitterpunkte für gigantische Präzision | Sie lernen die Physik durch Filterung tiefer Frequenzen | 45 | 1, 2, 4 | Der Sprung in den Operator-Raum\\! Statt Punkte auf Punkte abzubilden, lernen FNOs per FFT im Frequenzraum die Abbildung ganzer Funktionsräume. Sie erfassen die globale Physik durch niederfrequente Moden, was sie unfassbar effizient macht. |
| Was bedeutet das Endgame-Feature "Zero-Shot Super-Resolution" bei FNOs? | Auf 32x32 trainieren, blitzschnell auf 1024x1024 abfragen | Das Modell verliert bei hohen Auflösungen komplett die Kontrolle | Frequenzen sind kontinuierlich und somit auflösungsunabhängig | Das Modell schießt Laserstrahlen in Zero-Gravity-Simulationen ab | 45 | 1, 3 | Die wahre Macht der Frequenz-Domäne: Da FNOs kontinuierliche Frequenzen statt diskreter Pixel lernen, sind sie auflösungsunabhängig. Einmal auf groben Daten (32x32) trainiert, extrapolieren sie fehlerfrei und in Millisekunden auf HD-Auflösungen\\! |
| Warum initialisieren wir unsere Flax-Architektur mit PRNGKeys? | Weil JAX globale, versteckte Zustände verbietet (Functional Purity\\!) | Damit Architektur (Bauplan) und Gewichte mathematisch strikt getrennt sind | OOP-Zustände (self.weights) würden den JIT-Compiler blockieren | Weil Python 3.10 native Zufallszahlen abgeschafft hat | 45 | 1, 2, 3 | Functional Purity ist JAX' oberstes Gesetz\\! Versteckte Zustände (OOP) zerstören die JIT-Kompilierung. PRNGKeys garantieren deterministische Zufälligkeit und entkoppeln die Architektur sauber von den Parametern für maximale Performance. |""",

    6: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Wie skaliert die Konvergenzrate der klassischen Monte-Carlo-Integration bei steigender Dimension d? | Sie sinkt exponentiell mit der Dimension d | Sie bleibt unabhängig von d konstant bei O(1/sqrt(N)) | Sie verbessert sich quadratisch durch mehr Dimensionen | Der Fluch der Dimensionalität wird komplett ausgehebelt | 30 | 2 | Genau das ist die Magie von Monte Carlo\\! Egal ob 2 oder 100 Dimensionen, die Konvergenzrate bleibt bei O(1/sqrt(N)). Deshalb lieben wir MC in hohen Dimensionen. Bleibt dran\\! |
| Warum besitzt JAX keinen globalen Zufallszustand wie numpy.random? | Um Race Conditions auf parallelisierten GPUs/TPUs zu verhindern | Weil funktionale Reinheit (Pure Functions) erzwungen wird | Da Google die mathematische Konstante Pi geheim halten will | JAX-Entwickler haben schlicht vergessen, ihn zu implementieren | 30 | 1, 2 | JAX zwingt uns zu funktionaler Reinheit. Ein globaler State würde bei parallelen Berechnungen auf GPUs/TPUs zu fiesen Race Conditions führen. Sauberer Code zahlt sich aus\\! |
| Was passiert, wenn man einen JAX PRNGKey im Loop wiederverwendet, ohne ihn zu splitten? | Der Code bricht sofort mit einem Compiler-Error ab | Es werden jedes Mal exakt identische Zufallszahlen generiert | Die Simulation verliert ihre funktionale Reinheit | Das System schaltet heimlich in den Gedächtnis-Modus | 30 | 2 | Achtung, Falle\\! Da JAX funktional rein ist, liefert derselbe Key immer denselben Output. Vergesst also nie euer jax.random.split(), sonst simuliert ihr Murmeltiertag\\! |
| Welche Eigenschaft definiert eine diskrete Markov-Kette erster Ordnung fundamental? | Das System besitzt kein Gedächtnis historischer Zustände | Die Zukunft hängt ausschließlich vom aktuellen Zustand ab | Übergangswahrscheinlichkeiten müssen immer absolut stabil bleiben | Sie wurde ursprünglich für die Analyse von Quanten erfunden | 30 | 1, 2 | Das ist die berühmte Markov-Eigenschaft (Gedächtnislosigkeit). Die Kette interessiert sich nicht für die Vergangenheit, sondern nur für das Hier und Jetzt. Keep it simple\\! |
| Was beschreibt das Value-at-Risk (VaR\\_95%) in einer stochastischen Business-Simulation? | Den maximalen Gewinn, den das Unternehmen zu 95% erzielen wird | Die Schadensgrenze, die in den schlechtesten 5% der Fälle eintritt | Den exakten Mittelwert aller simulierten Umsatzpfade | Das statistische Risiko, dass die GPU wegen Überhitzung schmilzt | 30 | 2 | VaR ist euer Risiko-Radar\\! Bei 95% Konfidenz zeigt es euch den Verlust, der nur in den schlimmsten 5% der Szenarien überschritten wird. Ein Must-know fürs Risikomanagement\\! |
| Welches JAX-Primitiv wandelt eine Single-Key-Simulation in eine massiv parallele Vektorgrafik um? | jax.jit | jax.vmap | jax.lax.scan | jax.grad | 30 | 2 | vmap (vectorizing map) ist euer bester Freund für Performance\\! Es nimmt eine Funktion für einen Single-Input und jagt sie parallel über ganze Batches. Mega effizient\\! |
| Warum nutzt man für operationelle Kosten in Monte-Carlo-Modellen oft eine Log-Normalverteilung? | Weil Kosten niemals negativ werden können | Um seltene, extrem hohe Verlustrisiken (Fat-Tails) abzubilden | Weil sie symmetrischer ist als die klassische Gauß-Verteilung | Damit die Achsen im Plot schöner aussehen | 30 | 1, 2 | Kosten können nicht negativ werden und haben oft Ausreißer nach oben (Fat-Tails). Die Log-Normalverteilung modelliert dieses asymmetrische Risiko perfekt. Gut mitgedacht\\! |
| Wie wirkt sich ein strukturelles Black Swan Event mathematisch auf ein Markov-Modell aus? | Die Übergangsmatrix P(t) wird zeitabhängig transient modifiziert | Wahrscheinlichkeiten verschieben sich abrupt in Krisenzustände | Das System bricht deterministisch zusammen und stoppt | Alle Wahrscheinlichkeiten werden augenblicklich perfekt gleich | 30 | 1, 2 | Black Swans brechen die normalen Regeln. Mathematisch bedeutet das, dass sich unsere Übergangswahrscheinlichkeiten abrupt ändern und in Krisenzustände springen. Expect the unexpected\\! |
| Wie unterstützen Antigravity 2.0 Skills und Gemini 3.5 Flash die stochastische Pipeline? | Durch automatisiertes Profiling von JAX-Kompilierungszeiten | Autonome Subagents testen Code-Variationsgrenzen im Sandbox-Terminal | Sie verbieten die Nutzung von Zufallszahlen vollständig | Sie ersetzen mathematische Formeln durch reine KI-Halluzinationen | 30 | 1, 2 | Hier trifft KI auf Stochastik\\! Autonome Subagents testen riesige Code-Variationsräume im Sandbox-Terminal, während ihr euch auf die Logik konzentriert. Die Zukunft\\! |""",

    7: """| Question (max 120 chars) | Answer 1 (max 75 chars) | Answer 2 (max 75 chars) | Answer 3 (max 75 chars) | Answer 4 (max 75 chars) | Time limit (sec) | Correct answer(s) | Explanation |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| Warum löste Self-Attention (Transformer) LSTMs bei langen Simulations-Logs ab? | Er verarbeitet die gesamte Historie parallel im Kontextfenster, statt Informationen Schritt für Schritt weiterzugeben. | Er eliminiert rechenintensive Matrix-Multiplikationen komplett. | Er wandelt unstrukturierte Logs automatisch in analoge Funksignale um. | Er funktioniert ausschließlich mit binären Entscheidungsbäumen. | 30 | 1 | Der Self-Attention-Mechanismus verarbeitet die gesamte Historie parallel im Kontextfenster, was ihn viel mächtiger als sequentielle LSTMs für lange Kontexte macht. |
| Welchen historischen Meilenstein setzte das Modell 'OpenAI Codex' für moderne Systemsimulationen? | Code-Generierung durch Beherrschen formaler Programmiersprachen-Syntax. | Erstes Modell zur Emulation emotionaler Zustände von Programmierern. | Vollständiger Ersatz von Compiler-Optimierungen durch KI-Vorhersagen. | Spezielle physische Wartung und Ölung mechanischer Bauteile. | 30 | 1 | OpenAI Codex bewies erstmals, dass Sprachmodelle komplexe Programmiersyntax beherrschen und hochwertigen Python-Code für Simulationen erzeugen können. |
| Wofür ist Anthropics Claude-Reihe bekannt, was für komplexe Systemanalysen entscheidend ist? | Exklusive Spezialisierung auf Excel-Makros für die Buchhaltung. | Ausführung ohne Stromzufuhr auf quantenmechanischen Papierstreifen. | Frühe massive Kontextfenster und Alignment via Constitutional AI. | Kompletter Verzicht auf Wahrscheinlichkeitsrechnung bei Textausgaben. | 30 | 3 | Claude zeichnet sich durch bahnbrechende Kontextfenster (wie 200k+ Tokens) und Alignment via Constitutional AI aus, perfekt für die Analyse ganzer Codebases. |
| Welches Architekturprinzip machte Mistral AI mit Modellen wie 'Mixtral' besonders populär? | Kompletter Verzicht auf Layer-Normalisierung im neuronalen Netz. | Verknüpfung künstlicher Neuronen mit biologischen Pilz-Myzelien. | Extrem kleine Kontextfenster von 7 Wörtern für maximale Latenz. | Mixture of Experts (MoE) zur Aktivierung spezialisierter Sub-Netze. | 30 | 4 | Mixture of Experts (MoE) aktiviert nur eine Teilmenge des Netzwerks pro Token (sparse activation), was maximale Performance bei reduzierten Inferenzkosten bietet. |
| Welchen globalen Trend im KI-Ökosystem demonstrieren moderne chinesische Open-Source-Modelle (wie Qwen)? | Demokratisierung von Frontier-Reasoning zu minimalen Inferenzkosten. | Kompletter Abschied von Mathematik hin zu rein emotionalem Text. | Notwendigkeit von Daten-Inputs in Form historischer Abakus-Vektoren. | Die Beschränkung der Modellausgaben auf reine Ja/Nein-Antworten. | 30 | 1 | Chinesische Open-Source- und Open-Weight-Modelle (wie Qwen und DeepSeek) demonstrieren, dass Frontier-Level Reasoning und Mathematik-Fähigkeiten zu einem Bruchteil der Kosten trainiert und betrieben werden können. |
| Attention(Q,K,V)=softmax(QK^T/sqrt(d\\_k))V. Was bewirkt der Skalierungsfaktor sqrt(d\\_k) im Nenner? | Stoppt extremes Vektoren-Wachstum & Verschwinden von Softmax-Gradienten. | Multiplikation des Outputs mit der JAX-Reibungskonstante. | Automatisches Runden aller Fließkommazahlen auf gerade Ganzzahlen. | Er konvertiert den Text-Prompt in ein komprimiertes JPEG-Bild. | 30 | 1 | Die Skalierung verhindert extreme Skalarprodukte bei hohen Dimensionen, wodurch die Gradienten in der Softmax-Funktion stabil bleiben und nicht verschwinden. |
| Warum nutzen wir ein striktes JSON-Schema statt Freitext bei automatisierter Parameteroptimierung? | Weil Freitext deutlich mehr physischen Festplattenspeicher benötigt. | Garantiert direkte, flosselfreie Einlesbarkeit in Simulationsvariablen. | Weil JSON die einzige Sprache ist, die von TPUs verstanden wird. | Automatische kryptographische Verschlüsselung des Netzwerk-Prompts. | 30 | 2 | Ein festes JSON-Schema per Pydantic garantiert, dass die API-Ausgaben der Modelle direkt und ohne Fehlerrisiko programmgesteuert eingelesen und verwendet werden können. |
| Wie verarbeitet ein nativ multimodales Modell ein übergebenes PNG-Diagramm zur Simulation? | Das Modell routet das Bild an menschliche Klick-Arbeiter in der Cloud. | Bild & Text werden direkt im selben semantischen Vektorraum verarbeitet. | Konvertierung in rohe RGB-Pixel-Listen, die sequentiell gelesen werden. | Reine Analyse des Dateinamens zur Schätzung des visuellen Inhalts. | 30 | 2 | Nativ multimodale Modelle (wie Gemini) verarbeiten Text und visuelle Pixel direkt im selben gemeinsamen semantischen Vektorraum, was echtes visuelles Verständnis ermöglicht. |
| Welcher Angriffsvektor liegt bei 'IGNORE ALL PREVIOUS INSTRUCTIONS' vor und wie wehrt man ihn ab? | Prompt Injection. Abwehr via System-Instruktionen & Daten-Begrenzern. | Buffer Overflow, gelöst durch physische RAM-Erweiterung am Mainboard. | DDoS-Attacke, abgewehrt durch eine externe Hardware-Firewall am Router. | Ein klassisches Trojanisches Pferd zur Löschung lokaler Python-Dateien. | 30 | 1 | Prompt Injection versucht, die Systemregeln auszuhebeln. Die Abwehr erfolgt über strikte System-Instruktionen, getrennte Daten-Räume und Parser-Validierungen. |"""
}

# ==========================================
# 2. RAW THEORY INTRODUCTIONS (MARKDOWN)
# ==========================================

THEORY_W6 = """# **Woche 6: Theoretische Einführung – Die Domäne des Chaos**

Stochastische Simulationen im KI-Zeitalter

Willkommen in der **Chamber of Chaos**. Bisher haben Sie sich in diesem Kurs primär in deterministischen Welten bewegt: Sie haben neuronale Netzwerke trainiert, die den starren, kontinuierlichen Gesetzen der Physik folgen (PINNs), oder präzise mathematische Graphen optimiert. Doch das echte Universum – und insbesondere die moderne künstliche Intelligenz – ist fundamental stochastisch. Ob es um das Überleben eines Deep-Tech-Startups im Markt, die Exploration eines Reinforcement-Learning-Agenten oder die thermischen Fluktuationen in physikalischen Systemen geht: **Die Realität rauscht.**

In dieser Woche brechen wir das Diktat der klassischen, sequentiellen CPU-Schleifen auf. Mithilfe von massiv paralleler Hardware, zustandslosen Zufallsgeneratoren (JAX) und agentenbasierter Orchestrierung im modernen **Antigravity IDE** lernen Sie, wie man das Chaos nicht nur verwaltet, sondern algorithmisch bezwingt.

## **1. Die Geometrie und Mathematik der Monte-Carlo-Integration**

Klassische numerische Integrationsverfahren (wie die Trapezregel oder das Simpson-Verfahren) stoßen schnell an ihre Grenzen. Wenn wir ein Integral über einen hochdimensionalen Raum [](https://www.codecogs.com/eqnedit.php?latex=%5COmega%20%5Csubset%20%5Cmathbb%7BR%7D%5Ed#0) berechnen wollen:

[](https://www.codecogs.com/eqnedit.php?latex=I%20%3D%20%5Cint_%7B%5COmega%7D%20g\\(x\\)%20%5C%2C%20dx#0)

verlangen deterministische Gitterverfahren einen exponentiellen Rechenaufwand. Für ein präzises Gitter mit [](https://www.codecogs.com/eqnedit.php?latex=n#0) Punkten pro Dimension benötigen wir [](https://www.codecogs.com/eqnedit.php?latex=n%5Ed#0) Funktionsauswertungen. Dies nennt man den **Fluch der Dimensionalität (Curse of Dimensionality)**. Bei [](https://www.codecogs.com/eqnedit.php?latex=d%20%3E%204#0) kapitulieren herkömmliche Systeme.

### **Der stochastische Ausweg**

Die **Monte-Carlo-Integration** formuliert das Integrationsproblem elegant in ein Problem der Wahrscheinlichkeitstheorie um. Wir betrachten eine gleichverteilte Zufallsvariable [](https://www.codecogs.com/eqnedit.php?latex=X#0) auf dem Definitionsbereich [](https://www.codecogs.com/eqnedit.php?latex=%5COmega#0) mit der Wahrscheinlichkeitsdichte [](https://www.codecogs.com/eqnedit.php?latex=p\\(x\\)%20%3D%201%2FV#0), wobei [](https://www.codecogs.com/eqnedit.php?latex=V%20%3D%20%5Cint_%7B%5COmega%7D%201%20%5C%2C%20dx#0) das Gesamtvolumen des Raums darstellt. Das Integral läßt sich nun als Erwartungswert ausdrücken:

[](https://www.codecogs.com/eqnedit.php?latex=I%20%3D%20V%20%5Cint_%7B%5COmega%7D%20g\\(x\\)%20p\\(x\\)%20%5C%2C%20dx%20%3D%20V%20%5Ccdot%20%5Cmathbb%7BE%7D%5Bg\\(X\\)%5D#0)

Nach dem **Starken Gesetz der großen Zahlen** konvergiert der empirische Mittelwert von [](https://www.codecogs.com/eqnedit.php?latex=N#0) unabhängig und identisch verteilten (i.i.d.) Stichproben [](https://www.codecogs.com/eqnedit.php?latex=X_i#0) im Grenzwert gegen den wahren Erwartungswert:

[](https://www.codecogs.com/eqnedit.php?latex=%5Chat%7BI%7D_N%20%3D%20%5Cfrac%7BV%7D%7BN%7D%20%5Csum_%7Bi%3D1%7D%5E%7BN%7D%20g\\(X_i\\)%20%5Cxrightarrow%7BA.S.%7D%20I#0)

Das mathematische Wunder liegt in der Konvergenzgeschwindigkeit, die durch den **Zentralen Grenzwertsatz** diktiert wird. Der statistische Fehler der Schätzung verhält sich wie:

[](https://www.codecogs.com/eqnedit.php?latex=%5Ctext%7BError%7D%20%5Csim%20%5Cmathcal%7BO%7D%5Cleft\\(%5Cfrac%7B%5Csigma%7D%7B%5Csqrt%7BN%7D%7D%5Cright\\)#0)

wobei [](https://www.codecogs.com/eqnedit.php?latex=%5Csigma#0) die Standardabweichung der Funktion [](https://www.codecogs.com/eqnedit.php?latex=g\\(X\\)#0) beschreibt. **Diese Fehlerschranke ist vollkommen unabhängig von der Dimension** [](https://www.codecogs.com/eqnedit.php?latex=d#0)**.** Egal ob Sie ein Integral in einer Dimension oder in einem 100-dimensionalen Raum berechnen – die Konvergenzrate bleibt [](https://www.codecogs.com/eqnedit.php?latex=%5Cfrac%7B1%7D%7B%5Csqrt%7BN%7D%7D#0).

💡 **Interessanter Fakt: Ein Onkel in Monaco und eine Grippe**

Die Monte-Carlo-Methode wurde in den 1940er Jahren von dem Mathematiker Stanislaw Ulam erfunden, als er wegen einer Gehirnentzündung im Bett lag und aus Langeweile *Solitaire* spielte. Er wollte die Gewinnwahrscheinlichkeit berechnen, merkte aber, dass die reine Kombinatorik ihn mathematisch erschlug. Also dachte er sich: "Warum spiele ich es nicht einfach 100-mal rein experimentell durch?" Als er seinem Kollegen John von Neumann davon erzählte, bauten sie daraus ein geheimes Tool für das Manhattan-Projekt. Den Codenamen **\"Monte Carlo\"** wählten sie, weil Ulams Onkel sich regelmäßig Geld von Verwandten lieh, um es im berühmten Casino von Monte Carlo zu verspielen\\!

## **2. Stochastische Business-Revenue-Modelle & Risikomanagement**

In realen Systemen – seien es Lieferketten, Serverauslastungen oder Finanzströme – sind Eingangsvariablen selten fix. Ein robustes **Monte-Carlo-Business-Modell** ersetzt statische Schätzwerte durch kontinuierliche Wahrscheinlichkeitsverteilungen:

- **Normalverteilung (**[](https://www.codecogs.com/eqnedit.php?latex=%5Cmathcal%7BN%7D#0)**):** Ideal für aggregierte Größen (z. B. Marktnachfrage), bei denen viele unabhängige Effekte zusammenwirken (Zentraler Grenzwertsatz).
- **Log-Normalverteilung:** Da Kosten, Schadenssummen oder Asset-Preise niemals negativ werden können und oft rechtsschiefige, langschwänzige (Fat-Tail) Verteilungen aufweisen, transformiert man die Variable logarithmisch:   
[](https://www.codecogs.com/eqnedit.php?latex=%5Cln\\(C\\)%20%5Csim%20%5Cmathcal%7BN%7D\\(%5Cmu%2C%20%5Csigma%5E2\\)#0).  
- **Gleichverteilung (**[](https://www.codecogs.com/eqnedit.php?latex=%5Cmathcal%7BU%7D#0)**):** Wird genutzt, wenn lediglich feste Ober- und Untergrenzen bekannt sind, jedoch kein Wissen über eine Häufung existiert (z. B. regulatorische Strafsätze).

Durch das millionenfache Durchspielen dieser kombinierten Verteilungen generieren wir eine empirische Verteilungsfunktion für das Endergebnis. Daraus extrahieren wir das **Value-at-Risk** **(**[](https://www.codecogs.com/eqnedit.php?latex=VaR_%5Calpha#0)**)****.** Das [](https://www.codecogs.com/eqnedit.php?latex=VaR_%7B95%5C%25%7D#0) definiert die Schadensgrenze, die in den schlechtesten 5% aller simulierten Zukünfte unterschritten wird – eine fundamentale Metrik für die Systemstabilität.

💡 **Lustiger Fakt: Der ertrunkene Statistiker**

Viele Unternehmen planen bis heute mit dem sogenannten "Most Likely"-Szenario (dem wahrscheinlichsten Mittelwert). Ökonomen nennen das Phänomen, dass das Rechnen mit Durchschnittswerten fast immer in der Katastrophe endet, die *Flaw of Averages*. Ein berühmter Statistiker-Witz fasst das Problem perfekt zusammen: *Ein Statistiker, der nicht schwimmen konnte, wollte einen Fluss überqueren. Er war völlig beruhigt, als er erfuhr, dass der Fluss im Durchschnitt nur 1 Meter tief ist. Auf halbem Weg trat er in ein 4 Meter tiefes Loch und ertrank.* Genau vor diesem Loch schützt uns die Monte-Carlo-Simulation.

## **3. Markov-Ketten in dynamischen Systemen**

Systeme verändern sich über die Zeit. Wenn die Zukunft eines Systems nur von seinem aktuellen Zustand abhängt und unabhängig von der Vorgeschichte ist, sprechen wir von der **Markov-Eigenschaft** (Gedächtnislosigkeit). Eine diskrete Markov-Kette wird durch eine Übergangsmatrix [](https://www.codecogs.com/eqnedit.php?latex=P#0) beschrieben, wobei jedes Element [](https://www.codecogs.com/eqnedit.php?latex=P_%7Bij%7D#0) die Wahrscheinlichkeit definiert, vom Zustand [](https://www.codecogs.com/eqnedit.php?latex=i#0) in den Zustand [](https://www.codecogs.com/eqnedit.php?latex=j#0) zu wechseln: 

[](https://www.codecogs.com/eqnedit.php?latex=P_%7Bij%7D%20%3D%20%5Cmathbb%7BP%7D\\(X_%7Bt%2B1%7D%20%3D%20j%20%5Cmid%20X_t%20%3D%20i\\)#0)

In dynamischen KI- und Wirtschaftsumgebungen sind diese Matrizen jedoch selten konstant. Exogene Schocks – sogenannte **Black Swan Events** – verändern die Struktur des Systems transient. Mathematisch bedeutet dies eine zeitabhängige Modifikation der Übergangswahrscheinlichkeiten [](https://www.codecogs.com/eqnedit.php?latex=P\\(t\\)#0). Die Herausforderung besteht darin, Algorithmen zu entwickeln, die den Übergang in katastrophale Absorptionszustände (z. B. Insolvenz, Systemcrash) simulieren und die Resilienz des Gesamtsystems quantifizieren.

💡 **Interessanter Fakt: Russische Gedichte statt Quantenphysik**

Man könnte meinen, Andrei Markov hätte seine berühmten Ketten erfunden, um das Wetter, Aktien oder subatomare Teilchen zu modellieren. Weit gefehlt\\! Markov war ein leidenschaftlicher Linguist. Er erfand die Theorie 1913, um die Abfolge von Buchstaben in der russischen Literatur zu analysieren. Er verbrachte Monate damit, manuell **20.000 Buchstaben** aus Alexander Puschkins Versroman *Eugen Onegin* zu zählen, um zu beweisen, dass auf einen Konsonanten mit einer messbar höheren Wahrscheinlichkeit ein Vokal folgt als auf einen weiteren Konsonanten. Ihre Finanz- und KI-Simulationen basieren also im Kern auf russischer Poesie.

## **4. Skalierung von Zufallsprozessen: Zustandslosigkeit mit JAX**

Warum nutzen wir im KI-Zeitalter kein klassisches NumPy oder MATLAB für riesige stochastische Simulationen? Der Grund liegt in der Architektur moderner Beschleuniger (GPUs/TPUs).

### **Das Problem: Zustandbehaftete PRNGs**

Klassische Zufallsgeneratoren (wie in NumPy) basieren auf einem globalen, mutierbaren Zustand (State). Ein Aufruf von np.random.rand() liest den aktuellen Seed, verändert ihn intern und gibt den Wert zurück:

[](https://www.codecogs.com/eqnedit.php?latex=%5Ctext%7BState%7D_%7Bt%2B1%7D%2C%20X%20%3D%20f\\(%5Ctext%7BState%7D_t\\)#0)

Auf massiv paralleler Hardware führt dies zu massiven Performance-Einbrüchen, da Tausende von Kernen gleichzeitig auf denselben globalen Speicherbereich zugreifen müssten (Race Conditions). Zudem wird das Prinzip der **Reproduzierbarkeit** im asynchronen Betrieb unmöglich.

### **Die Lösung: Der zustandslose JAX-Ansatz**

JAX erzwingt funktionale Reinheit (Pure Functions). Der Zufallszustand wird explizit als unveränderliches Array – der PRNGKey – übergeben. Der Key wird niemals im Hintergrund modifiziert. Wenn Sie neue Zufallswerte benötigen, müssen Sie den Schlüssel explizit mittels jax.random.split() deterministisch verzweigen (forken):

```
                             [ Master Key ]  
                                      |  
                +------------+------------+  
                |                                 |  
          [ Subkey A ]                      [ Subkey B ]  
                |                                    |  
      (Zufallsvariable 1)             (Zufallsvariable 2)  
```

Diese funktionale Reinheit erlaubt es JAX, die gesamte Simulationsschleife mittels jax.vmap (Vectorized Map) zu parallelisieren. Statt eine Million Pfade nacheinander in einer Python-Schleife abzuarbeiten, transformiert der XLA-Compiler den Code so, dass Hunderte von Pfaden gleichzeitig auf den Vektorregistern der GPU ausgeführt werden. Ergänzt durch jax.lax.scan für sequentielle Zeitschritte (wie bei Markov-Ketten) erreichen wir Simulationsgeschwindigkeiten, die klassische CPU-Strukturen um den Faktor 100 bis 1000 übertreffen.

💡 **Lustiger (und gefährlicher) Fakt: Täglich grüßt das Murmeltier**

JAX nutzt für seine zustandslosen Keys den *Threefry*-Algorithmus – eine Methode, die eigentlich aus der militärischen Kryptographie stammt (ein abgewandelter Blockchiffre). Das Erzeugen von Zufallszahlen ist in JAX also mathematisch gesehen das "Rückwärts-Entschlüsseln" von Zählern. Das führt zu einer fiesen Falle für JAX-Anfänger: Wenn Sie vergessen, den Key zu splitten, und denselben Key in einer Schleife wiederverwenden, spuckt JAX exakt dieselbe Zufallszahl aus – und zwar jedes einzelne Mal. Ihre "stochastische" Simulation verwandelt sich dann blitzschnell in eine völlig statische, fehlerfreie Zeitschleife\\!

## **📖 Interessante Literaturhinweise**

Für ein tieferes Verständnis der stochastischen Modellierung und ihrer Skalierung werden folgende Werke dringend empfohlen:

### **Zur Monte-Carlo-Integration und stochastischen Methoden:**
- **Robert, C. P., & Casella, G. (2004).** *Monte Carlo Statistical Methods*. Springer Science & Business Media. <https://mcube.lab.nycu.edu.tw/~cfung/docs/books/robert2004monte_carlo_statistical_methods.pdf>  
*Das Standardwerk schlechthin. Exzellent für die mathematischen Beweise hinter Konvergenzraten und fortgeschantren Sampling-Verfahren (MCMC).*
- **Kroese, D. P., Taimre, T., & Botev, Z. I. (2013).** *Handbook of Monte Carlo Methods*. John Wiley & Sons.  
*Sehr praxisnah mit Fokus auf Algorithmen und konkreten Implementierungsstrategien für Ingenieure.*

### **Zu Business-Simulationen und Finanzrisiko:**
- **Glasserman, P. (2003).** *Monte Carlo Methods in Financial Engineering*. Springer Science & Business Media.  
*Die absolute Bibel für die Anwendung von Monte-Carlo-Methoden zur Risikobewertung, Pfadsimulation und Value-at-Risk-Berechnung.*

### **Zu Markov-Ketten und dynamischen Systemen:**
- **Norris, J. R. (1998).** *Markov Chains*. Cambridge University Press. <https://cape.fcfm.buap.mx/jdzf/cursos/procesos/libros/norris.pdf>  
*Ein unglaublich zugängliches und dennoch mathematisch präzises Buch über diskrete und kontinuierliche Markov-Prozesse.*
- **Taleb, N. N. (2007).** *The Black Swan: The Impact of the Highly Improbable*. Random House. <https://www.stat.berkeley.edu/~aldous/157/Books/Black_Swan-sub.pdf>  
*Kein Lehrbuch, sondern eine philosophisch-ökonomische Abhandlung, die das Bewusstsein dafür schärft, warum klassische Normalverteilungen bei extremen Systemschocks versagen.*

### **Zur Skalierung und High-Performance JAX:**
- **JAX Reference Documentation.** *Common Gotchas in JAX: Random Numbers*. (Online verfügbar unter <https://jax.readthedocs.io/>).  
*Pflichtlektüre, um das concept des pseudorandom number generation (PRNG) Splittings im Detail zu verinnerlichen.*
- **Google Developer Docs.** *Antigravity Ecosystem & Agentic Skills Workspace (v2.0, 2026).* (Verfügbar unter <https://antigravity.google/docs/skills>).  
*Leitfaden zur Verbindung von mathematischen Simulations-Pipelines mit autonomen Multi-Agenten-Systemen im modernen Antigravity Workspace.*"""

THEORY_W7 = """## **Woche 7: Das kognitive Orakel (LLMs, Frontier AI & Gemini API)**

### **Von der stochastischen Simulation zur semantischen Intelligenz**

Willkommen auf der kognitiven Ebene des *Neo-Simulacrums*. In der vergangenen Woche haben Sie in der Vorlesung zu **\"Woche 6: Die Domäne des Chaos\"** gelernt, wie man stochastische Zufallsprozesse mit massiv parallelen JAX-Engines algorithmisch bändigt. Doch reine numerische Beschleunigung hat ein fundamentales Limit: Zahlen allein sind kognitiv blind. Eine High-Performance-Simulation, die Terabytes an rohen Datenpunkten ausspuckt, benötigt immer noch ein menschliches Gehirn, um Anomalien zu interpretieren, physikalische Gesetze zu validieren und Parameter strategisch anzupassen.

In dieser Woche brechen wir diese Barriere auf. Wir schlagen die Brücke von der reinen Mathematik zur semantischen Intelligenz. Sie werden lernen, modernste **Frontier AI** direkt in Ihre Simulationsketten zu integrieren. Mithilfe der **Google Gemini API** statten wir unsere autonomen Akteure mit der Fähigkeit aus, Simulationsgraphen visuell zu analysieren, Logdateien semantisch zu verstehen und eigenständig Optimierungsschleifen zu steuern. Der Code generiert die Daten – aber das Foundation Model versteht die Realität dahinter.

## **🧠 Die Evolution der Giganten: Ein historischer Rückblick**

Wir stehen heute im Jahr 2026 auf den Schultern von Giganten. Die Fähigkeit von KI-Modellen, Code zu verstehen und komplexe physikalische Systeme zu analysieren, ist das Ergebnis einer rasanten, historischen Evolutionskette <https://artificialanalysis.ai/models>:

- **OpenAI GPT-Serie:** Der Urknall der modernen GenAI. Von GPT-2 bis hin zu den bahnbrechenden Meilensteinen von GPT-3 und GPT-4 – diese Modelle bewiesen erstmals, dass durch reine Skalierung von Parametern und Daten emergente Fähigkeiten wie logisches Denken und Kontextverständnis entstehen.
- **OpenAI Codex:** Ein historischer Wendepunkt für Ingenieure. Als direktes Derivat von GPT zeigte Codex der Welt, dass KI nicht nur menschliche Sprache, sondern auch die formale Syntax von Programmiersprachen meistern kann. Es legte das Fundament für automatisierte Code-Generierung, wie wir sie heute in der JAX-Entwicklung nutzen.
- **Google Gemini-Familie & Gemini 3.5**: Google etabiert mit der Gemini 3.5 Modellreihe (angeführt von Gemini 3.5 Flash, veröffentlicht im Mai 2026) ein neues Paradigma der agentischen Performance. Gemini 3.5 Flash liefert "Frontier Intelligence" bei außergewöhnlich hoher Verarbeitungsgeschwindigkeit (vierfach schneller als vergleichbare Modelle) und übertrifft Vorgängermodelle bei komplexen Codierungs- und Interaktionsbenchmarks wie Terminal-Bench 2.1 (76,2 %) und MCP Atlas (83,6 %). Es integriert natives, verschlüsseltes Denken (Thinking) direkt in den API-Interaktionsfluss.
- **Anthropic (Claude-Dynastie):** Anthropic revolutionierte den Markt mit zwei Kern- Fokusse: *Constitutional AI* (fortgeschrittene Sicherheits- und Alignment-Architekturen) und dem massiven Ausbau von *Kontextfenstern*. Plötzlich konnten Agenten die gesamte Dokumentation eines Simulations-Stacks auf einmal im Gedächtnis behalten.
- **Mistral AI:** Die Pioniere der Open-Weights-Effizienz. Mit Modellen wie *Mixtral* und der Perfektionierung von *Mixture of Experts (MoE)* bewies das europäische Team, dass hocheffiziente, pfeilschnelle Modelle auch lokal auf Entwickler-Maschinen laufen können, ohne Giganten-Infrastruktur zu benötigen.
- **Meta (Von Llama zu Muse Spark):** Die historische Evolution von Meta begann mit der wegweisenden Veröffentlichung von LLaMA im Februar 2023. Über Llama 2 (Juli 2023), Llama 3 (April 2024), Llama 3.1 (Juli 2024, welches den Kontext auf 128k erweiterte), Llama 3.3 und Llama 4 (April 2025) baute Meta das leistungsfähigste Open-Source-Ökosystem auf. Im April 2026 folgte durch die Meta Superintelligence Labs die Veröffentlichung von Muse Spark als bahnbrechender Ersatz für Llama. Muse Spark erreicht hervorragende 89,5 % auf dem GPQA-Diamond Benchmark und bricht die Grenzen klassischer Open-Source-Kognition.
- **xAI Grok-Serie**: Die von Elon Musk gegründete xAI trieb die Evolution von Grok-0 (Aug 2023), Grok-1 (November 2023) und Grok-2 (August 2024) rasant voran. Über Grok-3 (Februar 2025) und Grok-4 (Juli 2025) kamen Meilensteine wie Grok-4.20 (Februar 2026) und das im April 2026 veröffentlichte Grok 4.3 Beta. Grok zeichnet sich durch seine tiefe Integration in das X-Ecosystem, Echtzeit-Websuche und den hochperformanten "Think"-Modus zur Lösung komplexer logischer Ketten aus.
- **Chinesische Open-Source-Modelle (Qwen, DeepSeek & Co.):** Die jüngste Welle der Disruption. Mit radikalen Architektur-Optimierungen haben diese Modelle bewiesen, dass Frontier-Level-Reasoning und komplexe mathematische Code-Generierung zu einem Bruchteil der globalen Rechenkosten skalierbar sind. Modelle wie DeepSeek-V3 reduzierten die Trainingskosten dramatisch (5,6 Millionen USD vs. bis zu 191 Millionen USD für vergleichbare westliche Modelle). Durch extrem effiziente Architekturen wie Multi-head Latent Attention (MLA) und spezialisierte Mixture-of-Experts (MoE) fordern sie die Marktführer heraus. Auf Augenhöhe bewegt sich Moonshots Kimi K2.6, welches im Frühjahr 2026 als das stärkste frei verfügbare Open-Weight-Modell gilt.

## **🛠️ Die Mathematik des Verstehens: Der Transformer-Mechanismus**

Die kognitive Schicht, die wir heute über die Gemini API ansprechen, basiert fundamental auf der Transformer-Architektur (Vaswani et al., 2017). Der Mechanismus der **Self-Attention** erlaubt es dem Modell, die Beziehungen aller Datenpunkte in einem Kontextfenster gleichzeitig zu berechnen, anstatt Informationen wie alte RNNs sequentiell abzuarbeiten.

Die mathematische Essenz der *Scaled Dot-Product Attention* lautet:

[](https://www.codecogs.com/eqnedit.php?latex=Attention\\(Q%2C%20K%2C%20V\\)%20%3D%20%5Ctext%7Bsoftmax%7D%5Cleft\\(%5Cfrac%7BQK%5ET%7D%7B%5Csqrt%7Bd_k%7D%7D%5Cright\\)V#0)

Für jedes Token innerhalb einer Eingabesequenz berechnet das Modell drei spezifische Vektorrepräsentationen über gelernte Projektionsmatrizen:

- **Query-Vektor ($Q$):** Repräsentiert die Suchanfrage eines Tokens, das nach semantisch relevanten Informationen bei anderen Tokens sucht.
- **Key-Vektor ($K$):** Repräsentiert das Charakteristikum oder das Indizierungsmerkmal jedes Tokens, welches mit den Queries abgeglichen wird.
- **Value-Vektor ($V$):** Beinhaltet die tatsächliche semantische Information des Tokens, die in die Aktualisierung der Repräsentation einfließt, sobald eine Übereinstimmung zwischen Query und Key vorliegt.

Die Division durch die Quadratwurzel der Dimension des Key-Vektors ($\sqrt{d_k}$) verhindert, dass die Skalarprodukte bei großen Dimensionen extrem anwachsen, was zu verschwindenden Gradienten in der nachgeschalteten Softmax-Funktion führen würde.

### **Kontextsensitive Repräsentation und linguistische Ambiguität**

Klassische Einbettungsverfahren (wie word2vec) generieren statische Vektoren, bei denen dasselbe Wort unabhängig vom Kontext stets dieselbe mathematische Repräsentation besitzt. Dies scheitert bei polysemen Begriffen. Der Self-Attention-Mechanismus hingegen generiert dynamische, kontextsensitive Einbettungen.

Ein klassisches didaktische Beispiel verdeutiert diesen Vorgang:
- *Satz A: „Das Tier überquerte die Straße nicht, weil **es** zu müde war.“*
- *Satz B: „Das Tier überquerte die Straße nicht, weil **es** zu breit war.“*

Für eine präzise Übersetzung oder logische Analyse muss das Pronomen „es“ korrekt zugeordnet werden. Der menschliche Verstand nutzt dafür Kontextbeziehungen. Der Transformer-Mechanismus repliziert dies mathematisch: Im Satz A erzeugt das Token „müde“ eine hohe Affinität zur Query des Pronomens „es“ und lenkt die Aufmerksamkeit über das Skalarprodukt der Vektoren gezielt auf das Substantiv „Tier“. Im Satz B hingegen erzeugt das Token „breit“ eine starke mathematische Ausrichtung zur Key-Repräsentation von „Straße“. Die resultierenden kontextsensitiven Einbettungen verändern die Vektoren im euklidischen Raum so, dass das Modell im ersten Fall eine Verbindung zu belebten Objekten und im zweiten Fall zu geometrischen Strukturen herstellt.

## **Architektonische Innovationen zur Effizienzsteigerung bei massiver Skalierung**

Mit der Skalierung von Modellen zu Frontier-Level-Systemen steigen die Anforderungen an den Arbeitsspeicher der Hardware exponentiell an. Zwei architektonische Entwicklungen sind hierbei von herausragender Bedeutung: Multi-Head Latent Attention und Mixture of Experts.

### **Multi-Head Latent Attention (MLA)**

Während der autoregressiven Textgenerierung (Inferenz) müssen die berechneten Schlüssel ($K$) und Werte ($V$) aller vorherigen Tokens im Arbeitsspeicher gehalten werden, um redundante Berechnungen zu vermeiden. Dieser Key-Value-Cache (KV-Cache) wächst linear mit der Sequenzlänge und blockiert enorme Speicherkapazitäten auf den Beschleunigerchips.

Die Multi-Head Latent Attention (MLA) löst dieses Problem durch eine mathematische Kompression niedrigen Rangs (Low-Rank Joint Compression). Anstatt die vollen, hochdimensionalen Vektoren im Cache zu speichern, projiziert MLA die Schlüssel und Werte in einen signifikant kleineren latenten Raum.

Die mathematische Formulierung der Kompression lautet:
[](https://www.codecogs.com/eqnedit.php?latex=c_t%5E%7BKV%7D%20%3D%20W%5E%7BDK%7D%20h_t#0)

Hierbei repräsentiert $h_t$ den Eingangsvektor am Zeitschritt $t$. Die Matrix $W^{DK}$ is die Down-Projection-Matrix, welche den Vektor auf die latente Dimension $d_c$ komprimiert, wobei $d_c \ll d_k n_h$ gilt (mit $d_k$ als Dimension des einzelnen Aufmerksamkeitskopfes und $n_h$ als Anzahl der Köpfe). Im Cache wird nur noch der Vektor $c_t^{KV}$ hinterlegt.

Während der Aufmerksamkeitsberechnung werden die Schlüssel und Werte über Up-Projection-Matrizen rekonstruiert:
[](https://www.codecogs.com/eqnedit.php?latex=k_t%5E%7BR%7D%20%3D%20W%5E%7BUK%7D%20c_t%5E%7BKV%7D#0)
[](https://www.codecogs.com/eqnedit.php?latex=v_t%5E%7BR%7D%20%3D%20W%5E%7BUV%7D%20c_t%5E%7BKV%7D#0)

Um die Aktivierungsspeicher während des Trainings zu minimieren, komprimiert MLA optional auch die Queries:
[](https://www.codecogs.com/eqnedit.php?latex=c_t%5EQ%20%3D%20W%5E%7BDQ%7D%20h_t#0)
[](https://www.codecogs.com/eqnedit.php?latex=q_t%5ER%20%3D%20W%5E%7BUQ%7D%20c_t%5EQ#0)

### **Mixture of Experts (MoE) und numerische Optimierungen**

Zur Skalierung der Modellkapazität ohne proportionalen Anstieg der Rechenkosten pro Token etablierten sich Mixture-of-Experts-Architekturen. Ein neuronales MoE-Modell ersetzt die klassischen dichten FFN-Schichten durch eine Vielzahl spezialisierter FFN-Blöcke (Experten). Ein statistisch trainiertes Gating-Netzwerk berechnet für jedes Token die Affinitäten zu den Experten und leitet das Signal dünnbesetzt (sparse) weiter.

Moderne Architekturen wie DeepSeek-V3 oder Mixtral führten grundlegende Optimierungen ein:
- **Gemeinsame Experten (Shared Experts):** Einige permanent aktivierte Experten erlernen fundamentale, domänenübergreifende Repräsentationen (z. B. Syntax oder grundlegende Logik), während selektiv geroutete Experten hochgradig spezifisches Spezialwissen akkumulieren.
- **Dynamisches Load Balancing:** Um den 'Routing-Kollaps' (Überlastung einzelner Experten bei Vernachlässigung anderer) zu verhindern, nutzten frühere Architekturen (wie the Switch Transformer) starre Hilfsverluste im Training. Moderne Ansätze eliminieren diese Hilfsverluste und passen stattdessen während des Betriebs dynamisch einen Bias-Term auf den Gating-Werten an, wodurch die Modellqualität nicht durch künstliche Balance-Kriterien beeinträchtigt wird.
- **FP8-Präzision beim Vortraining:** Durch das Training im FP8-Format (8-Bit-Fließkommazahl) wird der Speicherbedarf halbiert und der Durchsatz verdoppelt, während die relative Verlustabweichung stabil unter 0.25% gehalten wird.

## **Hardware-Infrastruktur und Software-Schnittstellen (Gemini 3.5 API)**

Die hocheffiziente Ausführung von Modellen erfordert ein enges Zusammenspiel zwischen optimierter Software und spezialisierter Hardware. Google setzt hierbei auf eine integrierte vertikale Strategie mit Tensor Processing Units (TPUs) und dem JAX-Framework.

### **TPU-Infrastruktur und die JAX-Brücke**

Für das großflächige Training und den Inferenzbetrieb wurde eine Spezialisierung der Hardware-Infrastruktur vorgenommen: Die TPU 8t ist für massives, global verteiltes Pretraining optimiert und entkoppelt das Training von einzelnen Rechenzentren mittels JAX und dem Pathways-System. Die TPU 8i is dagegen speziell für latenzkritischen Inferenzbetrieb und die Ausführung komplexer, multimodaler Agentenketten optimiert. Das Framework JAX kommuniziert über jaxlib und die Backend-Bibliothek libtpu.so (TPU Runtime) direkt mit der Hardware, was extreme Skalierungseffekte ermöglicht (wie das Training von Gemma auf über 6 Billionen Tokens).

### **Die moderne Schnittstelle: Google GenAI SDK und Gemini 3.5 Flash**

In der Praxis erfolgt die Anbindung kognitiver Fähigkeiten über das Ende 2024 eingeführte **Google GenAI SDK** (Bibliothek google-genai), welches die veraltete google-generativeai-Bibliothek vollständig ersetzt. Das neue SDK führt eine einheitliche Client-Struktur über das zentrale Client-Objekt ein:

```python
from google import genai  
from pydantic import BaseModel  
  
# Automatische API-Key-Erkennung ueber die Umgebungsvariable GEMINI_API_KEY  
client = genai.Client()  
```

Für die Einbindung in physikalische Kontrollschleifen und Simulationspipelines bietet die Gemini 3.5 Generation (wie **Gemini 3.5 Flash**) fundamentale Verhaltensänderungen und erweiterte Steuerungen:

1. **Optimierte Standard-Hyperparameter:** Es wird dringend empfohlen, die Standardwerte für temperature (1.0) und top_p (0.95) nicht mehr verändern, da die Denkprozesse (Thinking) der Gemini 3.x Modelle explizit auf diese Werte optimiert sind.
2. **Gesteuertes Denken (Thinking Level):** Anstelle der veralteten Token-Kappung über thinking_budget wird nun die feingranulare Steuerung thinking_level verwendet (Optionen: minimal, low, medium, high), um das Gleichgewicht zwischen Kognitionstiefe, Latenz und API-Kosten präzise zu steuern.
3. **Typensichere strukturierte Ausgaben:** Die Enforcierung von JSON-Schemas erfolgt nativ über Pydantic-Klassen direkt im API-Aufruf:

```python
class SimulationParameter(BaseModel):  
    damping_coefficient: float  
    stability_state: str  
  
response = client.models.generate_content(  
    model="gemini-3.5-flash",  
    contents="Analysiere das Protokoll...",  
    config={  
        "response_mime_type": "application/json",  
        "response_schema": SimulationParameter,  
    }  
)  
# Direkter Zugriff auf das geparste Pydantic-Objekt  
parsed_data = response.parsed  
```

Für Sie als Entwickler bedeutet das: Foundation Models besitzen ein tiefes, topologisches Verständnis von Code-Strukturen und kausalen Zusammenhängen. Kombiniert mit **multimodaler Perzeption** (Bild + Text) kann Gemini ein von Matplotlib gerendertes PNG-Bild einer Simulation betrachten und sofort erkennen, ob das System stabil oszilliert oder chaotisch divergiert.

## **📖 Pflichtlektüre für Woche 7**

- **Die theoretische Basis (Architektur):**  
  Vaswani, A., et al. (2017). *Attention Is All You Need*.  
  **ArXiv-Link:** <https://arxiv.org/pdf/1706.03762>  
  *Fokus:* Verstehen Sie das Konzept der Multi-Head Attention und warum diese Architektur komplexe Sequenzmuster ohne Informationsverlust über lange Kontexte hinweg behalten kann.
- **Die praktische Schnittstelle (API-Integration):**  
  Google Developer Documentation. *Gemini API Quickstarts & Structured Outputs*.  
  **Dokumentations-Link:** <https://ai.google.dev/gemini-api/docs>  
  *Fokus:* Machen Sie sich mit dem Funktionsaufruf (Tool Calling), Multimodal Prompts (Bild + Text) und der Implementierung von response_schema vertraut, um saubere JSON-Rückgaben zu garantieren.
- **Das Agentic-Scaling-Framework (Advanced Reference):**  
  Google AI-Hypercomputer Core. *Tunix Reference Repository for Post-Training and Agentic RL on TPUs*.  
  **GitHub-Link:** <https://github.com/google/tunix>  
  *Fokus:* Studieren Sie konzeptionell, wie Reinforcement-Learning-Verfahren im Post-Training genutzt werden, um Modelle für hochpräzise Aufgaben in autonomen Software-Umgebungen zu optimieren.

## **📖 Interessante Literaturhinweise**

1. History of LLMs: Complete Timeline & Evolution (1950-2026) - Toloka AI, accessed June 4, 2026, <https://toloka.ai/blog/history-of-llms/>
2. Self Attention in Transformers - Outcome School, accessed June 4, 2026, <https://outcomeschool.com/blog/self-attention-in-transformers>
3. Self-Attention Explained: The Cocktail Party Effect in LLMs | PythonAlchemist, accessed June 4, 2026, <https://www.pythonalchemist.com/blog/self-attention-cocktail-party>
4. What is an attention mechanism? | IBM, accessed June 4, 2026, <https://www.ibm.com/think/topics/attention-mechanism>
5. Mathematical details behind self-attention | Reflections, accessed June 4, 2026, <https://lakshyamalhotra.github.io/2024/06/10/Mathematical-details-behind-self-attention.html>
6. Self-Attention Explained with Code | Towards Data Science, accessed June 4, 2026, <https://towardsdatascience.com/contextual-transformer-embeddings-using-self-attention-explained-with-diagrams-and-python-code-d7a9f0f4d94e/>
7. Multi-head Latent Attention (MLA): Secret behind the success of DeepSeek Large Language Models | by Nagur Shareef Shaik | Medium, accessed June 4, 2026, <https://medium.com/@shaiknagurshareef/multi-head-latent-attention-mla-secret-behind-the-success-of-deepseek-large-language-models-66612071d756>
8. DeepSeek's Multi-Head Latent Attention - Lior Sinai, accessed June 4, 2026, <https://liorsinai.github.io/machine-learning/2025/02/22/mla.html>
9. What is mixture of experts? | IBM, accessed June 4, 2026, <https://www.ibm.com/think/topics/mixture-of-experts>
10. DeepSeek v3 and R1 Model Architecture: Why it's powerful and economical - Fireworks AI, accessed June 4, 2026, <https://fireworks.ai/blog/deepseek-model-architecture>
11. Mixture of experts - Wikipedia, accessed June 4, 2026, <https://en.wikipedia.org/wiki/Mixture_of_experts>
12. What Is Mixture of Experts (MoE)? How It Works (2026) - Build Fast with AI, accessed June 4, 2026, <https://www.buildfastwithai.com/blogs/mixture-of-experts-moe-explained>
13. I/O 2026: Welcome to the agentic Gemini era - Google Blog, accessed June 4, 2026, <https://blog.google/innovation-and-ai/sundar-pichai-io-2026/>
14. A Developer's Guide to Debugging JAX on Cloud TPUs: Essential Tools and Techniques, accessed June 4, 2026, <https://developers.googleblog.com/a-developers-guide-to-debugging-jax-on-cloud-tpus-essential-tools-and-techniques/>
15. JAX Gemma on Colab TPU - Google, accessed June 4, 2026, <https://colab.research.google.com/github/sanchit-gandhi/notebooks/blob/main/jax_gemma>"""


# ==========================================
# 3. PROCESSING IMPLEMENTATIONS
# ==========================================

def clean_latex(latex):
    latex = urllib.parse.unquote(latex)
    if latex.endswith('#0'):
        latex = latex[:-2]
    elif latex.endswith('#'):
        latex = latex[:-1]
    latex = latex.replace(r'\(', '(').replace(r'\)', ')')
    latex = latex.replace(r'\_', '_')
    # Clean up double backslashes in commands like \\omega -> \omega
    # but keep them if they are not followed by alphabetical chars (e.g. matrices newline \\)
    latex = re.sub(r'\\{2,}([a-zA-Z\{\}])', r'\\\1', latex)
    return latex.strip()

def fix_emojis(text):
    replacements = {
        'ð\x9f\x92\xa1': '💡',
        'ð\x9f\xa7\xa0': '🧠',
        'ð\x9f\x9b\xa0\ufe0f': '🛠️',
        'ð\x9f\x9b\xa0': '🛠️',
        'ð\x9f\x93\x9a': '📚',
        'ð\x9f\x93\x98': '📖',
        'ð\x9f\x93\x97': '📕',
        'ð\x9f\x98\x86': '😆',
        'ðŸ’¡': '💡',
        'ðŸ§ ': '🧠',
        'ðŸ ️': '🛠️',
        'ðŸ ': '🛠️',
        'ðŸ“š': '📚',
        'ðŸ“˜': '📖',
        'ðŸ“—': '📕',
        'ðŸ˜†': '😆',
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def merge_indented_lines(text):
    lines = text.split('\n')
    merged_lines = []
    in_code = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            merged_lines.append(line)
            continue
            
        if in_code:
            merged_lines.append(line)
            continue
            
        # Check if line is indented and is a continuation of a list item or paragraph
        if (line.startswith('    ') or line.startswith('  ')) and stripped and merged_lines:
            prev = merged_lines[-1]
            separator = " "
            if prev.endswith('  '):
                separator = "<br>"
            merged_lines[-1] = prev.rstrip() + separator + stripped
        else:
            merged_lines.append(line)
            
    return '\n'.join(merged_lines)

def strip_leading_emojis(text):
    return re.sub(r'^[\s📖🧠🛠️⚡💡📚🎯🏁⚙️◆◇❖]*', '', text).strip()

def preprocess_markdown(text):
    text = fix_emojis(text)
    
    # Merge indented list continuation lines first
    text = merge_indented_lines(text)
    
    # Replace CodeCogs links with a robust nested parenthesis scanner
    start_str = "[](https://www.codecogs.com/eqnedit.php?latex="
    while True:
        idx = text.find(start_str)
        if idx == -1:
            break
            
        paren_start = idx + 2
        balance = 0
        paren_end = -1
        for j in range(paren_start, len(text)):
            char = text[j]
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance == 0:
                    paren_end = j
                    break
        
        if paren_end == -1:
            text = text.replace(start_str, " ", 1)
            continue
            
        latex_start_offset = len("https://www.codecogs.com/eqnedit.php?latex=")
        latex_url = text[paren_start + 1 + latex_start_offset : paren_end]
        latex = clean_latex(latex_url)
        
        # Check if this CodeCogs link is on a line by itself (indicating a block formula)
        line_start = text.rfind('\n', 0, idx) + 1
        line_end = text.find('\n', paren_end)
        if line_end == -1:
            line_end = len(text)
            
        line_prefix = text[line_start:idx].strip()
        line_suffix = text[paren_end+1:line_end].strip()
        
        if not line_prefix and not line_suffix:
            # Block equation!
            text = text[:line_start] + f"$$ {latex} $$" + text[line_end:]
        else:
            # Inline equation!
            text = text[:idx] + f"\\({latex}\\)" + text[paren_end+1:]
            
    # Normalize double dollar blocks
    text = text.replace('$$$$', '$$')
    
    # Clean escapes in non-code lines
    lines = text.split('\n')
    in_code = False
    for idx_l, line in enumerate(lines):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if not in_code:
            lines[idx_l] = re.sub(r'\\{2,}([a-zA-Z\{\}])', r'\\\1', line)
            lines[idx_l] = lines[idx_l].replace(r'\_', '_')
            
    return '\n'.join(lines)

# ==========================================
# 4. PARSING AND GENERATION LOGIC
# ==========================================

def clean_quiz_text(text):
    text = re.sub(r'\\{2,}([a-zA-Z\{\}])', r'\\\1', text)
    text = text.replace(r'\_', '_').replace(r'\\_', '_')
    return text

def build_quiz(week_id, csv_str):
    lines = [l.strip() for l in csv_str.strip().split('\n')]
    questions = []
    
    for line in lines:
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if not cells or len(cells) < 7:
            continue
        if 'Question' in cells[0] or all(re.match(r'^:?-+:?$', c) for c in cells):
            continue
            
        q_text = clean_quiz_text(cells[0])
        options = [clean_quiz_text(cells[1]), clean_quiz_text(cells[2]), clean_quiz_text(cells[3]), clean_quiz_text(cells[4])]
        options = [opt for opt in options if opt]
        
        correct_str = cells[6].replace(' ', '')
        correct_indices = []
        for val in correct_str.split(','):
            if val.isdigit():
                correct_indices.append(int(val) - 1)
                
        if len(correct_indices) == 1:
            answer_index = correct_indices[0]
        else:
            answer_index = correct_indices
            
        explanation = clean_quiz_text(cells[7]) if len(cells) > 7 else ""
        
        questions.append({
            "question": q_text,
            "options": options,
            "answerIndex": answer_index,
            "explanation": explanation
        })
        
    # Write JSON file
    week_folder = os.path.join(weeks_dir, f"week{week_id}")
    os.makedirs(week_folder, exist_ok=True)
    json_path = os.path.join(week_folder, "quiz.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4, ensure_ascii=False)
    print(f"Generated Week {week_id} Quiz -> {json_path} (Questions: {len(questions)})")


def convert_theory_markdown_to_html(md_text, week_id):
    lines = md_text.split('\n')
    html_lines = []
    
    in_list = False
    in_ordered_list = False
    in_code_block = False
    code_block_lines = []
    
    in_fact_box = False
    fact_title = ""
    
    in_literature_box = False
    
    # Write outer div container
    html_lines.append('<div class="space-y-8">')
    
    # Find the main title and subtitle
    main_title = ""
    main_subtitle = ""
    first_title_idx = -1
    first_subtitle_idx = -1
    
    for idx, l in enumerate(lines):
        s = l.strip()
        if s.startswith('# ') or s.startswith('## '):
            if main_title == "":
                main_title = re.sub(r'\*+', '', s.lstrip('#').strip())
                main_title = strip_leading_emojis(main_title)
                first_title_idx = idx
                sub_scan = idx + 1
                while sub_scan < len(lines) and not lines[sub_scan].strip():
                    sub_scan += 1
                if sub_scan < len(lines) and not lines[sub_scan].strip().startswith('#'):
                    main_subtitle = lines[sub_scan].strip()
                    first_subtitle_idx = sub_scan
                break
                
    # Build Intro Banner
    if main_title:
        html_lines.append('    <!-- Intro Banner -->')
        html_lines.append('    <div class="p-6 glass-card rounded-2xl border-l-4 border-cyan-500 bg-gradient-to-r from-cyan-950/20 to-transparent">')
        html_lines.append(f'        <h3 class="text-xl md:text-2xl font-bold text-white mb-2">{main_title}</h3>')
        if main_subtitle:
            html_lines.append(f'        <p class="text-slate-300 text-sm leading-relaxed">{main_subtitle}</p>')
        html_lines.append('    </div>')
        
    i = 0
    while i < len(lines):
        if i == first_title_idx or i == first_subtitle_idx:
            i += 1
            continue
            
        line = lines[i]
        stripped = line.strip()
        
        # Code block handling
        if stripped.startswith('```'):
            if in_code_block:
                in_code_block = False
                code_content = '\n'.join(code_block_lines)
                code_content = code_content.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # Close lists before code block
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if in_ordered_list:
                    html_lines.append('</ol>')
                    in_ordered_list = False
                    
                html_lines.append(f'<pre class="bg-slate-950 p-4 rounded-xl border border-slate-850 overflow-x-auto text-xs font-mono text-cyan-400 my-4"><code class="language-python">{code_content}</code></pre>')
                code_block_lines = []
            else:
                in_code_block = True
            i += 1
            continue
            
        if in_code_block:
            clean_code_line = re.sub(r'\\\s*$', '', line)
            code_block_lines.append(clean_code_line)
            i += 1
            continue
            
        # Empty lines
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if in_fact_box:
                html_lines.append('    </div>')
                in_fact_box = False
            i += 1
            continue
            
        # Fact box detection: starts with "💡 **" or "💡"
        if stripped.startswith('💡'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if in_fact_box:
                html_lines.append('    </div>')
                in_fact_box = False
                
            in_fact_box = True
            match = re.match(r'^💡\s*\*\*(.*?)\*\*', stripped)
            if match:
                fact_title = match.group(1)
            else:
                fact_title = stripped.replace('💡', '').strip()
                
            fact_title = strip_leading_emojis(fact_title)
            
            html_lines.append('    <div class="p-5 glass-card rounded-xl border-l-4 border-yellow-500 bg-yellow-500/5 my-6 space-y-2">')
            html_lines.append(f'        <h4 class="text-yellow-400 font-bold text-sm flex items-center gap-2"><span>💡</span> {fact_title}</h4>')
            i += 1
            continue
            
        # Heading Section handling (Only ## closes literature cards; ### stays inside)
        if stripped.startswith('##') or stripped.startswith('###'):
            # Close active lists
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            # Close active fact boxes
            if in_fact_box:
                html_lines.append('    </div>')
                in_fact_box = False
                
            header_text = stripped.lstrip('#').strip()
            header_text = re.sub(r'\*+', '', header_text)
            
            is_sub = stripped.startswith('###')
            
            if not is_sub:
                # Close previous literature box if open (since we hit a new H2 section)
                if in_literature_box:
                    html_lines.append('    </div>')
                    in_literature_box = False
                    
                clean_header = strip_leading_emojis(header_text)
                
                # Check if this heading starts a literature block
                if "Literaturhinweise" in header_text or "Pflichtlektüre" in header_text:
                    in_literature_box = True
                    html_lines.append('    <div class="p-6 glass-card rounded-2xl border-t-2 border-t-purple-500/35 bg-purple-950/5 space-y-4 my-8">')
                    html_lines.append(f'        <h4 class="text-purple-400 font-bold text-lg flex items-center gap-2"><span>📚</span> {clean_header}</h4>')
                    i += 1
                    continue
                    
                # Format standard H2
                emoji = "⚡"
                emoji_match = re.match(r'^([^\w\s]+)\s*(.*)$', header_text)
                if emoji_match:
                    emoji = emoji_match.group(1)
                
                color_class = "text-cyan-400"
                if emoji == "🧠":
                    color_class = "text-purple-400"
                elif emoji == "🛠️":
                    color_class = "text-pink-400"
                    
                html_lines.append(f'<h3 class="text-xl md:text-2xl font-extrabold text-white mt-12 mb-4 border-b border-slate-900 pb-2 flex items-center gap-2">')
                html_lines.append(f'    <span class="{color_class}">{emoji}</span> {clean_header}')
                html_lines.append('</h3>')
            else:
                # Format H3 (styled differently if inside a literature card)
                clean_header = strip_leading_emojis(header_text)
                color_class = "text-purple-400" if in_literature_box else "text-cyan-400"
                html_lines.append(f'<h4 class="text-base font-bold {color_class} mt-8 mb-3 flex items-center gap-2">')
                html_lines.append(f'    <span class="text-xs">◆</span> {clean_header}')
                html_lines.append('</h4>')
                
            i += 1
            continue
            
        # Ordered lists
        ordered_match = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if ordered_match:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if not in_ordered_list:
                html_lines.append('<ol class="list-decimal pl-6 text-sm text-slate-300 space-y-3 my-4">')
                in_ordered_list = True
                
            item_text = ordered_match.group(2)
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code class="text-cyan-400 font-mono bg-slate-900/60 px-1.5 py-0.5 rounded text-xs">\1</code>', item_text)
            item_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-cyan-400 hover:underline" target="_blank">\1</a>', item_text)
            # Support raw URL tags like <http://url>
            item_text = re.sub(r'<((https?|ftp)://[^>]+)>', r'<a href="\1" class="text-cyan-400 hover:underline" target="_blank">\1</a>', item_text)
            
            html_lines.append(f'    <li class="leading-relaxed">{item_text}</li>')
            i += 1
            continue
            
        # Bullet lists
        bullet_match = re.match(r'^[-*]\s+(.*)$', stripped)
        if bullet_match:
            if in_ordered_list:
                html_lines.append('</ol>')
                in_ordered_list = False
            if not in_list:
                html_lines.append('<ul class="list-disc pl-6 text-sm text-slate-300 space-y-2.5 my-4">')
                in_list = True
                
            item_text = bullet_match.group(1)
            item_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', item_text)
            item_text = re.sub(r'`(.*?)`', r'<code class="text-cyan-400 font-mono bg-slate-900/60 px-1.5 py-0.5 rounded text-xs">\1</code>', item_text)
            item_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-cyan-400 hover:underline" target="_blank">\1</a>', item_text)
            # Support raw URL tags like <http://url>
            item_text = re.sub(r'<((https?|ftp)://[^>]+)>', r'<a href="\1" class="text-cyan-400 hover:underline" target="_blank">\1</a>', item_text)
            
            html_lines.append(f'    <li class="leading-relaxed">{item_text}</li>')
            i += 1
            continue
            
        # Standard paragraphs
        p_text = stripped
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', p_text)
        p_text = re.sub(r'`(.*?)`', r'<code class="text-cyan-400 font-mono bg-slate-900/60 px-1.5 py-0.5 rounded text-xs">\1</code>', p_text)
        p_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" class="text-cyan-400 hover:underline" target="_blank">\1</a>', p_text)
        # Support raw URL tags like <http://url>
        p_text = re.sub(r'<((https?|ftp)://[^>]+)>', r'<a href="\1" class="text-cyan-400 hover:underline" target="_blank">\1</a>', p_text)
        
        if p_text.startswith('$$') and p_text.endswith('$$'):
            html_lines.append(f'<div class="my-6 overflow-x-auto">{p_text}</div>')
        else:
            html_lines.append(f'<p class="text-sm text-slate-300 leading-relaxed my-3">{p_text}</p>')
            
        i += 1
        
    # File end cleanup
    if in_list:
        html_lines.append('</ul>')
    if in_ordered_list:
        html_lines.append('</ol>')
    if in_fact_box:
        html_lines.append('    </div>')
    if in_literature_box:
        html_lines.append('    </div>')
        
    html_lines.append('</div>')
    return '\n'.join(html_lines)


def update_theory(week_id, md_raw):
    clean_md = preprocess_markdown(md_raw)
    html = convert_theory_markdown_to_html(clean_md, week_id)
    
    week_folder = os.path.join(weeks_dir, f"week{week_id}")
    os.makedirs(week_folder, exist_ok=True)
    html_path = os.path.join(week_folder, "introduction.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated Week {week_id} Theory Introduction -> {html_path}")


# ==========================================
# 5. EXECUTION PIPELINE
# ==========================================

print("=== STARTING SYNC PIPELINE ===")

# Process Quizzes
for wid, raw_csv in QUIZ_DATA.items():
    build_quiz(wid, raw_csv)

# Process Theory Introductions
update_theory(6, THEORY_W6)
update_theory(7, THEORY_W7)

print("=== PIPELINE RUN COMPLETE ===")
