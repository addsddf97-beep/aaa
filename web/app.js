document.addEventListener('DOMContentLoaded', async () => {
    const projectsGrid = document.getElementById('projects-grid');
    const dataPaths = ['data/projects.json', '../data/projects.json'];
    const modal = document.getElementById('detail-modal');
    const modalClose = document.getElementById('modal-close');

    try {
        const allItems = await loadTimelineData(dataPaths);
        renderTimeline(projectsGrid, allItems);
        setupFilters(projectsGrid, allItems);
        setupDarkMode();
        setupModalClose(modal, modalClose);
    } catch (error) {
        console.error('로드 실패:', error);
        if (projectsGrid) projectsGrid.innerHTML = '<p class="error">데이터를 불러오지 못했습니다.</p>';
    }
});

async function loadTimelineData(paths) {
    let lastError;
    for (const path of paths) {
        try {
            const response = await fetch(path);
            if (!response.ok) throw new Error();
            return await response.json();
        } catch (error) { lastError = error; }
    }
    throw lastError;
}

function setupDarkMode() {
    const toggleSwitch = document.getElementById('darkmode-toggle');
    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        if (toggleSwitch) toggleSwitch.checked = true;
    }
    if (toggleSwitch) {
        toggleSwitch.addEventListener('change', (e) => {
            if (e.target.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light');
            }
        });
    }
}

function setupFilters(container, items) {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const brandTitle = document.getElementById('brand-title');
    filterButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            e.target.classList.add('active');
            const filterValue = e.target.getAttribute('data-filter');
            if (brandTitle) {
                brandTitle.className = '';
                brandTitle.classList.add(`theme-${filterValue}`);
            }
            const filtered = filterValue === 'all' ? items : items.filter(item => (item.type || 'project') === filterValue);
            renderTimeline(container, filtered);
        });
    });
}

function renderTimeline(container, items) {
    if (!container) return;
    container.innerHTML = '';
    if (items.length === 0) {
        container.innerHTML = '<p class="empty">정보가 없습니다.</p>';
        return;
    }
    const fragment = document.createDocumentFragment();
    items.forEach(item => {
        const card = document.createElement('article');
        const type = item.type || 'project';
        card.className = `project-card ${type}`;
        
        const labels = { 'project': 'Project', 'experience': 'Experience', 'education': 'Education', 'skill': 'Skill Stack', 'award': 'Award' };
        card.innerHTML = `
            <div class="item-meta">
                <span class="type-badge">${labels[type] || 'Info'}</span>
                <span class="item-period">${item.year || ''}</span>
            </div>
            <h3>${item.title || '내용 없음'}</h3>
            <p>${item.description || ''}</p>
            <div class="tags">${(item.tags || []).map(t => `<span class="badge">${t}</span>`).join('')}</div>
        `;
        
        if (item.link && item.link !== '#') {
            const link = document.createElement('a');
            link.className = 'project-link';
            link.href = item.link; link.target = '_blank'; link.textContent = '자세히 보기';
            card.appendChild(link);
        }
        
        card.addEventListener('click', (e) => {
            if (e.target.classList.contains('project-link')) return;
            openDetailModal(item);
        });
        fragment.appendChild(card);
    });
    container.appendChild(fragment);
}

function openDetailModal(item) {
    const modal = document.getElementById('detail-modal');
    const type = item.type || 'project';
    modal.className = `modal-overlay active ${type}`;
    
    const labels = { 'project': 'Project', 'experience': 'Experience', 'education': 'Education', 'skill': 'Skill Stack', 'award': 'Award' };
    document.getElementById('modal-type').textContent = labels[type] || 'Info';
    document.getElementById('modal-year').textContent = item.year || '';
    document.getElementById('modal-title').textContent = item.title || '';
    document.getElementById('modal-description').textContent = item.detail || item.description || '';
    document.getElementById('modal-tags').innerHTML = (item.tags || []).map(t => `<span class="badge">${t}</span>`).join('');
    
    const mLink = document.getElementById('modal-link');
    if (item.link && item.link !== '#') { mLink.style.display = 'inline-flex'; mLink.href = item.link; }
    else { mLink.style.display = 'none'; }
}

function setupModalClose(modal, closeBtn) {
    if (!closeBtn || !modal) return;
    closeBtn.addEventListener('click', () => modal.classList.remove('active'));
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('active'); });
}



