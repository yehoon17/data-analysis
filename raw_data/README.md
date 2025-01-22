### 1. Kaggle CLI 설치

```bash
pip install kaggle
```

### 2. API Credentials 설정

1. **Kaggle 계정 설정 페이지로 이동:**
   - Kaggle 계정에 로그인한 상태에서 [Kaggle API 페이지](https://www.kaggle.com/docs/api) 접속
   - `Create New API Token` 버튼을 눌러서 `kaggle.json` 파일을 다운로드

2. **`kaggle.json` 파일 이동:**  
   - `kaggle.json` 파일을 `~/.kaggle/` 디렉터리에 이동
   - Windows인 경우: `C:\Users\{사용자명}\.kaggle`

### 3. 설치 확인
```bash
kaggle --version
```
