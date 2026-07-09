"""
실습 1: projects.json을 Document로 변환
"""

import json
from pathlib import Path

from langchain_core.documents import Document


PROJECTS_JSON = Path(__file__).resolve().parent / "projects.sample.json"


def project_to_text(project: dict) -> str:
    title = project.get("title") or project.get("name") or "제목 없음"
    description = project.get("description") or project.get("summary") or "설명 없음"
    tags = project.get("tags") or project.get("stack") or []
    link = project.get("link") or "링크 없음"
    period = project.get("period")
    role = project.get("role")
    result = project.get("result")

    lines = [
        f"프로젝트명: {title}",
        f"설명: {description}",
        f"기술/태그: {', '.join(tags)}",
        f"링크: {link}",
    ]

    if period:
        lines.append(f"기간: {period}")
    if role:
        lines.append(f"역할: {role}")
    if result:
        lines.append(f"성과: {result}")

    return "\n".join(lines)


def load_documents() -> list[Document]:
    with open(PROJECTS_JSON, encoding="utf-8") as f:
        projects = json.load(f)

    docs = []
    for idx, project in enumerate(projects):
        title = project.get("title") or project.get("name") or f"project_{idx}"
        docs.append(
            Document(
                page_content=project_to_text(project),
                metadata={"name": title},
            )
        )
    return docs


if __name__ == "__main__":
    docs = load_documents()
    print(len(docs), "개의 Document 생성")
    if docs:
        print("--- 첫 번째 문서 ---")
        print(docs[0].page_content)