# 오늘의 중국어

> 잠금화면에서 하루 한 단어.

SwiftUI + WidgetKit 로 만든 아이폰 앱. 서버·로그인·결제·광고 없음, 로컬 JSON 단어 데이터만 사용한다.

가장 중요한 제품은 앱이 아니라 **잠금화면 위젯**이다. 위젯에는 앱 이름이나
"Today's Chinese", "오늘의 중국어", "TODAY" 같은 제목을 넣지 않는다.
오늘의 단어 자체가 주인공이고, 정보 우선순위는 항상 **한자 → 병음 → 뜻** 순서다.

```
┌─────────────────────┐
│ 坚持                │
│ jiānchí             │
│ 꾸준히 하다          │
└─────────────────────┘
```

---

## 두 가지 버전이 있습니다

| | 네이티브 앱 (`TodayChinese.xcodeproj`) | Scriptable 스크립트 (`Scriptable/TodayChinese.js`) |
|---|---|---|
| 필요한 것 | macOS + Xcode, 기기 설치엔 유료 개발자 계정 | 아이폰 + 무료 Scriptable 앱 |
| 잠금화면 위젯 3종 | ✅ | ✅ |
| 앱 UI | 탭바, 온보딩, 내 단어장, 설정 | 위젯 탭 시 상세 화면 |
| 난이도 선택 | 설정 화면에서 자유 조합 | 위젯 Parameter 칸에 입력 |
| 설치 유효기간 | TestFlight 90일 / 정식 배포 무제한 | 무제한 |
| 앱스토어 배포 | 가능 | 불가 |

단어 데이터(`Shared/Data/words.json`)와 오늘의 단어 규칙은 두 버전이 공유합니다.
맥이 없다면 **Scriptable 쪽부터** 쓰면 됩니다.

## Scriptable 로 지금 바로 쓰기 (맥 불필요)

1. 앱스토어에서 **Scriptable** 설치 (무료)
2. 아이폰 사파리로 아래 주소를 열고 **전체 선택 → 복사**

   `https://raw.githubusercontent.com/9pjwon-debug/jamidusu-app/main/ios/TodayChinese/Scriptable/TodayChinese.js`

3. Scriptable → `+` → 붙여넣기 → 스크립트 이름을 **오늘의 중국어** 로 변경
4. 잠금화면 길게 누르기 → **사용자화 → 잠금화면** → 시계 아래 위젯 슬롯 탭
5. 목록에서 **Scriptable** 선택 → 추가된 위젯을 탭해서 Script 를 `오늘의 중국어` 로 지정
6. (선택) **Parameter** 칸에 난이도를 적으면 그 난이도만 나옵니다

   | 입력 | 결과 |
   |---|---|
   | (비움) | HSK 1~3 |
   | `HSK 3` | HSK 3 만 |
   | `HSK 1, HSK 2, 실전 회화` | 세 가지 섞어서 |
   | `전체` | 122개 전부 |

Rectangular / Circular / Inline 세 종류 모두 같은 스크립트 하나로 동작합니다.
위젯을 탭하면 Scriptable 이 열리면서 예문·번역·발음 듣기·연속 학습일이 나옵니다.

알아둘 점:

- 위젯 갱신 시점은 iOS 가 정합니다. 자정에 정확히 바뀌지 않고 몇 분~몇십 분 늦을 수 있습니다
- 발음 듣기는 Scriptable 의 `Speech` API 를 쓰는데, 버전에 따라 없을 수 있어 그때는 안내만 뜹니다
- 이 파일은 **자동 생성물**입니다. 단어를 고치려면 `words.json` 을 고치고 `python Tools/gen_scriptable.py` 를 다시 돌리세요

---

## 열기 전에 (필수 설정 2가지)

Xcode 에서 `TodayChinese.xcodeproj` 를 연 뒤:

