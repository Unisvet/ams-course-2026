// Reusable Quiz Engine for AMS Course 2026

export class QuizEngine {
    constructor(container, quizData, onCompleteCallback) {
        this.container = container;
        this.questions = quizData;
        this.onComplete = onCompleteCallback;
        
        this.currentIndex = 0;
        this.score = 0;
        this.selectedAnswer = null;
        this.isAnswered = false;
        
        this.init();
    }

    init() {
        if (!this.questions || this.questions.length === 0) {
            this.container.innerHTML = `
                <div class="text-center p-8 glass-card rounded-xl">
                    <p class="text-vibrant-textMuted">Kein Quiz für diese Woche verfügbar.</p>
                </div>
            `;
            return;
        }
        this.renderQuestion();
    }

    renderQuestion() {
        this.isAnswered = false;
        this.selectedAnswer = null;
        const q = this.questions[this.currentIndex];
        const progressPercent = ((this.currentIndex) / this.questions.length) * 100;
        
        this.container.innerHTML = `
            <div class="animate-slide-up space-y-6">
                <!-- Progress Header -->
                <div class="flex justify-between items-center text-sm font-mono text-slate-400">
                    <span>Frage ${this.currentIndex + 1} von ${this.questions.length}</span>
                    <span>Fortschritt: ${Math.round(progressPercent)}%</span>
                </div>
                
                <!-- Progress Bar -->
                <div class="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div class="bg-gradient-to-r from-cyan-500 to-violet-500 h-full transition-all duration-300" style="width: ${progressPercent}%"></div>
                </div>

                <!-- Question Title -->
                <div class="glass-card rounded-xl p-6 border-l-4 border-cyan-500">
                    <h3 class="text-xl font-bold text-white leading-relaxed">${q.question}</h3>
                </div>

                <!-- Options Grid -->
                <div class="grid grid-cols-1 gap-4" id="quiz-options-container">
                    ${q.options.map((opt, idx) => `
                        <button 
                            data-index="${idx}" 
                            class="quiz-option text-left w-full p-4 rounded-lg bg-slate-800/40 text-slate-300 font-medium hover:text-white border border-slate-700/50 transition duration-200"
                        >
                            <span class="inline-block w-8 h-8 mr-3 rounded-full bg-slate-800 text-center leading-8 text-sm text-cyan-400 font-mono">${String.fromCharCode(65 + idx)}</span>
                            ${opt}
                        </button>
                    `).join('')}
                </div>

                <!-- Explanation Area (hidden initially) -->
                <div id="quiz-explanation-box" class="hidden glass-card rounded-xl p-5 bg-slate-900/40 border-l-4 border-amber-500">
                    <h4 class="text-amber-400 font-mono text-sm font-bold mb-1">Erklärung:</h4>
                    <p class="text-slate-300 text-sm leading-relaxed">${q.explanation || 'Keine Erklärung verfügbar.'}</p>
                </div>

                <!-- Action Button -->
                <div class="flex justify-end pt-2">
                    <button 
                        id="quiz-next-btn" 
                        class="hidden px-6 py-2.5 rounded-lg font-bold text-sm bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white transition duration-200 shadow-lg"
                    >
                        ${this.currentIndex === this.questions.length - 1 ? 'Quiz abschließen' : 'Nächste Frage &rarr;'}
                    </button>
                </div>
            </div>
        `;

        // Add Event Listeners for options
        const optionButtons = this.container.querySelectorAll('.quiz-option');
        optionButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleAnswerSelect(btn));
        });

        // Add Event Listener for Next Button
        const nextBtn = this.container.querySelector('#quiz-next-btn');
        nextBtn.addEventListener('click', () => this.handleNextQuestion());
    }

    handleAnswerSelect(clickedButton) {
        if (this.isAnswered) return;
        this.isAnswered = true;
        
        const selectedIdx = parseInt(clickedButton.getAttribute('data-index'));
        const correctIdx = this.questions[this.currentIndex].answerIndex;
        const isMultiCorrect = Array.isArray(correctIdx);
        
        const optionButtons = this.container.querySelectorAll('.quiz-option');
        
        // Highlight choices
        optionButtons.forEach(btn => {
            btn.classList.add('locked');
            const idx = parseInt(btn.getAttribute('data-index'));
            const isCorrect = isMultiCorrect ? correctIdx.includes(idx) : idx === correctIdx;
            if (isCorrect) {
                btn.classList.add('correct');
            } else if (idx === selectedIdx) {
                btn.classList.add('incorrect');
            }
        });

        const selectedIsCorrect = isMultiCorrect ? correctIdx.includes(selectedIdx) : selectedIdx === correctIdx;
        if (selectedIsCorrect) {
            this.score++;
        }

        // Show explanation
        const explanationBox = this.container.querySelector('#quiz-explanation-box');
        explanationBox.classList.remove('hidden');

        // Show Next Button
        const nextBtn = this.container.querySelector('#quiz-next-btn');
        nextBtn.classList.remove('hidden');
    }

    handleNextQuestion() {
        if (this.currentIndex < this.questions.length - 1) {
            this.currentIndex++;
            this.renderQuestion();
        } else {
            this.renderResults();
        }
    }

    renderResults() {
        const percent = Math.round((this.score / this.questions.length) * 100);
        let badge = "🎓 Master-Simulant";
        let feedback = "Hervorragende Leistung! Du hast das Thema dieser Woche vollständig durchdrungen.";
        
        if (percent < 50) {
            badge = "🌱 Einsteiger";
            feedback = "Das war ein guter Versuch, aber du solltest die Übungen und die Einführung noch einmal durchgehen.";
        } else if (percent < 85) {
            badge = "🛡️ Simulations-Analyst";
            feedback = "Gute Arbeit! Die Kernkonzepte sind verstanden. Schau dir die falschen Fragen noch einmal an.";
        }

        this.container.innerHTML = `
            <div class="animate-slide-up text-center py-8 px-4 glass-card rounded-2xl border-t-4 border-cyan-500 max-w-xl mx-auto space-y-6">
                <div class="text-6xl">🏆</div>
                <h3 class="text-2xl md:text-3xl font-extrabold text-white">Quiz abgeschlossen!</h3>
                
                <div class="py-4">
                    <div class="text-sm font-mono text-slate-400 mb-1">Deine Punktzahl</div>
                    <div class="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-500">${this.score} / ${this.questions.length}</div>
                    <div class="text-lg font-mono text-cyan-400 mt-2 font-bold">${percent}% Richtig</div>
                </div>

                <div class="p-4 bg-slate-900/60 rounded-xl border border-slate-800 text-left space-y-2">
                    <div class="text-xs font-mono text-slate-500 uppercase tracking-wider">Erhaltenes Abzeichen:</div>
                    <div class="text-white font-bold text-lg flex items-center gap-2">
                        <span>${badge}</span>
                    </div>
                    <p class="text-sm text-slate-400 leading-relaxed">${feedback}</p>
                </div>

                <div class="flex flex-col sm:flex-row justify-center gap-4 pt-4">
                    <button 
                        id="quiz-restart-btn" 
                        class="px-5 py-2.5 rounded-lg border border-slate-700 hover:border-slate-500 text-sm font-medium text-slate-300 hover:text-white transition duration-200"
                    >
                        Wiederholen
                    </button>
                    <a 
                        href="index.html" 
                        class="px-5 py-2.5 rounded-lg font-bold text-sm bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-400 hover:to-purple-500 text-white transition duration-200 text-center shadow-lg"
                    >
                        Zurück zum Dashboard
                    </a>
                </div>
            </div>
        `;

        // Add event listener to restart button
        const restartBtn = this.container.querySelector('#quiz-restart-btn');
        restartBtn.addEventListener('click', () => {
            this.currentIndex = 0;
            this.score = 0;
            this.init();
        });

        // Trigger complete callback to notify shell
        if (this.onComplete) {
            this.onComplete(this.score, this.questions.length);
        }
    }
}
