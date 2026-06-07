import { courseInfo, modules, weeksData } from './data.js';
import { QuizEngine } from './quiz.js';

document.addEventListener('DOMContentLoaded', () => {
    // Detect current page
    const path = window.location.pathname;
    const page = path.substring(path.lastIndexOf('/') + 1);
    
    if (page === '' || page === 'index.html') {
        initPortalPage();
    } else if (page === 'week.html') {
        initWeekPage();
    }
    
    // Setup global lightbox
    setupImageLightbox(document);
});

/* ==========================================
   1. PORTAL PAGE LOGIC (index.html)
   ========================================== */
function initPortalPage() {
    // Populate course titles
    document.getElementById('course-title').innerText = courseInfo.title;
    document.getElementById('course-subtitle').innerText = courseInfo.subtitle;
    document.getElementById('course-semester').innerText = courseInfo.semester;
    document.getElementById('course-department').innerText = courseInfo.department;
    document.getElementById('course-institution').innerText = courseInfo.institution;
    
    // Populate grading breakdown
    const gradingContainer = document.getElementById('grading-container');
    if (gradingContainer) {
        gradingContainer.innerHTML = courseInfo.grading.map(item => `
            <div class="flex justify-between items-center py-2.5 border-b border-slate-800 text-sm">
                <span class="text-slate-400 font-medium">${item.label}</span>
                <span class="text-cyan-400 font-mono font-bold">${item.value}</span>
            </div>
        `).join('');
    }

    // Toggle grading drawer visibility
    const openDrawerBtn = document.getElementById('toggle-grades-drawer-btn');
    const closeDrawerBtn = document.getElementById('close-drawer-btn');
    const drawer = document.getElementById('grades-drawer');
    const backdrop = document.getElementById('drawer-backdrop');

    if (openDrawerBtn && closeDrawerBtn && drawer && backdrop) {
        const toggleDrawer = () => {
            const isOpen = drawer.classList.contains('translate-x-0');
            if (isOpen) {
                drawer.classList.remove('translate-x-0');
                drawer.classList.add('translate-x-full');
                backdrop.classList.add('opacity-0');
                setTimeout(() => backdrop.classList.add('hidden'), 300);
            } else {
                backdrop.classList.remove('hidden');
                setTimeout(() => backdrop.classList.remove('opacity-0'), 10);
                drawer.classList.remove('translate-x-full');
                drawer.classList.add('translate-x-0');
            }
        };

        openDrawerBtn.addEventListener('click', toggleDrawer);
        closeDrawerBtn.addEventListener('click', toggleDrawer);
        backdrop.addEventListener('click', toggleDrawer);
    }

    // Calculate completion progress
    const activeWeeks = Object.values(weeksData).filter(w => w.active && w.id !== '14'); // Exclude presentation week for quiz calculation
    
    let totalPointsEarned = 0;
    const maxPointsPossible = activeWeeks.length * 5; // 1 pt for quiz, 4 pts for problem set
    
    const pointsListHtml = activeWeeks.map(w => {
        const quizDone = localStorage.getItem(`quiz_completed_week_${w.id}`) === 'true';
        const psDone = localStorage.getItem(`problemset_completed_week_${w.id}`) === 'true';
        
        const quizPts = quizDone ? 1 : 0;
        const psPts = psDone ? 4 : 0;
        const weekPts = quizPts + psPts;
        totalPointsEarned += weekPts;
        
        return `
            <div class="p-3 rounded-xl bg-slate-900/40 border border-slate-800 space-y-2">
                <div class="flex justify-between items-center text-xs font-mono font-bold text-white">
                    <span>Woche ${w.id}: ${w.title.substring(0, 30)}${w.title.length > 30 ? '...' : ''}</span>
                    <span class="text-cyan-400 font-mono font-bold">${weekPts} / 5 Pkt</span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="flex items-center gap-1.5 p-1.5 rounded bg-slate-950/35 border ${quizDone ? 'border-emerald-500/20 text-emerald-400' : 'border-slate-800 text-slate-500'}">
                        <span>${quizDone ? '✓' : '○'}</span>
                        <span class="font-medium">Quiz (1 Pkt)</span>
                    </div>
                    <label class="flex items-center gap-1.5 p-1.5 rounded bg-slate-950/35 border cursor-pointer select-none transition-all ${psDone ? 'border-emerald-500/20 text-emerald-400 hover:border-emerald-500/35' : 'border-slate-800 text-slate-500 hover:border-slate-700'}" for="checkbox-ps-${w.id}">
                        <input 
                            type="checkbox" 
                            id="checkbox-ps-${w.id}" 
                            class="hidden problemset-checkbox" 
                            data-week="${w.id}"
                            ${psDone ? 'checked' : ''}
                        />
                        <span>${psDone ? '✓' : '○'}</span>
                        <span class="font-medium">ProbSet (4 Pkt)</span>
                    </label>
                </div>
            </div>
        `;
    }).join('');

    const pointsListContainer = document.getElementById('points-list-container');
    const totalPointsLabel = document.getElementById('portal-total-points');
    
    if (pointsListContainer) {
        pointsListContainer.innerHTML = pointsListHtml;
        
        // Add change event listeners to checkboxes to toggle completion
        pointsListContainer.querySelectorAll('.problemset-checkbox').forEach(chk => {
            chk.addEventListener('change', (e) => {
                const weekId = e.target.getAttribute('data-week');
                const isChecked = e.target.checked;
                localStorage.setItem(`problemset_completed_week_${weekId}`, isChecked ? 'true' : 'false');
                
                // Rerender portal to update grades and calculations
                initPortalPage();
            });
        });
    }
    
    if (totalPointsLabel) {
        totalPointsLabel.innerText = `${totalPointsEarned} / ${maxPointsPossible} Pkt`;
    }
    
    const progressPercent = maxPointsPossible > 0 ? Math.round((totalPointsEarned / maxPointsPossible) * 100) : 0;
    
    const progressFill = document.getElementById('portal-progress-fill');
    const progressText = document.getElementById('portal-progress-text');
    if (progressFill && progressText) {
        progressFill.style.width = `${progressPercent}%`;
        progressText.innerText = `${progressPercent}% abgeschlossen (${totalPointsEarned}/${maxPointsPossible} Punkte)`;
    }

    // Render Weekly Modules Cards
    const roadmapContainer = document.getElementById('roadmap-grid');
    if (roadmapContainer) {
        roadmapContainer.innerHTML = Object.values(weeksData).map(w => {
            const isCompleted = localStorage.getItem(`quiz_completed_week_${w.id}`) === 'true';
            const moduleName = modules[w.module] || 'Fortgeschrittene Methoden';
            
            if (w.active) {
                return `
                    <div class="glass-card rounded-2xl p-6 glow-cyan flex flex-col justify-between border-t-2 border-t-cyan-500/35 relative overflow-hidden group">
                        ${isCompleted ? `
                            <div class="absolute top-3 right-3 bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-0.5 rounded-full font-mono font-bold flex items-center gap-1 border border-emerald-500/30">
                                <span>✓</span> abgeschlossen
                            </div>
                        ` : ''}
                        <div>
                            <div class="text-xs font-mono text-cyan-400 uppercase tracking-wider mb-2">${moduleName}</div>
                            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-cyan-400 transition-colors">Woche ${w.id}: ${w.title}</h3>
                            <p class="text-sm text-slate-400 leading-relaxed mb-6">${w.description}</p>
                        </div>
                        <a 
                            href="week.html?id=${w.id}" 
                            class="inline-flex items-center gap-2 text-sm font-bold text-cyan-400 hover:text-cyan-300 group-hover:translate-x-1 transition-transform"
                        >
                            Materialien öffnen &rarr;
                        </a>
                    </div>
                `;
            } else {
                return `
                    <div class="glass-card rounded-2xl p-6 border-t-2 border-t-slate-800 week-locked flex flex-col justify-between">
                        <div>
                            <div class="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2">${moduleName}</div>
                            <h3 class="text-xl font-bold text-slate-500 mb-2 flex items-center gap-2">
                                Woche ${w.id}: ${w.title}
                                <span class="text-base text-slate-600">🔒</span>
                            </h3>
                            <p class="text-sm text-slate-500 leading-relaxed mb-6">${w.description}</p>
                        </div>
                        <span class="text-xs font-mono text-amber-500/75 uppercase tracking-widest font-bold">Demnächst verfügbar</span>
                    </div>
                `;
            }
        }).join('');
    }
}