1. **Signing Team 선택**
   `TodayChinese` 와 `TodayChineseWidgetExtension` 두 타깃 모두
   Signing & Capabilities → Team 을 본인 계정으로 지정한다.
   (시뮬레이터만 돌릴 거면 이 단계는 건너뛰어도 된다.)

2. **App Group 확인**
   두 타깃 모두 App Groups 에 `group.com.jamidusu.todaychinese` 가 체크되어 있어야
   앱에서 고른 난이도가 위젯에 그대로 반영된다.
   계정에 이 그룹이 없다면 Xcode 에서 `+` 로 추가하면 자동 등록된다.

   Bundle ID 를 본인 것으로 바꾸려면 세 곳을 함께 바꿔야 한다:
   - 두 타깃의 `PRODUCT_BUNDLE_IDENTIFIER`
   - `Shared/AppGroup.swift` 의 `AppGroup.identifier`
   - `TodayChinese/TodayChinese.entitlements`, `TodayChineseWidget/TodayChineseWidget.entitlements`

   App Group 이 연결되지 않아도 앱은 죽지 않는다.
   `UserDefaults.standard` 로 폴백하고, 설정 화면 하단에 안내 문구가 뜬다.

빌드/실행:

```bash
xcodebuild -project TodayChinese.xcodeproj -scheme TodayChinese -destination 'platform=iOS Simulator,name=iPhone 16' build
```

## 잠금화면 위젯 올리기

1. 앱을 한 번 실행해 온보딩을 마친다. (난이도를 골라야 위젯이 쓸 설정이 생긴다)
2. 잠금화면을 길게 누른 뒤 **사용자화 → 잠금화면**
3. 시계 아래 영역에서 위젯 추가 → `오늘의 중국어` 선택
4. 원하는 모양을 고른다.

| 위젯 | 보이는 것 | 비고 |
|---|---|---|
| Rectangular | `坚持` / `jiānchí` / `꾸준히 하다` (3줄, 좁으면 2줄) | 가장 중요한 형태 |
| Circular | `坚持` 한자만 | 뜻·병음을 억지로 넣지 않음 |
| Inline | `坚持 · 꾸준히 하다` | 시계 아래 한 줄 |

위젯을 탭하면 `todaychinese://detail` 로 앱이 열리고 오늘의 단어 상세가 뜬다.

> 갤러리(위젯 추가 화면)에 보이는 "오늘의 중국어"는 WidgetKit 이 요구하는
> `configurationDisplayName` 이다. 실제 잠금화면에 렌더링되는 위젯에는 들어가지 않는다.

## 폴더 구조

```
Shared/                      앱 · 위젯이 함께 쓰는 코드 (두 타깃 모두에 포함)
  AppGroup.swift             App Group ID, URL scheme, UserDefaults 키
  Models/ChineseWord.swift   단어 모델 + 위젯용 축약 헬퍼
  Models/StudyLevel.swift    HSK 1~6, 실전 회화
  Data/words.json            단어 122개
  Data/WordRepository.swift  번들 JSON 로딩 + 난이도/카테고리 필터
  Services/DailyWordService  오늘의 단어 선택 (순수 함수)
  Services/AppSettingsStore  App Group 설정 읽기/쓰기
  Services/SavedWordsStore   내 단어장 + 최근 본 단어
  Services/StreakService     연속 학습일
  Services/SeededRandom      결정적 난수 (앱·위젯이 같은 결과를 내기 위해)

TodayChinese/                앱 타깃
  TodayChineseApp.swift      진입점, 딥링크, scenePhase 처리
  AppModel.swift             전역 상태, 설정 변경 시 위젯 타임라인 갱신
  Theme.swift                아이보리 배경 + 잉크 텍스트 팔레트
  Views/                     온보딩 / 오늘 / 상세 / 내 단어장 / 설정
  Services/SpeechService     AVSpeechSynthesizer (zh-CN)
  Services/NotificationService  하루 한 번 알림

TodayChineseWidget/          위젯 익스텐션 타깃
  TodayChineseWidgetBundle   @main
  TodayChineseWidget         StaticConfiguration + 지원 패밀리
  TodayChineseWidgetProvider TimelineProvider (7일치 미리 생성)
  WidgetViews                Rectangular / Circular / Inline

Scriptable/TodayChinese.js   맥 없이 쓰는 단일 파일 버전 (words.json 에서 자동 생성)
Tools/                       macOS 없이 돌리는 점검 스크립트 (아래 참고)
```

