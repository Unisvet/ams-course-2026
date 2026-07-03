import { courseInfo, modules, weeksData, ui, currentLang, translations } from './data.js';
import { QuizEngine } from './quiz.js';

document.addEventListener('DOMContentLoaded', () => {
    // Detect current page
    const path = window.location.pathname;
    const page = path.substring(path.lastIndexOf('/') + 1);
    
    // Setup language switcher first
    setupLanguageSwitcher();
    
    if (page === '' || page === 'index.html') {
        initPortalPage();
        setupPortalEventListeners();
    } else if (page === 'week.html') {
        initWeekPage();
    }
    
    // Setup global lightbox
    setupImageLightbox(document);
});

function setupLanguageSwitcher() {
    const btnDe = document.getElementById('lang-de');
    const btnEn = document.getElementById('lang-en');
    
    if (!btnDe || !btnEn) return;
    
    const updateButtons = (lang) => {
        if (lang === 'de') {
            btnDe.classList.add('bg-cyan-500', 'text-white');
            btnDe.classList.remove('text-slate-500');
            btnEn.classList.add('text-slate-500');
            btnEn.classList.remove('bg-cyan-500', 'text-white');
        } else {
            btnEn.classList.add('bg-cyan-500', 'text-white');
            btnEn.classList.remove('text-slate-500');
            btnDe.classList.add('text-slate-500');
            btnDe.classList.remove('bg-cyan-500', 'text-white');
        }
    };
    
    updateButtons(currentLang);
    
    btnDe.addEventListener('click', () => {
        if (currentLang !== 'de') {
            localStorage.setItem('ams_lang', 'de');
            window.location.reload();
        }
    });
    
    btnEn.addEventListener('click', () => {
        if (currentLang !== 'en') {
            localStorage.setItem('ams_lang', 'en');
            window.location.reload();
        }
    });
}

/* ==========================================
   1. PORTAL PAGE LOGIC (index.html)
   ========================================== */