/* ==========================================
   2. WEEKLY DASHBOARD LOGIC (week.html)
   ========================================== */
let currentWeekId = "1";
let activeTab = "intro"; // 'intro', 'infographic', 'problemset', 'quiz'

function initWeekPage() {
    // Get week ID from URL parameter
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    
    // Validate week ID
    if (id && weeksData[id] && weeksData[id].active) {
        currentWeekId = id;
    } else {
        // Find first active week
        const firstActive = Object.values(weeksData).find(w => w.active);
        currentWeekId = firstActive ? firstActive.id : "1";
    }

    // Populate shell details
    const week = weeksData[currentWeekId];
    const moduleName = modules[week.module] || 'Fortgeschrittene Methoden';
    
    document.getElementById('header-week-title').innerText = `Woche ${week.id}: ${week.title}`;
    document.getElementById('header-module-title').innerText = moduleName;
    document.title = `Woche ${week.id}: ${week.title} - Advanced Modeling & System Simulation`;

    // Render sidebar navigation
    renderSidebar();
    
    // Set up tab events
    setupTabs();
    
    // Load default tab content
    loadTabContent('intro');

    // Sidebar Mobile Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar-nav-container');
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('-translate-x-full');
        });
    }
}

function renderSidebar() {
    const listContainer = document.getElementById('sidebar-weeks-list');
    if (!listContainer) return;
    
    listContainer.innerHTML = Object.values(weeksData).map(w => {
        const isActive = w.id === currentWeekId;
        const quizDone = localStorage.getItem(`quiz_completed_week_${w.id}`) === 'true';
        const psDone = localStorage.getItem(`problemset_completed_week_${w.id}`) === 'true';
        const isFullyCompleted = quizDone && psDone;
        const isPartiallyCompleted = quizDone || psDone;
        
        if (w.active) {
            let statusIndicator = `<span class="w-1.5 h-1.5 rounded-full bg-cyan-400" title="Aktiv"></span>`;
            if (isFullyCompleted) {
                statusIndicator = `<span class="text-emerald-400 font-bold text-sm leading-none" title="Vollständig abgeschlossen (5/5 Pkt)">✓</span>`;
            } else if (isPartiallyCompleted) {
                statusIndicator = `<span class="text-amber-400 font-bold text-xs leading-none" title="Teilweise abgeschlossen (1/5 oder 4/5 Pkt)">◐</span>`;
            }
            
            return `
                <li>
                    <a 
                        href="week.html?id=${w.id}" 
                        class="flex items-center justify-between px-4 py-3 rounded-lg text-sm transition-all ${
                            isActive 
                            ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 border-l-4 border-cyan-500 text-cyan-400 font-bold' 
                            : 'text-slate-300 hover:bg-slate-800/50 hover:text-white'
                        }"
                    >
                        <span class="truncate pr-2">W${w.id}: ${w.title}</span>
                        ${statusIndicator}
                    </a>
                </li>
            `;
        } else {
            return `
                <li>
                    <div 
                        class="flex items-center justify-between px-4 py-3 rounded-lg text-sm text-slate-600 cursor-not-allowed select-none"
                        title="Demnächst verfügbar"
                    >
                        <span class="truncate pr-2">W${w.id}: ${w.title}</span>
                        <span class="text-xs">🔒</span>
                    </div>
                </li>
            `;
        }
    }).join('');
}

