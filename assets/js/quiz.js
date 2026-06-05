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
        this.selectedAnswers = [];
        const q = this.questions[this.currentIndex];
        const progressPercent = ((this.currentIndex) / this.questions.length) * 100;
        const isMultiCorrect = Array.isArray(q.answerIndex);
        
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
                <div class="glass-card rounded-xl p-6 border-l-4 ${isMultiCorrect ? 'border-purple-500 bg-purple-950/5' : 'border-cyan-500 bg-cyan-950/5'}">
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded ${isMultiCorrect ? 'bg-purple-500/20 text-purple-400 border border-purple-500/30' : 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'} mb-3 inline-block font-bold uppercase tracking-wider">
                        ${isMultiCorrect ? 'Mehrfachauswahl (Wähle alle richtigen Antworten)' : 'Einfachauswahl (Wähle eine richtige Antwort)'}
                    </span>
                    <h3 class="text-xl font-bold text-white leading-relaxed">${q.question}</h3>
                </div>

                <!-- Options Grid -->
                <div class="grid grid-cols-1 gap-4" id="quiz-options-container">
                    ${q.options.map((opt, idx) => `
                        <button 
                            data-index="${idx}" 
                            class="quiz-option text-left w-full p-4 rounded-lg bg-slate-800/40 text-slate-300 font-medium hover:text-white border border-slate-700/50 transition duration-200 flex items-center justify-between"
                        >
                            <span class="flex items-center">
                                <span class="inline-block w-8 h-8 mr-3 rounded-full bg-slate-800 text-center leading-8 text-sm text-cyan-400 font-mono option-prefix">${String.fromCharCode(65 + idx)}</span>
                                <span class="option-text">${opt}</span>
                            </span>
                            <span class="checkbox-box w-5 h-5 rounded border ${isMultiCorrect ? 'border-purple-800/60' : 'border-cyan-800/60'} flex items-center justify-center text-[10px] text-white opacity-0 transition-opacity">✓</span>
                        </button>
                    `).join('')}
                </div>

                <!-- Explanation Area (hidden initially) -->
                <div id="quiz-explanation-box" class="hidden glass-card rounded-xl p-5 bg-slate-900/40 border-l-4 border-amber-500">
                    <h4 class="text-amber-400 font-mono text-sm font-bold mb-1">Erklärung:</h4>
                    <p class="text-slate-300 text-sm leading-relaxed">${q.explanation || 'Keine Erklärung verfügbar.'}</p>
                </div>

                <!-- Action Buttons -->
                <div class="flex justify-end gap-4 pt-2">
                    <button 
                        id="quiz-submit-btn" 
                        class="px-6 py-2.5 rounded-lg font-bold text-sm bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white transition duration-200 shadow-lg disabled:opacity-40 disabled:cursor-not-allowed focus:outline-none"
                        disabled
                    >
                        Antwort abgeben
                    </button>
                    <button 
                        id="quiz-next-btn" 
                        class="hidden px-6 py-2.5 rounded-lg font-bold text-sm bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white transition duration-200 shadow-lg focus:outline-none"
                    >
                        ${this.currentIndex === this.questions.length - 1 ? 'Quiz abschließen &rarr;' : 'Nächste Frage &rarr;'}
                    </button>
                </div>
            </div>
        `;

        // Add Event Listeners for options
        const optionButtons = this.container.querySelectorAll('.quiz-option');
        optionButtons.forEach(btn => {
            btn.addEventListener('click', () => this.handleAnswerSelect(btn));
        });

        // Add Event Listener for Submit Button
        const submitBtn = this.container.querySelector('#quiz-submit-btn');
        submitBtn.addEventListener('click', () => this.handleSubmitAnswer());

        // Add Event Listener for Next Button
        const nextBtn = this.container.querySelector('#quiz-next-btn');
        nextBtn.addEventListener('click', () => this.handleNextQuestion());
    }

    handleAnswerSelect(clickedButton) {
        if (this.isAnswered) return;
        
        const selectedIdx = parseInt(clickedButton.getAttribute('data-index'));
        const q = this.questions[this.currentIndex];
        const isMultiCorrect = Array.isArray(q.answerIndex);
        
        if (isMultiCorrect) {
            // Toggle selection
            const idxInSelected = this.selectedAnswers.indexOf(selectedIdx);
            if (idxInSelected > -1) {
                this.selectedAnswers.splice(idxInSelected, 1);
                clickedButton.classList.remove('selected');
                clickedButton.querySelector('.checkbox-box').classList.add('opacity-0');
            } else {
                this.selectedAnswers.push(selectedIdx);
                clickedButton.classList.add('selected');
                clickedButton.querySelector('.checkbox-box').classList.remove('opacity-0');
            }
        } else {
            // Single select: deselect others
            this.selectedAnswers = [selectedIdx];
            const optionButtons = this.container.querySelectorAll('.quiz-option');
            optionButtons.forEach(btn => {
                const idx = parseInt(btn.getAttribute('data-index'));
                const check = btn.querySelector('.checkbox-box');
                if (idx === selectedIdx) {
                    btn.classList.add('selected');
                    if (check) check.classList.remove('opacity-0');
                } else {
                    btn.classList.remove('selected');
                    if (check) check.classList.add('opacity-0');
                }
            });
        }
        
        // Enable submit button if at least one selected
        const submitBtn = this.container.querySelector('#quiz-submit-btn');
        if (submitBtn) {
            submitBtn.disabled = this.selectedAnswers.length === 0;
        }
    }

    handleSubmitAnswer() {
        if (this.isAnswered) return;
        this.isAnswered = true;
        
        const q = this.questions[this.currentIndex];
        const correctIdx = q.answerIndex;
        const isMultiCorrect = Array.isArray(correctIdx);
        
        const optionButtons = this.container.querySelectorAll('.quiz-option');
        
        // Lock all options and highlight correct/incorrect
        optionButtons.forEach(btn => {
            btn.classList.add('locked');
            btn.classList.remove('selected'); // remove selected styling
            const idx = parseInt(btn.getAttribute('data-index'));
            const check = btn.querySelector('.checkbox-box');
            if (check) check.classList.add('opacity-0');
            
            const isCorrect = isMultiCorrect ? correctIdx.includes(idx) : idx === correctIdx;
            const isSelected = this.selectedAnswers.includes(idx);
            
            if (isCorrect) {
                btn.classList.add('correct');
            } else if (isSelected) {
                btn.classList.add('incorrect');
            }
        });
        
        // Grade the answer
        let isUserCorrect = false;
        if (isMultiCorrect) {
            // User must have selected exactly the correct set
            const sortedSelected = [...this.selectedAnswers].sort((a, b) => a - b);
            const sortedCorrect = [...correctIdx].sort((a, b) => a - b);
            isUserCorrect = sortedSelected.length === sortedCorrect.length && 
                           sortedSelected.every((val, index) => val === sortedCorrect[index]);
        } else {
            isUserCorrect = this.selectedAnswers[0] === correctIdx;
        }
        
        if (isUserCorrect) {
            this.score++;
        }
        
        // Hide submit button, show next button
        const submitBtn = this.container.querySelector('#quiz-submit-btn');
        if (submitBtn) submitBtn.classList.add('hidden');
        
        const nextBtn = this.container.querySelector('#quiz-next-btn');
        if (nextBtn) nextBtn.classList.remove('hidden');
        
        // Show explanation
        const explanationBox = this.container.querySelector('#quiz-explanation-box');
        if (explanationBox) explanationBox.classList.remove('hidden');
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