function initPortalPage() {
    try {
        // Localize static UI elements - more robustly
        const allH2s = document.querySelectorAll('main h2');
        
        // Goals Section
        const goalsTitle = Array.from(allH2s).find(h => h.innerText.includes('Lernziele') || h.innerText.includes('Learning Objectives'));
        if (goalsTitle) {
            goalsTitle.innerHTML = `<span>🎓</span> ${ui.goalsTitle}`;
            const parent = goalsTitle.parentElement;
            if (parent) {
                const paragraphs = parent.querySelectorAll('p');
                if (paragraphs.length >= 1) paragraphs[0].innerHTML = formatMarkdown(ui.goalsContent1);
                if (paragraphs.length >= 2) paragraphs[1].innerHTML = formatMarkdown(ui.goalsContent2);
            }
        }
        
        // Core Contents Section
        const coreTitle = Array.from(allH2s).find(h => h.innerText.includes('Kerninhalte') || h.innerText.includes('Core Curriculum'));
        if (coreTitle) {
            coreTitle.innerHTML = `<span>🔬</span> ${ui.coreContents}`;
            const parent = coreTitle.parentElement;
            if (parent) {
                const grid = parent.querySelector('.grid');
                if (grid) {
                    const cards = grid.children;
                    if (cards.length >= 4) {
                        cards[0].querySelector('h4').innerText = `⚙️ ${ui.theory}`;
                        cards[0].querySelector('p').innerText = ui.theoryDesc;
                        cards[1].querySelector('h4').innerText = `🤖 ${ui.predictive}`;
                        cards[1].querySelector('p').innerText = ui.predictiveDesc;
                        cards[2].querySelector('h4').innerText = `⚡ ${ui.hpc}`;
                        cards[2].querySelector('p').innerText = ui.hpcDesc;
                        cards[3].querySelector('h4').innerText = `🧠 ${ui.agentic}`;
                        cards[3].querySelector('p').innerText = ui.agenticDesc;
                    }
                }
            }
        }
        
        // Roadmap Title
        const roadmapTitleElement = document.querySelector('section h2') || Array.from(allH2s).find(h => h.innerText.includes('Roadmap'));
        if (roadmapTitleElement) {
            roadmapTitleElement.innerText = ui.roadmapTitle;
            const desc = roadmapTitleElement.nextElementSibling;
            if (desc && desc.tagName === 'P') {
                desc.innerText = ui.roadmapDesc;
            }
        }
    } catch (e) {
        console.error("Error localizing static elements:", e);
    }
    
    const gradesBtnText = document.getElementById('grades-btn-text');
    if (gradesBtnText) gradesBtnText.innerText = `📊 ${ui.gradesBtn}`;
    
    const footerP1 = document.querySelector('footer p:nth-of-type(1)');
    const footerP2 = document.querySelector('footer p:nth-of-type(2)');
    if (footerP1) footerP1.innerText = `© 2026 ${courseInfo.title} | ${courseInfo.institution}`;
    if (footerP2) footerP2.innerText = ui.footerText;
    
    const drawerHeader = document.querySelector('#grades-drawer h3');
    if (drawerHeader) drawerHeader.innerHTML = `<span>📊</span> ${ui.points}`;
    
    const gradingWeightHeader = document.querySelector('#grades-drawer h4:nth-of-type(1)');
    if (gradingWeightHeader) gradingWeightHeader.innerText = ui.gradingWeight;
    
    const yourPointsHeader = document.querySelector('#grades-drawer h4:nth-of-type(2)');
    if (yourPointsHeader) yourPointsHeader.innerText = ui.yourPoints;
    
    const progressHeader = document.querySelector('#grades-drawer h4:nth-of-type(3)');
    if (progressHeader) progressHeader.innerText = ui.yourProgress;

    // Populate course titles
    const titleEl = document.getElementById('course-title');
    const subtitleEl = document.getElementById('course-subtitle');
    const semesterEl = document.getElementById('course-semester');
    const deptEl = document.getElementById('course-department');
    const instEl = document.getElementById('course-institution');

    if (titleEl) titleEl.innerText = courseInfo.title;
    if (subtitleEl) subtitleEl.innerText = courseInfo.subtitle;
    if (semesterEl) semesterEl.innerText = courseInfo.semester;
    if (deptEl) deptEl.innerText = courseInfo.department;
    if (instEl) instEl.innerText = courseInfo.institution;
    
    // Populate grading breakdown
    const gradingContainer = document.getElementById('grading-container');
    if (gradingContainer && courseInfo.grading) {
        gradingContainer.innerHTML = courseInfo.grading.map(item => `
            <div class="flex justify-between items-center py-2.5 border-b border-slate-800 text-sm">
                <span class="text-slate-400 font-medium">${item.label}</span>
                <span class="text-cyan-400 font-mono font-bold">${item.value}</span>
            </div>
        `).join('');
    }

    renderPortalProgress();
    renderRoadmapGrid();
    
    // Explicitly handle hero image click
    const heroImg = document.getElementById('hero-course-image');
    if (heroImg) {
        heroImg.addEventListener('click', (e) => {
            e.stopPropagation();
            if (window.openLightbox) {
                window.openLightbox(heroImg.src, heroImg.alt);
            }
        });
    }
    
    console.log("Portal initialization complete");
}

function setupPortalEventListeners() {
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
}