`Shared/` 안의 파일은 **두 타깃 모두**에 들어간다. `words.json` 도 마찬가지라
위젯 익스텐션 번들 안에 자기 몫의 사본이 들어가고, 양쪽 다 `Bundle.main` 으로 읽는다.

## 오늘의 단어 규칙

`DailyWordService` 는 **(날짜 + 설정)** 만으로 단어를 정하는 순수 함수다.
앱과 위젯이 서로 통신하지 않고 각자 계산해도 같은 결과가 나온다.

1. 난이도·카테고리로 거른 목록을 id 순으로 정렬한다.
2. 목록 구성으로 지문을 만들어 **한 번만** 결정적으로 섞는다. (`SeededRandom`)
3. `2024-01-01` 부터 며칠 지났는지를 목록 길이로 나눈 나머지 위치의 단어를 쓴다.

이 구조 덕분에 **연속한 어떤 N일(N = 목록 길이)을 잘라 봐도 같은 단어가 두 번
나오지 않는다.** 나머지 연산이 전단사라서 수학적으로 보장된다.

처음에는 "주기마다 순서를 다시 섞는" 방식으로 만들었는데,
`Tools/sim_daily.py` 시뮬레이션에서 주기 경계에 같은 단어가 이틀 연속 나오는
사례가 잡혀서 지금 방식으로 바꿨다. 대신 순서는 N일마다 그대로 반복된다
(전체 122단어 기준 약 4개월). 순서를 매번 섞는 것과 "가까이 반복되지 않는 것"은
동시에 만족시킬 수 없어서 후자를 택했다.

위젯 타임라인은 한 번에 7일치를 만들고, 마지막 날 다음 자정에 갱신을 요청한다.
앱에서 난이도를 바꾸면 `WidgetCenter.reloadTimelines` 로 즉시 다시 계산한다.

## 점검 스크립트

macOS 가 없는 환경에서 만들어진 프로젝트라 xcodebuild 검증 대신
아래 스크립트로 구조를 확인했다. Python 3 만 있으면 어디서든 돌아간다.

```bash
python Tools/validate_project.py .   # pbxproj ID/경로 정합성
python Tools/check_swift.py .        # 괄호 균형, 타입 중복 선언
python Tools/sim_daily.py .          # 오늘의 단어 알고리즘 성질 검증
python Tools/check_scriptable.py     # Scriptable .js 구조 + 데이터 대조
python Tools/gen_project.py          # 파일 추가 후 pbxproj 재생성
python Tools/gen_scriptable.py       # words.json 수정 후 .js 재생성
```

**소스 파일을 새로 추가하면** `Tools/gen_project.py` 상단의 목록에 한 줄 넣고
다시 실행하면 두 타깃의 Target Membership 까지 맞춰서 프로젝트를 다시 만든다.
Xcode 에서 직접 추가해도 되지만, 그때는 `Shared/` 파일의 Target Membership 에
위젯 타깃도 체크했는지 꼭 확인해야 한다.

`project.yml` 은 XcodeGen 용 대체 스펙이다. 프로젝트 파일이 꼬였을 때
`xcodegen generate` 로 다시 만들 수 있다.

## MVP 범위

들어간 것: 온보딩, 오늘의 단어, 예문, 발음(zh-CN TTS), 저장·단어장, 난이도·카테고리
설정, 연속 학습일, 하루 한 번 알림, 잠금화면 위젯 3종, App Group 공유, 딥링크.

의도적으로 뺀 것: 서버, 로그인, 회원가입, 결제, 광고, 소셜, AI API, 외부 DB, 복잡한 통계.