function setupTabs() {
    const tabButtons = {
        intro: document.getElementById('tab-btn-intro'),
        infographic: document.getElementById('tab-btn-infographic'),
        problemset: document.getElementById('tab-btn-problemset'),
        quiz: document.getElementById('tab-btn-quiz')
    };

    Object.keys(tabButtons).forEach(tab => {
        const btn = tabButtons[tab];
        if (btn) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                loadTabContent(tab);
            });
        }
    });
}

function updateActiveTabUI(selectedTab) {
    activeTab = selectedTab;
    const tabs = ['intro', 'infographic', 'problemset', 'quiz'];
    
    tabs.forEach(tab => {
        const btn = document.getElementById(`tab-btn-${tab}`);
        if (btn) {
            if (tab === selectedTab) {
                btn.classList.add('tab-active');
                btn.classList.remove('text-slate-400');
            } else {
                btn.classList.remove('tab-active');
                btn.classList.add('text-slate-400');
            }
        }
    });
}

function loadTabContent(tab) {
    updateActiveTabUI(tab);
    const contentArea = document.getElementById('tab-viewport-content');
    if (!contentArea) return;

    // Show loading state
    contentArea.innerHTML = `
        <div class="flex flex-col items-center justify-center py-20 space-y-4">
            <div class="w-10 h-10 border-4 border-cyan-500/20 border-t-cyan-500 rounded-full animate-spin"></div>
            <p class="text-slate-500 font-mono text-sm">Lade Daten...</p>
        </div>
    `;

    const weekPath = `weeks/week${currentWeekId}`;

    if (tab === 'intro') {
        fetch(`${weekPath}/introduction.html?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) throw new Error("Einführung nicht gefunden");
                return res.text();
            })
            .then(html => {
                contentArea.innerHTML = `<div class="animate-slide-up space-y-6">${html}</div>`;
                highlightCodeSnippets(contentArea);
                setupImageLightbox(contentArea);
                renderMath(contentArea);
            })
            .catch(err => {
                contentArea.innerHTML = renderErrorState("Einführung konnte nicht geladen werden.", err.message);
            });
            
    } else if (tab === 'infographic') {
        // Infographic is loaded in iframe to sand-box scripts (Tailwind configuration & Chart.js instances)
        contentArea.innerHTML = `
            <div class="animate-slide-up space-y-4">
                <div class="flex justify-between items-center text-xs text-slate-400 font-mono mb-2">
                    <span>💡 Tipp: Interagierte mit den Diagrammen für Detailinfos</span>
                    <button id="iframe-reload-btn" class="hover:text-cyan-400 transition-colors">🔄 Neu laden</button>
                </div>
                <div class="iframe-container shadow-2xl border border-slate-800">
                    <iframe 
                        id="infographic-iframe" 
                        src="${weekPath}/infographic.html?v=${Date.now()}"
                        allow="fullscreen"
                    ></iframe>
                </div>
            </div>
        `;
        
        const reloadBtn = document.getElementById('iframe-reload-btn');
        if (reloadBtn) {
            reloadBtn.addEventListener('click', () => {
                const iframe = document.getElementById('infographic-iframe');
                if (iframe) iframe.src = `${weekPath}/infographic.html?v=${Date.now()}`;
            });
        }
        
    } else if (tab === 'problemset') {
        fetch(`${weekPath}/problemset.html?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) throw new Error("Problem Set nicht gefunden");
                return res.text();
            })
            .then(html => {
                const psDone = localStorage.getItem(`problemset_completed_week_${currentWeekId}`) === 'true';
                
                const statusCardHtml = `
                    <div id="problemset-status-card" class="glass-card rounded-2xl p-6 border flex flex-col sm:flex-row justify-between items-center gap-4 mb-6 transition-all duration-300 ${
                        psDone 
                        ? 'border-emerald-500/35 bg-emerald-500/5 shadow-emerald-500/5' 
                        : 'border-cyan-500/25 bg-cyan-950/5'
                    }">
                        <div class="flex items-center gap-3">
                            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-xl font-bold transition-all duration-300 ${
                                psDone ? 'bg-emerald-500/20 text-emerald-400' : 'bg-cyan-500/10 text-cyan-400'
                            }" id="problemset-status-icon">
                                ${psDone ? '✓' : '📝'}
                            </div>
                            <div>
                                <h4 class="text-white font-bold text-base">Problem Set Abgabestatus</h4>
                                <p class="text-xs text-slate-400 font-mono" id="problemset-status-text">
                                    ${psDone ? 'Status: Erfolgreich abgeschlossen (+4 Punkte)' : 'Status: Noch nicht abgeschlossen (Wert: 4 Punkte)'}
                                </p>
                            </div>
                        </div>
                        <button 
                            id="problemset-toggle-complete-btn" 
                            class="px-5 py-2.5 rounded-xl font-bold font-mono text-xs shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 border focus:outline-none ${
                                psDone 
                                ? 'bg-emerald-600 hover:bg-emerald-500 border-emerald-500/40 text-white shadow-emerald-600/10' 
                                : 'bg-slate-900 hover:bg-cyan-500/5 border-slate-800 hover:border-cyan-500/50 text-cyan-400 shadow-cyan-500/5'
                            }"
                        >
                            ${psDone ? 'Als unvollständig markieren' : 'Als abgeschlossen markieren'}
                        </button>
                    </div>
                `;
                
                contentArea.innerHTML = `<div class="animate-slide-up space-y-6">${statusCardHtml}${html}</div>`;
                
                // Add event listener to toggle button
                const toggleBtn = document.getElementById('problemset-toggle-complete-btn');
                const statusCard = document.getElementById('problemset-status-card');
                const statusIcon = document.getElementById('problemset-status-icon');
                const statusText = document.getElementById('problemset-status-text');
                
                if (toggleBtn && statusCard && statusIcon && statusText) {
                    toggleBtn.addEventListener('click', () => {
                        const currentStatus = localStorage.getItem(`problemset_completed_week_${currentWeekId}`) === 'true';
                        const newStatus = !currentStatus;
                        localStorage.setItem(`problemset_completed_week_${currentWeekId}`, newStatus ? 'true' : 'false');
                        
                        // Update UI classes and text
                        if (newStatus) {
                            statusCard.className = "glass-card rounded-2xl p-6 border flex flex-col sm:flex-row justify-between items-center gap-4 mb-6 transition-all duration-300 border-emerald-500/35 bg-emerald-500/5 shadow-emerald-500/5";
                            statusIcon.className = "w-12 h-12 rounded-xl flex items-center justify-center text-xl font-bold transition-all duration-300 bg-emerald-500/20 text-emerald-400";
                            statusIcon.innerHTML = "✓";
                            statusText.innerHTML = "Status: Erfolgreich abgeschlossen (+4 Punkte)";
                            toggleBtn.className = "px-5 py-2.5 rounded-xl font-bold font-mono text-xs shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 border focus:outline-none bg-emerald-600 hover:bg-emerald-500 border-emerald-500/40 text-white shadow-emerald-600/10";
                            toggleBtn.innerText = "Als unvollständig markieren";
                        } else {
                            statusCard.className = "glass-card rounded-2xl p-6 border flex flex-col sm:flex-row justify-between items-center gap-4 mb-6 transition-all duration-300 border-cyan-500/25 bg-cyan-950/5";
                            statusIcon.className = "w-12 h-12 rounded-xl flex items-center justify-center text-xl font-bold transition-all duration-300 bg-cyan-500/10 text-cyan-400";
                            statusIcon.innerHTML = "📝";
                            statusText.innerHTML = "Status: Noch nicht abgeschlossen (Wert: 4 Punkte)";
                            toggleBtn.className = "px-5 py-2.5 rounded-xl font-bold font-mono text-xs shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 border focus:outline-none bg-slate-900 hover:bg-cyan-500/5 border-slate-800 hover:border-cyan-500/50 text-cyan-400 shadow-cyan-500/5";
                            toggleBtn.innerText = "Als abgeschlossen markieren";
                        }
                        
                        // Update sidebar navigation checks
                        renderSidebar();
                    });
                }

                highlightCodeSnippets(contentArea);
                addCopyButtonsToCode(contentArea);
                setupImageLightbox(contentArea);
                renderMath(contentArea);
            })
            .catch(err => {
                contentArea.innerHTML = renderErrorState("Problem Set (in English) konnte nicht geladen werden.", err.message);
            });
            
    } else if (tab === 'quiz') {
        fetch(`${weekPath}/quiz.json?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) throw new Error("Quiz-Datenbank nicht gefunden");
                return res.json();
            })
            .then(jsonData => {
                new QuizEngine(contentArea, jsonData, (score, total) => {
                    // Mark quiz as completed in localStorage
                    localStorage.setItem(`quiz_completed_week_${currentWeekId}`, 'true');
                    // Rerender sidebar to show completion tick
                    renderSidebar();
                });
            })
            .catch(err => {
                contentArea.innerHTML = renderErrorState("Quiz konnte nicht initialisiert werden.", err.message);
            });
    }
}

function renderErrorState(title, message) {
    return `
        <div class="text-center py-16 px-4 glass-card rounded-2xl border-t-4 border-rose-500 max-w-lg mx-auto space-y-4">
            <div class="text-4xl text-rose-500">⚠</div>
            <h3 class="text-xl font-bold text-white">${title}</h3>
            <p class="text-sm text-slate-400 font-mono">${message}</p>
            <p class="text-xs text-slate-500 leading-relaxed">Bitte stelle sicher, dass die Dateistruktur lokal übereinstimmt und der Server über <code>uv run server.py</code> läuft.</p>
        </div>
    `;
}

function highlightCodeSnippets(container) {
    // Look for standard <pre><code> structures.
    // If user has hljs (Highlight.js) loaded globally, we call it.
    if (window.hljs) {
        container.querySelectorAll('pre code').forEach((block) => {
            window.hljs.highlightElement(block);
        });
    }
}

function addCopyButtonsToCode(container) {
    const blocks = container.querySelectorAll('pre');
    blocks.forEach(block => {
        // Ensure relative positioning
        block.classList.add('relative', 'group');
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'absolute top-3 right-3 px-3 py-1 rounded bg-slate-800 text-xs text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity duration-200 border border-slate-700 hover:text-white hover:bg-slate-750';
        copyBtn.innerText = 'Copy';
        
        copyBtn.addEventListener('click', () => {
            const code = block.querySelector('code').innerText;
            navigator.clipboard.writeText(code).then(() => {
                copyBtn.innerText = 'Copied!';
                copyBtn.classList.add('text-emerald-400', 'border-emerald-600');
                setTimeout(() => {
                    copyBtn.innerText = 'Copy';
                    copyBtn.classList.remove('text-emerald-400', 'border-emerald-600');
                }, 2000);
            });
        });
        block.appendChild(copyBtn);
    });
}

function renderMath(container) {
    if (window.renderMathInElement) {
        window.renderMathInElement(container, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\(', right: '\\)', display: false},
                {left: '\\[', right: '\\]', display: true}
            ],
            throwOnError: false
        });
    } else {
        setTimeout(() => renderMath(container), 100);
    }
}

function setupImageLightbox(container) {
    let lightbox = document.getElementById('global-lightbox');
    if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.id = 'global-lightbox';
        lightbox.className = 'fixed inset-0 z-[100] hidden bg-slate-950/90 backdrop-blur-md flex flex-col items-center justify-center p-4 cursor-zoom-out opacity-0 transition-opacity duration-300';
        lightbox.innerHTML = `
            <div class="relative max-w-5xl max-h-[90vh] flex flex-col items-center transform scale-95 transition-transform duration-300 ease-out" id="lightbox-content">
                <button class="absolute -top-12 right-0 text-slate-400 hover:text-white transition-colors text-xs font-mono flex items-center gap-1.5 bg-slate-900/60 px-3 py-1.5 rounded-lg border border-white/10 select-none">
                    ✕ CLOSE
                </button>
                <img class="max-w-full max-h-[80vh] object-contain rounded-2xl border border-white/10 shadow-2xl" id="lightbox-img" src="" alt="Enlarged view">
                <p class="text-xs font-mono text-cyan-400 mt-4 bg-slate-900/65 px-4 py-2 rounded-lg border border-white/10 select-none" id="lightbox-caption"></p>
            </div>
        `;
        document.body.appendChild(lightbox);

        lightbox.addEventListener('click', () => {
            closeLightbox();
        });
        
        const img = lightbox.querySelector('#lightbox-img');
        img.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    function openLightbox(src, alt) {
        const img = lightbox.querySelector('#lightbox-img');
        const caption = lightbox.querySelector('#lightbox-caption');
        const content = lightbox.querySelector('#lightbox-content');
        
        img.src = src;
        caption.innerText = alt || 'Abbildung';
        
        lightbox.classList.remove('hidden');
        void lightbox.offsetWidth; // Force reflow
        
        lightbox.classList.remove('opacity-0');
        content.classList.remove('scale-95');
        content.classList.add('scale-100');
        document.body.classList.add('overflow-hidden');
    }

    function closeLightbox() {
        const content = lightbox.querySelector('#lightbox-content');
        lightbox.classList.add('opacity-0');
        content.classList.remove('scale-100');
        content.classList.add('scale-95');
        
        setTimeout(() => {
            lightbox.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }, 300);
    }

    const images = container.querySelectorAll('img');
    images.forEach(img => {
        if (img.classList.contains('w-6') || img.classList.contains('h-6') || img.id === 'lightbox-img') return;
        
        img.classList.add('cursor-zoom-in', 'hover:brightness-95', 'transition-all', 'duration-200');
        img.addEventListener('click', () => {
            openLightbox(img.src, img.alt);
        });
    });
}
