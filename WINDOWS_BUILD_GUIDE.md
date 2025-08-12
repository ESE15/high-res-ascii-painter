# Windows 포터블 실행 파일 빌드 가이드

## 문제 상황
Linux/WSL에서 빌드한 실행 파일이 Windows에서 실행되지 않는 문제가 발생할 수 있습니다. 이는 PyInstaller가 크로스 플랫폼 빌드를 지원하지 않기 때문입니다.

## 해결 방법

### 방법 1: Windows에서 직접 빌드 (권장)

#### 1단계: Python 설치
- [Python 공식 웹사이트](https://python.org)에서 Python 3.10+ 설치
- 설치 시 "Add Python to PATH" 옵션 체크

#### 2단계: uv 설치
PowerShell을 관리자 권한으로 실행하고:
```powershell
# uv 설치
irm https://astral.sh/uv/install.ps1 | iex

# 또는 pip로 설치
pip install uv
```

#### 3단계: 프로젝트 설정
```powershell
# 프로젝트 디렉토리로 이동
cd path\to\high-res-ascii-painter

# 개발 의존성 포함 설치
uv sync --dev
```

#### 4단계: 빌드 실행
```powershell
# Python 빌드 스크립트 실행
uv run python build_windows.py

# 또는 배치 파일 사용
.\build_windows.bat
```

#### 5단계: 결과 확인
빌드 성공 시 `dist\windows\` 폴더에 다음 파일들이 생성됩니다:
- `ascii-painter.exe` - 포터블 실행 파일
- `README.md` - 사용법 설명

### 방법 2: GitHub Actions를 통한 자동 빌드

프로젝트에 GitHub Actions 워크플로우를 추가하여 자동으로 Windows 빌드를 생성할 수 있습니다.

#### `.github/workflows/build-windows.yml` 파일 생성:

```yaml
name: Build Windows Executable

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:  # 수동 실행 가능

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install uv
      uses: astral-sh/setup-uv@v3
      with:
        version: "latest"
    
    - name: Install dependencies
      run: uv sync --dev
    
    - name: Build executable
      run: uv run python build_windows.py
    
    - name: Upload artifact
      uses: actions/upload-artifact@v4
      with:
        name: ascii-painter-windows-x64
        path: dist/windows/
        retention-days: 30
```

### 방법 3: Docker를 사용한 Windows 빌드

Windows 컨테이너를 사용하여 빌드할 수 있습니다 (고급 사용자용).

## 빌드 확인 방법

빌드가 성공했는지 확인하는 방법:

```cmd
# 실행 파일 정보 확인
ascii-painter.exe --help

# 파일 속성 확인 (Windows에서)
# 파일을 우클릭 → 속성 → 세부 정보 탭에서 아키텍처 확인
```

## 문제 해결

### 일반적인 오류들:

1. **"이 앱은 PC에서 실행할 수 없습니다"**
   - 32비트/64비트 아키텍처 불일치
   - 다른 OS에서 빌드된 실행 파일

2. **"Windows에서 이 파일을 열 수 없습니다"**
   - 실행 파일이 손상되었거나 호환되지 않음
   - Windows에서 다시 빌드 필요

3. **빌드 시 "pyinstaller not found" 오류**
   ```powershell
   uv add --dev pyinstaller
   uv sync --dev
   ```

4. **빌드 시 권한 오류**
   - PowerShell을 관리자 권한으로 실행
   - 바이러스 백신 소프트웨어 일시 비활성화

## 최종 권장사항

**가장 확실한 방법은 Windows 10/11 환경에서 직접 빌드하는 것입니다.**

1. Windows PC에서 Python과 uv 설치
2. 프로젝트 클론 또는 다운로드
3. `uv sync --dev` 실행
4. `uv run python build_windows.py` 실행
5. `dist\windows\ascii-painter.exe` 사용

이렇게 빌드한 실행 파일은 Windows 10/11 64비트에서 정상적으로 작동할 것입니다.
