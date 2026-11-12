# 인스타 자동 업로드 (@_memepigeon)

세컨드 브레인 `_inbox/올릴것` 폴더의 밈 묶음을 **정해진 시간에 인스타그램에 자동으로 올려주는** 저장소예요. (Claude와 함께 만듦, 2026.11)

## 어떻게 돌아가나요?
1. `images/` 폴더에 사진, `schedule.json`에 올릴 시간·캡션이 들어 있어요.
2. GitHub Actions가 15분마다 확인해서, 시간이 된 게시물을 인스타에 올려요. (몇 분~30분 정도 늦을 수 있어요)
3. 모든 게시물 맨 뒷장에 팔로우 안내 사진(`images/end_card.jpg`)이 자동으로 붙어요. 빼고 싶으면 이 파일만 지우면 돼요.
4. 올린 게시물은 `posted.json`에 기록돼서 두 번 올라가지 않아요.
5. 매달 1일·15일에 토큰이 살아 있는지 확인해요. 만료됐으면 빨간 ❌ + GitHub 메일이 와요.

## 토큰이 만료됐을 때
1. Meta 개발자 앱 → Instagram API → API setup with Unified login → 2. 액세스 토큰 생성 → _memepigeon 옆 **토큰 생성** (EAA로 시작하는 게 정상)
2. GitHub → Settings → Secrets and variables → Actions → `IG_TOKEN` ✏️ → 붙여넣고 Update

## 새 게시물 추가하는 법
1. 사진을 `images/`에 올리기 (JPG, 1080x1350 권장, 게시물당 최대 9장 — 마지막 1장은 팔로우 안내 사진 자리)
2. `schedule.json`에 항목 추가 (id는 격치지 않게, 시간은 `2026-11-23T21:00:00+09:00` 형식)

## 파일 설명
| 파일 | 내용 |
|---|---|
| `images/` | 올릴 사진 (`b02_1.jpg` = 묶음02의 1번째 사진, `end_card.jpg` = 맨 뒷장 팔로우 안내) |
| `schedule.json` | 게시물별 날짜·시간·캡션 |
| `posted.json` | 이미 올린 묶음 기록 |
| `post.py` | 실제로 인스타에 올리는 프로그램 |
| `.github/workflows/` | 자동 실행 설정 |

## 문제가 생기면
- 상단 **Actions** 탭에서 빨간 ❌ 표시가 있는지 확인하세요.
- 비밀값 `IG_TOKEN`(Settings → Secrets and variables → Actions)은 절대 공개하지 마세요.
