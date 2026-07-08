#!/usr/bin/env python3
"""
프로젝트 빌드 스크립트

data/projects/ 디렉토리의 각 프로젝트 폴더에서 project.json을 읽어
하나의 projects.json 파일로 통합합니다.

Usage:
    python data/build.py
"""

import json
from pathlib import Path


def build_projects_json():
    """프로젝트 폴더들을 스캔하여 projects.json 생성"""

    # 경로 설정
    data_dir = Path(__file__).parent
    root_dir = data_dir.parent
    projects_dir = data_dir / "projects"
    output_file = data_dir / "projects.json"
    web_output_file = root_dir / "web" / "data" / "projects.json"

    # projects/ 디렉토리가 없으면 에러
    if not projects_dir.exists():
        print(f"❌ Error: {projects_dir} 디렉토리가 없습니다.")
        print("   data/projects/ 디렉토리를 먼저 생성해주세요.")
        return False

    # 모든 프로젝트 수집
    projects = []
    project_folders = sorted([d for d in projects_dir.iterdir() if d.is_dir()])

    if not project_folders:
        print(f"⚠️  Warning: {projects_dir} 디렉토리가 비어있습니다.")
        print("   프로젝트 폴더를 추가해주세요.")
        return False

    print(f"📂 {len(project_folders)}개의 프로젝트 폴더를 발견했습니다.\n")

    # 각 프로젝트 폴더 처리
    for project_folder in project_folders:
        project_json_path = project_folder / "project.json"

        # project.json 파일 확인
        if not project_json_path.exists():
            print(f"⚠️  Skip: {project_folder.name}/ (project.json 없음)")
            continue

        # JSON 파일 읽기
        try:
            with open(project_json_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)

            # 필수 필드 검증
            required_fields = ["id", "title", "description", "tags", "link"]
            missing_fields = [field for field in required_fields if field not in project_data]

            if missing_fields:
                print(f"❌ Error: {project_folder.name}/project.json")
                print(f"   누락된 필드: {', '.join(missing_fields)}")
                continue

            # 프로젝트 추가
            projects.append(project_data)
            print(f"✅ {project_data['id']}: {project_data['title']}")

        except json.JSONDecodeError as e:
            print(f"❌ Error: {project_folder.name}/project.json - JSON 파싱 실패")
            print(f"   {str(e)}")
            continue
        except Exception as e:
            print(f"❌ Error: {project_folder.name}/project.json - {str(e)}")
            continue

    # projects.json 생성
    if not projects:
        print("\n❌ 유효한 프로젝트가 하나도 없습니다.")
        return False

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)

        web_output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(web_output_file, "w", encoding="utf-8") as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)

        print(f"\n🎉 성공! {output_file.name} 파일이 생성되었습니다.")
        print(f"   웹 배포용 파일: {web_output_file}")
        print(f"   총 {len(projects)}개의 프로젝트가 포함되었습니다.")
        return True

    except Exception as e:
        print(f"\n❌ projects.json 생성 실패: {str(e)}")
        return False


if __name__ == "__main__":
    success = build_projects_json()
    exit(0 if success else 1)
