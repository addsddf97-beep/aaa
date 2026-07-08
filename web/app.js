document.addEventListener('DOMContentLoaded', async () => {
    const projectsGrid = document.getElementById('projects-grid');
    const dataPaths = [
        'data/projects.json',
        '../data/projects.json',
    ];

    try {
        const projects = await loadProjects(dataPaths);
        renderProjects(projectsGrid, projects);
    } catch (error) {
        console.error('프로젝트를 불러오는 중 오류 발생:', error);
        projectsGrid.innerHTML = '<p class="error">프로젝트 데이터를 불러오지 못했습니다.</p>';
    }
});

async function loadProjects(paths) {
    let lastError;

    for (const path of paths) {
        try {
            const response = await fetch(path);

            if (!response.ok) {
                throw new Error(`${path}: ${response.status}`);
            }

            const projects = await response.json();

            if (!Array.isArray(projects)) {
                throw new Error(`${path}: 프로젝트 데이터는 배열이어야 합니다.`);
            }

            return projects;
        } catch (error) {
            lastError = error;
        }
    }

    throw lastError;
}

function renderProjects(container, projects) {
    container.innerHTML = '';

    if (projects.length === 0) {
        container.innerHTML = '<p class="empty">등록된 프로젝트가 없습니다.</p>';
        return;
    }

    const fragment = document.createDocumentFragment();

    projects.forEach(project => {
        fragment.appendChild(createProjectCard(project));
    });

    container.appendChild(fragment);
}

function createProjectCard(project) {
    const card = document.createElement('article');
    card.className = 'project-card';

    const title = document.createElement('h3');
    title.textContent = project.title || '제목 없는 프로젝트';

    const description = document.createElement('p');
    description.textContent = project.description || '';

    const tags = document.createElement('div');
    tags.className = 'tags';

    const projectTags = Array.isArray(project.tags) ? project.tags : [];
    projectTags.forEach(tag => {
        const badge = document.createElement('span');
        badge.className = 'badge';
        badge.textContent = tag;
        tags.appendChild(badge);
    });

    const link = document.createElement('a');
    link.className = 'project-link';
    link.href = project.link || '#';
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.textContent = '자세히 보기';

    card.append(title, description, tags, link);
    return card;
}
