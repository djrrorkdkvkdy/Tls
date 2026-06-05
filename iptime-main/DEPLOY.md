# 무료 배포 가이드 (Hugging Face Spaces)

## 1. Hugging Face 가입

1. https://huggingface.co 접속
2. **Sign Up**으로 무료 계정 생성

## 2. Space 만들기

1. 우측 상단 프로필 → **New Space**
2. 아래처럼 설정:
   - **Space name**: `hand-gesture-ai` (원하는 이름)
   - **License**: MIT
   - **Space SDK**: **Docker**
   - **Hardware**: **CPU basic** (무료)
3. **Create Space** 클릭

## 3. 파일 업로드

Space가 만들어지면 **Files** 탭에서 아래 파일들을 업로드합니다.

```
app.py
Dockerfile
README.md
requirements.txt
labels.txt
templates/index.html
model/hand_model.h5
```

또는 Git으로 올리기:

```bash
git clone https://huggingface.co/spaces/내아이디/hand-gesture-ai
cd hand-gesture-ai

# iptime-main 폴더 파일 복사 후
git add .
git commit -m "Deploy hand gesture AI"
git push
```

> Hugging Face 비밀번호 대신 **Access Token**이 필요합니다.  
> Settings → Access Tokens → **New token** (Write 권한)

## 4. 배포 완료

- 빌드에 **5~15분** 걸릴 수 있습니다 (TensorFlow 설치 때문).
- 완료되면 아래 주소로 접속합니다:

```
https://huggingface.co/spaces/내아이디/hand-gesture-ai
```

## 5. 문제 해결

| 문제 | 해결 |
|------|------|
| 빌드 실패 | Space **Logs** 탭에서 오류 확인 |
| 카메라 안 됨 | HTTPS 사이트이므로 카메라 허용 필요 |
| 느림 | 무료 CPU라 첫 로딩이 느릴 수 있음 (1~2분) |
