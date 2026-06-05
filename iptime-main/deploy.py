"""Hugging Face Space 배포 스크립트 - python deploy.py 실행"""
import sys

from huggingface_hub import HfApi, create_repo, upload_folder
from huggingface_hub.errors import HfHubHTTPError

DEFAULT_SPACE_NAME = "hand-gesture-ai"
FILES = [
    "app.py",
    "Dockerfile",
    "README.md",
    "requirements.txt",
    "labels.txt",
    "templates/index.html",
    "model/hand_model.h5",
]

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass


def ask(prompt, default=None):
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    value = input(prompt).strip()
    return value or default


def create_space(repo_id, token):
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            exist_ok=True,
            token=token,
        )
        print("Space 준비 완료")
        return True
    except HfHubHTTPError as e:
        if "403" in str(e):
            print()
            print("Space 자동 생성은 안 됩니다. 웹에서 먼저 만들어주세요:")
            print("  1. https://huggingface.co/new-space")
            print(f"  2. Space name: {repo_id.split('/')[1]}")
            print("  3. SDK: Docker")
            print("  4. Create Space 후 이 스크립트 다시 실행")
            print()
            answer = input("웹에서 Space를 이미 만들었나요? (y/n): ").strip().lower()
            return answer == "y"
        print(f"오류: Space 생성 실패 - {e}")
        return False
    except Exception as e:
        print(f"오류: Space 생성 실패 - {e}")
        return False


def main():
    print()
    print("=" * 40)
    print("  손동작 인식 AI - Hugging Face 배포")
    print("=" * 40)
    print()
    print("Token 발급: https://huggingface.co/settings/tokens")
    print("  -> Classic token -> Role: WRITE")
    print()

    token = ask("Access Token (hf_ 로 시작)")
    if not token or not token.startswith("hf_"):
        print("오류: 올바른 Token을 입력해주세요.")
        sys.exit(1)

    api = HfApi(token=token)
    try:
        username = api.whoami(token=token)["name"]
    except Exception:
        print("오류: Token이 틀렸습니다. Write 권한 Token을 확인해주세요.")
        sys.exit(1)

    print(f"계정 확인: {username}")

    space_name = ask("Space 이름", DEFAULT_SPACE_NAME)
    repo_id = f"{username}/{space_name}"

    print()
    print(f"배포 대상: https://huggingface.co/spaces/{repo_id}")

    if not create_space(repo_id, token):
        sys.exit(1)

    try:
        print("파일 업로드 중...")
        upload_folder(
            folder_path=".",
            repo_id=repo_id,
            repo_type="space",
            token=token,
            allow_patterns=FILES,
            commit_message="Deploy hand gesture AI",
        )
    except HfHubHTTPError as e:
        if "404" in str(e):
            print()
            print("오류: Space를 찾을 수 없습니다.")
            print(f"  확인: https://huggingface.co/spaces/{repo_id}")
            print("  웹에서 Space 이름이 같은지, Docker로 만들었는지 확인해주세요.")
        else:
            print(f"오류: 파일 업로드 실패 - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"오류: 파일 업로드 실패 - {e}")
        sys.exit(1)

    print()
    print("배포 완료!")
    print("빌드에 5~15분 걸릴 수 있습니다.")
    print()
    print(f"링크: https://huggingface.co/spaces/{repo_id}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n취소됨")
    input("\nEnter 키를 누르면 종료...")
