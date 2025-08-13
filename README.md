# high-res-ascii-painter

Slack-Optimized ASCII Art Generator

## 설치

### uv 사용 (권장)
```bash
# uv가 설치되어 있지 않은 경우
curl -LsSf https://astral.sh/uv/install.sh | sh

# 프로젝트 설치
uv sync
```

### pip 사용
```bash
pip install -e .
```

### Windows 포터블 실행 파일 빌드

⚠️ **중요**: Windows용 실행 파일은 반드시 Windows 환경에서 빌드해야 합니다!

#### Windows에서 빌드 (권장):
```powershell
# 개발 의존성 포함 설치
uv sync --dev

# Windows 실행 파일 빌드
uv run python build_windows.py

# 또는 배치 파일 사용
.\build_windows.bat
```

#### Linux/WSL에서 시도 (작동하지 않을 수 있음):
```bash
# 경고와 함께 빌드 시도
uv sync --dev
uv run python build_windows.py
```

자세한 빌드 가이드는 [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md)를 참조하세요.

## 사용법

### 쉘 스크립트 사용 (가장 간편)
```bash
# 프로젝트 디렉토리에서 실행
./ascii-painter.sh <image_file> [width] [options]

# 다른 디렉토리에서 절대 경로로 실행
/path/to/high-res-ascii-painter/ascii-painter.sh <image_file> [width] [options]
```

#### PATH에 추가하여 어디서든 실행 (선택사항)
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
export PATH="/path/to/high-res-ascii-painter:$PATH"

# 그 후 어디서든 실행 가능
ascii-painter.sh <image_file> [width] [options]
```

### uv run 사용
```bash
uv run ascii-painter <image_file> [width] [options]
uv run ascii-painter -w <image_url> [width] [options]
```

### 가상환경 활성화 후 사용
```bash
source .venv/bin/activate
ascii-painter <image_file> [width] [options]
ascii-painter -w <image_url> [width] [options]
```

### 전역 설치 후 사용 (선택사항)
```bash
uv tool install .
ascii-painter <image_file> [width] [options]
```

### Windows 포터블 실행 파일 사용
```cmd
# Windows Command Prompt 또는 PowerShell에서
ascii-painter.exe <image_file> [width] [options]
ascii-painter.exe -w <image_url> [width] [options]
ascii-painter.exe --clip [width] [options]
```

## 인수

- `image_file`: 입력 이미지 파일 경로
- `image_url`: 이미지 URL (웹 옵션과 함께 사용)
- `width`: ASCII 아트 너비 (문자 단위, 기본값: 70)

## 옵션

- `-w, --web`: 로컬 파일 대신 URL에서 이미지 다운로드
- `--clip, -v`: 클립보드의 이미지를 사용 (WSL/Windows 환경 필요)
- `-a, --auto-copy`: ASCII 아트 결과를 자동으로 클립보드에 복사
- `--color, -c`: 컬러 출력 활성화 (Slack에서는 권장하지 않음)
- `--trim, -t`: 배경 전용 행과 열을 제거하여 컴팩트한 출력
- `--help, -h`: 도움말 메시지 표시

## Slack 사용 팁

- Slack 코드 블록에서 최적의 결과를 위해 너비 60-80 사용
- 출력을 복사하여 코드 블록(```)을 사용해 Slack에 붙여넣기
- Slack에 붙여넣을 때는 컬러 모드 사용 금지

## 웹 이미지 주의사항

- Slack 파일 URL은 인증이 필요하므로 직접 작동하지 않음
- 공개 이미지 호스팅 서비스 사용 (imgur, picsum.photos 등)
- 일부 웹사이트에서는 자동화된 요청을 차단할 수 있음

## 클립보드 기능 주의사항

### 입력 (--clip)
- WSL/Windows 환경에서만 작동 (PowerShell 필요)
- 사용 전에 이미지를 클립보드에 복사해야 함
- 임시 파일은 자동으로 정리됨
- 스크린샷이나 복사된 이미지 모두 지원

