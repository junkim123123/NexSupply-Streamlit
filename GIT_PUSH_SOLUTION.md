# Git 푸시 권한 문제 해결 가이드

## 문제 상황

```
remote: Permission to junkim123123/nexy-ai-app1.git denied to junkimfrom82-boop.
fatal: unable to access 'https://github.com/junkim123123/nexy-ai-app1.git/'
```

현재 `junkimfrom82-boop` 계정으로 인증되어 있지만, `junkim123123/nexy-ai-app1` 저장소에 접근 권한이 없습니다.

## 해결 방법

### 방법 1: Windows Credential Manager에서 인증 정보 삭제

1. **Windows 자격 증명 관리자 열기**
   - Windows 검색에서 "자격 증명 관리자" 검색
   - 또는 `control /name Microsoft.CredentialManager` 실행

2. **Windows 자격 증명** 탭 선택

3. **GitHub 관련 자격 증명 찾기**
   - `git:https://github.com` 또는 `github.com` 검색

4. **자격 증명 삭제**
   - 해당 항목을 클릭하고 "제거" 또는 "편집" 선택

5. **다시 푸시 시도**
   ```bash
   git push -u origin main
   ```
   - 이번에는 올바른 GitHub 계정으로 로그인하라는 창이 나타납니다
   - `junkim123123` 계정으로 로그인

### 방법 2: 명령어로 자격 증명 삭제

```powershell
# PowerShell에서 실행
cmdkey /list | findstr github

# GitHub 자격 증명이 있다면 삭제
cmdkey /delete:git:https://github.com
```

### 방법 3: Personal Access Token 사용

1. **GitHub에서 Personal Access Token 생성**
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - "Generate new token (classic)" 클릭
   - `repo` 권한 선택
   - 토큰 생성 및 복사

2. **원격 URL에 토큰 포함**
   ```bash
   git remote set-url origin https://<YOUR_TOKEN>@github.com/junkim123123/nexy-ai-app1.git
   git push -u origin main
   ```

### 방법 4: SSH 키 사용 (권장)

1. **SSH 키 생성** (없는 경우)
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **SSH 키를 GitHub에 추가**
   - `C:\Users\kmyun\.ssh\id_ed25519.pub` 파일 내용 복사
   - GitHub → Settings → SSH and GPG keys → New SSH key

3. **원격 URL을 SSH로 변경**
   ```bash
   git remote set-url origin git@github.com:junkim123123/nexy-ai-app1.git
   git push -u origin main
   ```

### 방법 5: GitHub Desktop 사용

1. **GitHub Desktop 설치**
   - https://desktop.github.com/

2. **저장소 열기**
   - File → Add local repository
   - 현재 프로젝트 폴더 선택

3. **푸시**
   - GitHub Desktop에서 "Publish repository" 클릭
   - 올바른 계정으로 로그인

## 저장소 권한 확인

저장소에 대한 접근 권한이 있는지 확인:

1. **GitHub 저장소 확인**
   - https://github.com/junkim123123/nexy-ai-app1 접속
   - Settings → Collaborators에서 자신의 계정 확인

2. **저장소가 비어있는 경우**
   - GitHub에서 저장소를 생성할 때 README를 추가하지 않았는지 확인
   - 빈 저장소로 생성해야 첫 푸시가 가능합니다

## 현재 상태

✅ **로컬 커밋 완료**: 모든 변경사항이 로컬에 안전하게 저장되어 있습니다.

❌ **원격 푸시 대기**: 인증 문제 해결 후 푸시 가능

## 빠른 해결 (가장 간단한 방법)

1. **Windows 자격 증명 관리자 열기**
   ```
   Win + R → control /name Microsoft.CredentialManager
   ```

2. **GitHub 자격 증명 삭제**

3. **다시 푸시**
   ```bash
   git push -u origin main
   ```

4. **브라우저에서 GitHub 로그인**
   - `junkim123123` 계정으로 로그인
   - 권한 승인

---

**참고**: 로컬 커밋은 완료되었으므로, 인증 문제만 해결하면 푸시할 수 있습니다.