function renderPortalProgress() {
    // Calculate completion progress
    const activeWeeks = Object.values(weeksData).filter(w => w.active && w.id !== '13' && w.id !== '14'); 
    
    let totalPointsEarned = 0;
    const maxPointsPossible = activeWeeks.length * 5;
    
    const pointsListHtml = activeWeeks.map(w => {
        const quizDone = localStorage.getItem(`quiz_completed_week_${w.id}`) === 'true';
        const psDone = localStorage.getItem(`problemset_completed_week_${w.id}`) === 'true';
        
        const quizPts = quizDone ? 1 : 0;
        const psPts = psDone ? 4 : 0;
        const weekPts = quizPts + psPts;
        totalPointsEarned += weekPts;
        
        const weekLabel = currentLang === 'de' ? 'Woche' : 'Week';
        
        return `
            <div class="p-3 rounded-xl bg-slate-900/40 border border-slate-800 space-y-2">
                <div class="flex justify-between items-center text-xs font-mono font-bold text-white">
                    <span>${weekLabel} ${w.id}: ${w.title.substring(0, 30)}${w.title.length > 30 ? '...' : ''}</span>
                    <span class="text-cyan-400 font-mono font-bold">${weekPts} / 5 ${ui.pointsLabel}</span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs">
                    <div class="flex items-center gap-1.5 p-1.5 rounded bg-slate-950/35 border ${quizDone ? 'border-emerald-500/20 text-emerald-400' : 'border-slate-800 text-slate-500'}">
                        <span>${quizDone ? '✓' : '○'}</span>
                        <span class="font-medium">Quiz (1 ${ui.pointsLabel})</span>
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
                        <span class="font-medium">ProbSet (4 ${ui.pointsLabel})</span>
                    </label>
                </div>
            </div>
        `;
    }).join('');

    const pointsListContainer = document.getElementById('points-list-container');
    const totalPointsLabel = document.getElementById('portal-total-points');
    
    if (pointsListContainer) {
        pointsListContainer.innerHTML = pointsListHtml;
        
        pointsListContainer.querySelectorAll('.problemset-checkbox').forEach(chk => {
            chk.addEventListener('change', (e) => {
                const weekId = e.target.getAttribute('data-week');
                const isChecked = e.target.checked;
                localStorage.setItem(`problemset_completed_week_${weekId}`, isChecked ? 'true' : 'false');
                
                renderPortalProgress();
                renderRoadmapGrid();
            });
        });
    }
    
    if (totalPointsLabel) {
        totalPointsLabel.innerText = `${totalPointsEarned} / ${maxPointsPossible} ${ui.pointsLabel}`;
    }
    
    const progressPercent = maxPointsPossible > 0 ? Math.round((totalPointsEarned / maxPointsPossible) * 100) : 0;
    
    const progressFill = document.getElementById('portal-progress-fill');
    const progressText = document.getElementById('portal-progress-text');
    if (progressFill && progressText) {
        progressFill.style.width = `${progressPercent}%`;
        const completedText = ui.completed;
        progressText.innerText = `${progressPercent}% ${completedText} (${totalPointsEarned}/${maxPointsPossible} ${ui.pointsLabel})`;
    }
}

