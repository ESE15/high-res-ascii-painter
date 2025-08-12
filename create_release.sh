#!/bin/bash

# ASCII Painter 릴리즈 생성 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 함수들
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  ASCII Painter Release Tool${NC}"
    echo -e "${BLUE}================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# 현재 버전 확인
get_current_version() {
    if [ -f "pyproject.toml" ]; then
        grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'
    else
        echo "0.1.0"
    fi
}

# 버전 유효성 검사
validate_version() {
    local version=$1
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_error "Invalid version format. Use semantic versioning (x.y.z)"
        return 1
    fi
    return 0
}

# 메인 함수
main() {
    print_header
    
    # Git 상태 확인
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "This is not a git repository"
        exit 1
    fi
    
    # 변경사항 확인
    if [ -n "$(git status --porcelain)" ]; then
        print_warning "You have uncommitted changes:"
        git status --short
        echo
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Aborted"
            exit 1
        fi
    fi
    
    # 현재 버전 표시
    current_version=$(get_current_version)
    echo -e "Current version: ${YELLOW}v${current_version}${NC}"
    echo
    
    # 새 버전 입력
    read -p "Enter new version (x.y.z): " new_version
    
    if [ -z "$new_version" ]; then
        print_error "Version cannot be empty"
        exit 1
    fi
    
    if ! validate_version "$new_version"; then
        exit 1
    fi
    
    # 태그 중복 확인
    if git tag | grep -q "^v${new_version}$"; then
        print_error "Tag v${new_version} already exists"
        exit 1
    fi
    
    echo
    echo -e "Creating release: ${GREEN}v${new_version}${NC}"
    echo
    
    # 확인
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborted"
        exit 1
    fi
    
    # pyproject.toml 버전 업데이트
    if [ -f "pyproject.toml" ]; then
        print_success "Updating pyproject.toml version..."
        sed -i.bak "s/^version = .*/version = \"${new_version}\"/" pyproject.toml
        rm pyproject.toml.bak 2>/dev/null || true
        
        # 변경사항 커밋
        git add pyproject.toml
        git commit -m "chore: bump version to v${new_version}" || true
    fi
    
    # 태그 생성
    print_success "Creating tag v${new_version}..."
    git tag -a "v${new_version}" -m "Release v${new_version}"
    
    # 태그 푸시
    print_success "Pushing tag to remote..."
    git push origin "v${new_version}"
    
    # main 브랜치도 푸시 (버전 업데이트 커밋)
    if [ -f "pyproject.toml" ]; then
        git push origin main
    fi
    
    echo
    print_success "Release v${new_version} created successfully!"
    echo
    echo -e "${BLUE}What happens next:${NC}"
    echo "1. GitHub Actions will automatically build Windows executable"
    echo "2. A new release will be created with the executable attached"
    echo "3. Check the Actions tab for build progress"
    echo
    echo -e "${YELLOW}Release URL:${NC} https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/releases/tag/v${new_version}"
}

# 스크립트 실행
main "$@"