### 출력 (-a, --auto-copy)
- WSL/Windows 환경에서만 작동 (PowerShell 필요)
- ASCII 아트 결과를 자동으로 클립보드에 복사
- 컬러 모드 사용 시 색상 코드는 자동으로 제거됨 (호환성 향상)
- Slack에 바로 붙여넣기 가능 (코드 블록 ``` 사용)

## 출력 예시

```
.........-:=++******************************************++=:-.........
......:=+****************************************************+=:......
....:+**********************************************************+:....
..-+**************************************************************+-..
.-*************************%%%#####%%*******************************-.
.+**********************%# ...........##%***************************+.
=*********************%@.. #%%****%%%#...#%####%%%*******************=
********************%#..#%***********%#........... #%*****************
*******************% ..#*********%##...##%%****%%# ..#%***************
***************%%##...#******%%#....#%%************%#..#%*************
*************%#... ...%****##...##%*******%%*********#.. %************
***********%@..#%** ..%****.. %%******%%#... #%*******#..#************
**********#.. %****...%**** .#*****%##.. #%##...##%**+%...************
*********%. .%*****...%****..#*%%#....#%*****%%#... #%%...%***********
*********#..#******...%****.. #.. ###..##%*******%# ... .#************
*********#..%****** ..%****...#%%****%%#.. #%*******%# ..#%***********
*********#..#******...%****..#**********#.....##%******#...%**********
*********%...%*****# ..#%%%..#**********#..%%%#.. #*****%...%*********
**********%...#******%##.....#**********#..****%...******#..#*********
***********%#.. #%*******%# ..#%%****%%#...****%.. ******%..#*********
************#. ... #%*******%##..### ..# ..****%...******#..#*********
***********%...%%# ...#%%*****%#....#%%*#..****%...*****%. .%*********
************...%+**%##...##%# ..##%*****#. ****%...****% ..#**********
************#..#*******%# ...#%%******%% ..****%.. **%#..@%***********
************% ..#*********%%*******%##...##****%... ...#%*************
*************%#..#%************%%#....#%%******#...##%%***************
***************%#.. #%%****%%##...##%*********#.. %*******************
*****************%# ...........#%***********%#..#%********************
=*******************%%%####%#...#%%%****%%# ..@%**********************
-+***************************%##........... #%************************
.-*******************************%%#####%%%***************************
..-+******************************************************************
....:+****************************************************************
......:=+*************************************************************
.........-==++********************************************************
```

## 사용 예시

### 쉘 스크립트 사용 (가장 간편)
```bash
# 프로젝트 디렉토리에서 실행
./ascii-painter.sh image.jpg 70

# 다른 디렉토리에서 절대 경로로 실행 (파일 경로는 현재 디렉토리 기준)
/path/to/high-res-ascii-painter/ascii-painter.sh image.jpg 70

# 웹 이미지 URL 사용
./ascii-painter.sh -w https://picsum.photos/400/300 60

# 클립보드 이미지 사용
./ascii-painter.sh --clip 80 --trim

# 결과를 클립보드에 자동 복사
./ascii-painter.sh image.jpg 70 -a --trim

# 클립보드에서 입력받고 결과도 클립보드에 복사 (완전 자동화!)
./ascii-painter.sh --clip 80 --trim -a

# 웹 이미지와 트림 옵션
./ascii-painter.sh --web https://imgur.com/image.jpg --trim

# 모든 옵션 사용
./ascii-painter.sh image.jpg 80 --trim --color
```

### uv run 사용
```bash
# 로컬 이미지 파일 사용
uv run ascii-painter image.jpg 70

# 웹 이미지 URL 사용
uv run ascii-painter -w https://picsum.photos/400/300 60

# 클립보드 이미지 사용
uv run ascii-painter --clip 80 --trim

# 결과를 클립보드에 자동 복사
uv run ascii-painter image.jpg 70 -a --trim

# 클립보드에서 입력받고 결과도 클립보드에 복사 (완전 자동화!)
uv run ascii-painter --clip 80 --trim -a

# 웹 이미지와 트림 옵션
uv run ascii-painter --web https://imgur.com/image.jpg --trim

# 모든 옵션 사용
uv run ascii-painter image.jpg 80 --trim --color
```

### Windows 포터블 실행 파일 사용
```cmd
# 로컬 이미지 파일 사용
ascii-painter.exe image.jpg 70

# 웹 이미지 URL 사용
ascii-painter.exe -w https://picsum.photos/400/300 60

# 클립보드 이미지 사용
ascii-painter.exe --clip 80 --trim

# 결과를 클립보드에 자동 복사
ascii-painter.exe image.jpg 70 -a --trim

# 클립보드에서 입력받고 결과도 클립보드에 복사 (완전 자동화!)
ascii-painter.exe --clip 80 --trim -a

# 웹 이미지와 트림 옵션
ascii-painter.exe --web https://imgur.com/image.jpg --trim

# 모든 옵션 사용
ascii-painter.exe image.jpg 80 --trim --color
```

## Windows 포터블 실행 파일

### 빌드 방법

1. **개발 의존성 설치**:
   ```bash
   uv sync --dev
   ```

2. **실행 파일 빌드**:
   ```bash
   # Linux/WSL에서 빌드
   uv run python build_windows.py
   
   # Windows에서 배치 파일 사용
   build_windows.bat
   ```

3. **빌드 결과**:
   - `dist/windows/ascii-painter.exe` (약 23MB)
   - `dist/windows/README.md` (사용법 설명)

### 특징

- **포터블**: Python 설치 없이 실행 가능
- **단일 파일**: 모든 의존성이 포함된 하나의 .exe 파일
- **클립보드 지원**: PowerShell을 통한 완전한 클립보드 기능
- **크로스 플랫폼 빌드**: Linux/WSL에서 Windows용 실행 파일 생성 가능

### Windows에서 사용법

1. **다운로드**: `ascii-painter.exe` 파일을 원하는 폴더에 복사
2. **실행**: Command Prompt 또는 PowerShell에서 실행
3. **PATH 추가** (선택사항): 어디서든 실행하려면 PATH에 추가

```cmd
# 기본 사용법
ascii-painter.exe --help

# 완전 자동화 워크플로우 (가장 편리!)
# 1. 이미지 복사 (Ctrl+C 또는 Win+Shift+S로 스크린샷)
# 2. 실행:
ascii-painter.exe --clip 80 --trim -a
# 3. Slack에 붙여넣기 (Ctrl+V + 코드 블록 ```)
```

### 빌드 요구사항

- **Windows 10/11 환경** (크로스 컴파일 불가)
- Python 3.10+
- uv 패키지 매니저
- PyInstaller (자동 설치됨)
- 충분한 디스크 공간 (빌드 과정에서 임시 파일 생성)

### 문제 해결

**"이 앱은 PC에서 실행할 수 없습니다" 오류가 발생하는 경우:**
1. Linux/WSL에서 빌드한 실행 파일을 사용했을 가능성
2. Windows 환경에서 다시 빌드 필요
3. 자세한 해결 방법은 [WINDOWS_BUILD_GUIDE.md](WINDOWS_BUILD_GUIDE.md) 참조

**GitHub Actions를 통한 자동 빌드:**
- 이 저장소를 GitHub에 푸시하면 자동으로 Windows 실행 파일이 빌드됩니다
- Actions 탭에서 빌드된 아티팩트를 다운로드할 수 있습니다

**자동 릴리즈:**
- `v*` 태그를 푸시하면 자동으로 GitHub Release가 생성됩니다
- Windows 실행 파일이 자동으로 첨부됩니다
- 릴리즈 생성 스크립트: `./create_release.sh`

**GitHub Actions 권한 설정:**
릴리즈 생성이 실패하는 경우 GitHub 저장소 설정을 확인하세요:
1. Repository Settings → Actions → General
2. "Workflow permissions"에서 "Read and write permissions" 선택
3. "Allow GitHub Actions to create and approve pull requests" 체크

## 릴리즈 생성

### 자동 릴리즈 생성

```bash
# 릴리즈 스크립트 실행
./create_release.sh

# 또는 수동으로 태그 생성
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 릴리즈 프로세스

1. **버전 결정**: [Semantic Versioning](https://semver.org/) 사용 (예: v1.2.3)
2. **태그 생성**: `./create_release.sh` 실행 또는 수동 태그 생성
3. **자동 빌드**: GitHub Actions가 Windows 실행 파일 자동 빌드
4. **릴리즈 생성**: 실행 파일이 첨부된 GitHub Release 자동 생성

### 릴리즈에 포함되는 내용

- `ascii-painter.exe` - 단일 실행 파일 (바로 실행 가능, 약 23MB)
- `ascii-painter-windows-x64.zip` - 전체 패키지 (실행 파일 + README)
- **소스 코드** - GitHub이 자동으로 생성하는 zip/tar.gz 파일
- 자동 생성된 릴리즈 노트
- 사용법 및 주요 기능 설명
- 시스템 요구사항
