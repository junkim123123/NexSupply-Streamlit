# Vercel assetlinks.json 404 오류 완벽 해결 가이드

**최종 업데이트: 2025년 11월 28일**

---

## 🔍 문제 원인

Vercel에서 `/.well-known/assetlinks.json` 경로에 접근할 때 **404 오류**가 발생하는 경우:

1. **파일이 실제로 배포되지 않음** - 가장 흔한 원인
2. **MIME 타입이 올바르지 않음** - `Content-Type: application/json` 필요
3. **파일 경로가 잘못됨** - `.well-known` 폴더 위치 확인 필요

---

## ✅ 해결 방법

### 1단계: 파일 구조 확인

**올바른 파일 구조:**

```
프로젝트 루트/
├── .well-known/
│   └── assetlinks.json  ✅ 정확한 경로
├── vercel.json          ✅ Vercel 설정
├── manifest.json
└── service-worker.js
```

**확인 사항:**
- 폴더 이름: `.well-known` (앞에 점 있음)
- 파일 이름: `assetlinks.json` (소문자, 복수형)
- 파일이 Git에 커밋되어 있는지 확인

### 2단계: vercel.json 설정

프로젝트 루트에 `vercel.json` 파일 생성:

```json
{
  "version": 2,
  "headers": [
    {
      "source": "/.well-known/assetlinks.json",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/json; charset=utf-8"
        },
        {
          "key": "Cache-Control",
          "value": "public, max-age=86400, immutable"
        },
        {
          "key": "Content-Disposition",
          "value": "inline"
        },
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    },
    {
      "source": "/manifest.json",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/json; charset=utf-8"
        }
      ]
    },
    {
      "source": "/service-worker.js",
      "headers": [
        {
          "key": "Content-Type",
          "value": "application/javascript; charset=utf-8"
        },
        {
          "key": "Cache-Control",
          "value": "public, max-age=0"
        }
      ]
    }
  ],
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### 3단계: Git 커밋 및 푸시

```bash
git add vercel.json
git commit -m "Add vercel.json with assetlinks.json headers"
git push origin main
```

### 4단계: Vercel 재배포 확인

1. **자동 재배포**: Git 푸시 후 Vercel이 자동으로 재배포 시작
2. **수동 재배포**: Vercel 대시보드에서 "Redeploy" 클릭
3. **배포 상태 확인**: 약 1-2분 후 "Ready" 상태 확인

### 5단계: 테스트

**브라우저에서 확인:**
```
https://your-domain.vercel.app/.well-known/assetlinks.json
```

**터미널에서 확인:**
```bash
curl -I https://your-domain.vercel.app/.well-known/assetlinks.json
```

**성공 시:**
- HTTP 상태 코드: `200 OK`
- Content-Type: `application/json; charset=utf-8`
- JSON 내용이 올바르게 표시됨

---

## 🔧 문제 해결

### 파일이 여전히 404인 경우

1. **파일 존재 확인**
   ```bash
   # 로컬에서
   ls -la .well-known/assetlinks.json
   
   # Git에 커밋되었는지 확인
   git ls-files .well-known/assetlinks.json
   ```

2. **Vercel Output Directory 확인**
   - Vercel 대시보드 → Settings → Build & Development
   - Output Directory 값 확인
   - 해당 폴더 안에 `.well-known/assetlinks.json` 있는지 확인

3. **파일 경로 재확인**
   - 폴더 이름: `.well-known` (정확히)
   - 파일 이름: `assetlinks.json` (정확히)
   - 대소문자 구분 확인

### MIME 타입 문제

**문제:** 파일은 보이지만 Content-Type이 `text/html`로 표시됨

**해결:** `vercel.json`의 `headers` 설정이 올바른지 확인

---

## 📋 체크리스트

### 배포 전
- [ ] `.well-known/assetlinks.json` 파일 존재 확인
- [ ] 파일 경로가 정확한지 확인 (`.well-known/assetlinks.json`)
- [ ] `vercel.json` 파일 생성 및 설정
- [ ] Git에 모든 파일 커밋

### 배포 후
- [ ] Vercel 배포 상태 "Ready" 확인
- [ ] URL 접근 테스트 (200 OK)
- [ ] Content-Type 헤더 확인 (`application/json`)
- [ ] JSON 내용 확인

---

## 🎯 최종 확인

**성공 기준:**
- ✅ HTTP 200 OK
- ✅ Content-Type: `application/json; charset=utf-8`
- ✅ JSON 내용이 올바르게 표시됨
- ✅ Android TWA 검증 통과

---

## 📚 참고 자료

- [Vercel Headers 문서](https://vercel.com/docs/headers)
- [Vercel 프로젝트 설정](https://vercel.com/docs/project-configuration)
- [Android Digital Asset Links](https://developer.android.com/training/app-links/verify-applinks)

---

**이 가이드를 따라하면 assetlinks.json 404 오류가 해결됩니다! 🎉**