function renderRoadmapGrid() {
    const roadmapContainer = document.getElementById('roadmap-grid');
    if (roadmapContainer) {
        roadmapContainer.innerHTML = Object.values(weeksData).map(w => {
            const isCompleted = localStorage.getItem(`quiz_completed_week_${w.id}`) === 'true';
            const moduleName = modules[w.module] || (currentLang === 'de' ? 'Fortgeschrittene Methoden' : 'Advanced Methods');
            const weekLabel = currentLang === 'de' ? 'Woche' : 'Week';
            
            if (w.active) {
                return `
                    <div class="glass-card rounded-2xl p-6 glow-cyan flex flex-col justify-between border-t-2 border-t-cyan-500/35 relative overflow-hidden group">
                        ${isCompleted ? `
                            <div class="absolute top-3 right-3 w-6 h-6 bg-emerald-500/20 text-emerald-400 rounded-full font-mono font-bold flex items-center justify-center border border-emerald-500/30 shadow-lg shadow-emerald-500/5" title="Abgeschlossen">
                                ✓
                            </div>
                        ` : ''}
                        <div>
                            <div class="text-xs font-mono text-cyan-400 uppercase tracking-wider mb-2">${moduleName}</div>
                            <h3 class="text-xl font-bold text-white mb-2 group-hover:text-cyan-400 transition-colors">${weekLabel} ${w.id}: ${w.title}</h3>
                            <p class="text-sm text-slate-400 leading-relaxed mb-6">${w.description}</p>
                        </div>
                        <a 
                            href="week.html?id=${w.id}" 
                            class="inline-flex items-center gap-2 text-sm font-bold text-cyan-400 hover:text-cyan-300 group-hover:translate-x-1 transition-transform"
                        >
                            ${ui.materialsBtn} &rarr;
                        </a>
                    </div>
                `;
            } else {
                return `
                    <div class="glass-card rounded-2xl p-6 border-t-2 border-t-slate-800 week-locked flex flex-col justify-between">
                        <div>
                            <div class="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2">${moduleName}</div>
                            <h3 class="text-xl font-bold text-slate-500 mb-2 flex items-center gap-2">
                                ${weekLabel} ${w.id}: ${w.title}
                                <span class="text-base text-slate-600">🔒</span>
                            </h3>
                            <p class="text-sm text-slate-500 leading-relaxed mb-6">${w.description}</p>
                        </div>
                        <span class="text-xs font-mono text-amber-500/75 uppercase tracking-widest font-bold">${ui.locked}</span>
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
    // Localize static elements
    const syllabusHeader = document.querySelector('aside nav div.text-slate-500');
    if (syllabusHeader) syllabusHeader.innerText = ui.syllabus;
    
    const backToPortalBtn = document.querySelector('aside div.border-t a');
    if (backToPortalBtn) backToPortalBtn.innerHTML = `<span>&larr;</span> ${ui.backToPortal}`;
    
    const backToDashboardLink = document.getElementById('back-to-dashboard');
    if (backToDashboardLink) backToDashboardLink.innerText = `🏠 ${ui.backToDashboard}`;
    
    const tabIntro = document.getElementById('tab-btn-intro');
    if (tabIntro) tabIntro.innerHTML = `<span>📖</span> ${ui.theoryIntro}`;
    
    const tabInfo = document.getElementById('tab-btn-infographic');
    if (tabInfo) tabInfo.innerHTML = `<span>📊</span> ${ui.infographic}`;
    
    const tabPS = document.getElementById('tab-btn-problemset');
    if (tabPS) tabPS.innerHTML = `<span>💻</span> ${ui.problemSet}`;
    
    const tabQuiz = document.getElementById('tab-btn-quiz');
    if (tabQuiz) tabQuiz.innerHTML = `<span>🧠</span> ${ui.quiz}`;
    
    const tabStories = document.getElementById('tab-btn-stories');
    if (tabStories) tabStories.innerHTML = `<span>🎬</span> ${ui.stories}`;

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
    const moduleName = modules[week.module] || (currentLang === 'de' ? 'Fortgeschrittene Methoden' : 'Advanced Methods');
    const weekLabel = currentLang === 'de' ? 'Woche' : 'Week';
    
    document.getElementById('header-week-title').innerText = `${weekLabel} ${week.id}: ${week.title}`;
    document.getElementById('header-module-title').innerText = moduleName;
    document.title = `${weekLabel} ${week.id}: ${week.title} - Advanced Modeling & System Simulation`;

    // Localize Tab Buttons
    const tabIntro = document.getElementById('tab-btn-intro');
    const tabInfographic = document.getElementById('tab-btn-infographic');
    const tabProblemSet = document.getElementById('tab-btn-problemset');
    const tabQuiz = document.getElementById('tab-btn-quiz');
    const tabStories = document.getElementById('tab-btn-stories');

    if (tabIntro) tabIntro.innerHTML = `<span>📖</span> ${ui.theoryIntro}`;
    if (tabInfographic) tabInfographic.innerHTML = `<span>📊</span> ${ui.infographic}`;
    if (tabProblemSet) tabProblemSet.innerHTML = `<span>💻</span> ${ui.problemSet}`;
    if (tabQuiz) tabQuiz.innerHTML = `<span>🧠</span> ${ui.quiz}`;
    if (tabStories) tabStories.innerHTML = `<span>✨</span> ${ui.stories}`;

    // Filter tabs based on week data
    const allowedTabs = week.tabs || ['intro', 'infographic', 'problemset', 'quiz', 'stories'];
    const tabButtons = [tabIntro, tabInfographic, tabProblemSet, tabQuiz, tabStories];
    const tabIds = ['intro', 'infographic', 'problemset', 'quiz', 'stories'];

    tabIds.forEach((tabId, idx) => {
        const btn = tabButtons[idx];
        if (btn) {
            if (allowedTabs.includes(tabId)) {
                btn.classList.remove('hidden');
            } else {
                btn.classList.add('hidden');
            }
        }
    });

    // Localize Back to Dashboard link
    const backBtn = document.getElementById('back-to-dashboard');
    if (backBtn) backBtn.innerText = `🏠 ${ui.backToDashboard}`;

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
    
    const weekLabel = currentLang === 'de' ? 'W' : 'W';
    
    listContainer.innerHTML = Object.values(weeksData).map(w => {
        const isActive = w.id === currentWeekId;
        const quizDone = localStorage.getItem(`quiz_completed_week_${w.id}`) === 'true';
        const psDone = localStorage.getItem(`problemset_completed_week_${w.id}`) === 'true';
        const isFullyCompleted = quizDone && psDone;
        const isPartiallyCompleted = quizDone || psDone;
        
        if (w.active) {
            let statusIndicator = `<span class="w-1.5 h-1.5 rounded-full bg-cyan-400" title="${currentLang === 'de' ? 'Aktiv' : 'Active'}"></span>`;
            if (isFullyCompleted) {
                statusIndicator = `<span class="text-emerald-400 font-bold text-sm leading-none" title="${currentLang === 'de' ? 'Vollständig abgeschlossen' : 'Fully completed'} (5/5 ${ui.pointsLabel})">✓</span>`;
            } else if (isPartiallyCompleted) {
                statusIndicator = `<span class="text-amber-400 font-bold text-xs leading-none" title="${currentLang === 'de' ? 'Teilweise abgeschlossen' : 'Partially completed'} (1/5 ${currentLang === 'de' ? 'oder' : 'or'} 4/5 ${ui.pointsLabel})">◐</span>`;
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
                        <span class="truncate pr-2">${weekLabel}${w.id}: ${w.title}</span>
                        ${statusIndicator}
                    </a>
                </li>
            `;
        } else {
            return `
                <li>
                    <div 
                        class="flex items-center justify-between px-4 py-3 rounded-lg text-sm text-slate-600 cursor-not-allowed select-none"
                        title="${ui.locked}"
                    >
                        <span class="truncate pr-2">${weekLabel}${w.id}: ${w.title}</span>
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
        quiz: document.getElementById('tab-btn-quiz'),
        stories: document.getElementById('tab-btn-stories')
    };

    const week = weeksData[currentWeekId];
    const allowedTabs = week.tabs || ['intro', 'infographic', 'problemset', 'quiz', 'stories'];

    Object.keys(tabButtons).forEach(tab => {
        const btn = tabButtons[tab];
        if (btn) {
            if (allowedTabs.includes(tab)) {
                btn.style.display = 'flex';
                // Customize tab text for Week 13
                if (tab === 'intro' && currentWeekId === '13') {
                    btn.innerHTML = currentLang === 'de' ? `<span>💡</span> Themenvorschläge & Pitches` : `<span>💡</span> Topic Suggestions & Pitches`;
                } else if (tab === 'intro') {
                    btn.innerHTML = `<span>📖</span> ${ui.theoryIntro}`;
                } else if (tab === 'infographic') {
                    btn.innerHTML = `<span>📊</span> ${ui.infographic}`;
                } else if (tab === 'problemset') {
                    btn.innerHTML = `<span>💻</span> ${ui.problemSet}`;
                } else if (tab === 'quiz') {
                    btn.innerHTML = `<span>🧠</span> ${ui.quiz}`;
                } else if (tab === 'stories') {
                    btn.innerHTML = `<span>🎬</span> ${ui.stories}`;
                }
            } else {
                btn.style.display = 'none';
            }
        }
    });

    Object.keys(tabButtons).forEach(tab => {
        const btn = tabButtons[tab];
        if (btn && allowedTabs.includes(tab)) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                loadTabContent(tab);
            });
        }
    });
}

function updateActiveTabUI(selectedTab) {
    activeTab = selectedTab;
    const tabs = ['intro', 'infographic', 'problemset', 'quiz', 'stories'];
    
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


function formatMarkdown(text) {
    if (!text) return '';
    // Bold: **text** -> <strong class="text-white">text</strong>
    return text.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white">$1</strong>');
}

function loadTabContent(tab) {
    const week = weeksData[currentWeekId];
    const allowedTabs = week.tabs || ['intro', 'infographic', 'problemset', 'quiz', 'stories'];
    if (!allowedTabs.includes(tab)) {
        tab = allowedTabs[0] || 'intro';
    }
    updateActiveTabUI(tab);
    const contentArea = document.getElementById('tab-viewport-content');
    if (!contentArea) return;

    // Show loading state
    contentArea.innerHTML = `
        <div class="flex flex-col items-center justify-center py-20 space-y-4">
            <div class="w-10 h-10 border-4 border-cyan-500/20 border-t-cyan-500 rounded-full animate-spin"></div>
            <p class="text-slate-500 font-mono text-sm">${ui.loading}</p>
        </div>
    `;

    const weekPath = `weeks/week${currentWeekId}`;
    const langSuffix = currentLang === 'en' ? '_en' : '';

    if (tab === 'intro') {
        // Try loading language specific version, fallback to default
        const fileToLoad = `${weekPath}/introduction${langSuffix}.html`;
        fetch(`${fileToLoad}?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) {
                    if (langSuffix !== '') {
                        // Fallback to German if English not found
                        return fetch(`${weekPath}/introduction.html?v=${Date.now()}`).then(r => r.text());
                    }
                    throw new Error(ui.errorIntro);
                }
                return res.text();
            })
            .then(html => {
                const formattedHtml = formatMarkdown(html);
                contentArea.innerHTML = `<div class="animate-slide-up space-y-6">${formattedHtml}</div>`;
                
                // Execute scripts manually
                const scripts = contentArea.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                    newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                });

                highlightCodeSnippets(contentArea);
                setupImageLightbox(contentArea);
                renderMath(contentArea);
                renderMermaid(contentArea);
            })
            .catch(err => {
                contentArea.innerHTML = renderErrorState(ui.errorIntro, err.message);
            });
            
    } else if (tab === 'infographic') {
        const fileToLoad = `${weekPath}/infographic${langSuffix}.html`;
        contentArea.innerHTML = `
            <div class="animate-slide-up space-y-4">
                <div class="flex justify-between items-center text-xs text-slate-400 font-mono mb-2">
                    <span>💡 ${currentLang === 'de' ? 'Tipp: Interagiere mit den Diagrammen für Detailinfos' : 'Tip: Interact with the diagrams for details'}</span>
                    <button id="iframe-reload-btn" class="hover:text-cyan-400 transition-colors">🔄 ${currentLang === 'de' ? 'Neu laden' : 'Reload'}</button>
                </div>
                <div class="iframe-container shadow-2xl border border-slate-800">
                    <iframe 
                        id="infographic-iframe" 
                        src="${fileToLoad}?v=${Date.now()}"
                        allow="fullscreen"
                    ></iframe>
                </div>
            </div>
        `;
        
        const reloadBtn = document.getElementById('iframe-reload-btn');
        if (reloadBtn) {
            reloadBtn.addEventListener('click', () => {
                const iframe = document.getElementById('infographic-iframe');
                if (iframe) iframe.src = `${fileToLoad}?v=${Date.now()}`;
            });
        }
        
    } else if (tab === 'problemset') {
        const fileToLoad = `${weekPath}/problemset${langSuffix}.html`;
        fetch(`${fileToLoad}?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) {
                    if (langSuffix !== '') {
                        return fetch(`${weekPath}/problemset.html?v=${Date.now()}`).then(r => r.text());
                    }
                    throw new Error(ui.errorProblemSet);
                }
                return res.text();
            })
            .then(html => {
                const psDone = localStorage.getItem(`problemset_completed_week_${currentWeekId}`) === 'true';
                const formattedHtml = formatMarkdown(html);
                
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
                                <h4 class="text-white font-bold text-base">Problem Set ${currentLang === 'de' ? 'Abgabestatus' : 'Submission Status'}</h4>
                                <p class="text-xs text-slate-400 font-mono" id="problemset-status-text">
                                    ${psDone ? 'Status: ' + ui.statusDone + ' (+4 ' + ui.pointsLabel + ')' : 'Status: ' + ui.statusPending + ' (' + (currentLang === 'de' ? 'Wert' : 'Value') + ': 4 ' + ui.pointsLabel + ')'}
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
                            ${psDone ? ui.markUndone : ui.markDone}
                        </button>
                    </div>
                `;
                
                contentArea.innerHTML = `<div class="animate-slide-up space-y-6">${statusCardHtml}${formattedHtml}</div>`;
                
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
                            statusText.innerHTML = `Status: ${ui.statusDone} (+4 ${ui.pointsLabel})`;
                            toggleBtn.className = "px-5 py-2.5 rounded-xl font-bold font-mono text-xs shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 border focus:outline-none bg-emerald-600 hover:bg-emerald-500 border-emerald-500/40 text-white shadow-emerald-600/10";
                            toggleBtn.innerText = ui.markUndone;
                        } else {
                            statusCard.className = "glass-card rounded-2xl p-6 border flex flex-col sm:flex-row justify-between items-center gap-4 mb-6 transition-all duration-300 border-cyan-500/25 bg-cyan-950/5";
                            statusIcon.className = "w-12 h-12 rounded-xl flex items-center justify-center text-xl font-bold transition-all duration-300 bg-cyan-500/10 text-cyan-400";
                            statusIcon.innerHTML = "📝";
                            statusText.innerHTML = `Status: ${ui.statusPending} (${currentLang === 'de' ? 'Wert' : 'Value'}: 4 ${ui.pointsLabel})`;
                            toggleBtn.className = "px-5 py-2.5 rounded-xl font-bold font-mono text-xs shadow-lg transition-all duration-200 hover:scale-105 active:scale-95 border focus:outline-none bg-slate-900 hover:bg-cyan-500/5 border-slate-800 hover:border-cyan-500/50 text-cyan-400 shadow-cyan-500/5";
                            toggleBtn.innerText = ui.markDone;
                        }
                        
                        // Update sidebar navigation checks
                        renderSidebar();
                    });
                }

                highlightCodeSnippets(contentArea);
                addCopyButtonsToCode(contentArea);
                setupImageLightbox(contentArea);
                renderMath(contentArea);
                renderMermaid(contentArea);
            })
            .catch(err => {
                contentArea.innerHTML = renderErrorState(ui.errorProblemSet, err.message);
            });
            
    } else if (tab === 'quiz') {
        const fileToLoad = `${weekPath}/quiz${langSuffix}.json`;
        fetch(`${fileToLoad}?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) {
                    if (langSuffix !== '') {
                        return fetch(`${weekPath}/quiz.json?v=${Date.now()}`).then(r => r.json());
                    }
                    throw new Error(ui.errorQuiz);
                }
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
                contentArea.innerHTML = renderErrorState(ui.errorQuiz, err.message);
            });
    } else if (tab === 'stories') {
        const fileToLoad = `${weekPath}/stories${langSuffix}.html`;
        fetch(`${fileToLoad}?v=${Date.now()}`)
            .then(res => {
                if (!res.ok) {
                    if (langSuffix !== '') {
                        return fetch(`${weekPath}/stories.html?v=${Date.now()}`).then(r => r.text());
                    }
                    throw new Error(ui.errorStories);
                }
                return res.text();
            })
            .then(html => {
                const formattedHtml = formatMarkdown(html);
                contentArea.innerHTML = `<div class="animate-slide-up space-y-6">${formattedHtml}</div>`;
                
                // Manually execute scripts
                const scripts = contentArea.querySelectorAll('script');
                scripts.forEach(oldScript => {
                    const newScript = document.createElement('script');
                    Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                    newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                    oldScript.parentNode.replaceChild(newScript, oldScript);
                });

                highlightCodeSnippets(contentArea);
                setupImageLightbox(contentArea);
                renderMath(contentArea);
                renderMermaid(contentArea);
            })
            .catch(err => {
                contentArea.innerHTML = renderErrorState(ui.errorStories, err.message);
            });
    }
}

function renderErrorState(title, message) {
    return `
        <div class="text-center py-16 px-4 glass-card rounded-2xl border-t-4 border-rose-500 max-w-lg mx-auto space-y-4">
            <div class="text-4xl text-rose-500">⚠</div>
            <h3 class="text-xl font-bold text-white">${title}</h3>
            <p class="text-sm text-slate-400 font-mono">${message}</p>
            <p class="text-xs text-slate-500 leading-relaxed">${currentLang === 'de' ? 'Bitte stelle sicher, dass die Dateistruktur lokal übereinstimmt.' : 'Please ensure the file structure matches locally.'}</p>
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

    window.openLightbox = function(src, alt) {
        const img = lightbox.querySelector('#lightbox-img');
        const caption = lightbox.querySelector('#lightbox-caption');
        const content = lightbox.querySelector('#lightbox-content');
        
        img.src = src;
        caption.innerText = alt || (currentLang === 'de' ? 'Abbildung' : 'Figure');
        
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
        
        // Find closest wrapper (relative container or glass-card) that holds overlays
        let wrapper = img;
        if (img.parentElement && img.parentElement.classList.contains('relative')) {
            wrapper = img.parentElement;
        } else if (img.parentElement && img.parentElement.parentElement && (img.parentElement.parentElement.classList.contains('glass-card') || img.parentElement.parentElement.classList.contains('relative'))) {
            wrapper = img.parentElement.parentElement;
        }
        
        wrapper.classList.add('cursor-zoom-in');
        img.classList.add('cursor-zoom-in');
        
        // Add hover styles to wrapper/image
        wrapper.classList.add('hover:brightness-95', 'transition-all', 'duration-200');
        
        const clickHandler = (e) => {
            e.stopPropagation();
            openLightbox(img.src, img.alt);
        };

        wrapper.addEventListener('click', clickHandler);
        img.addEventListener('click', clickHandler);
    });
}

function renderMermaid(container) {
    if (window.mermaid) {
        window.mermaid.initialize({
            startOnLoad: false,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {
                background: '#090d16',
                primaryColor: '#0f172a',
                primaryTextColor: '#f8fafc',
                lineColor: '#06b6d4',
                textColor: '#f8fafc',
                fontSize: '12px'
            }
        });
        
        const elements = container.querySelectorAll('.mermaid');
        if (elements.length > 0) {
            window.mermaid.run({
                nodes: Array.from(elements)
            });
        }
    }
}
