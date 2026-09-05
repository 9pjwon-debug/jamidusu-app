"""Scriptable(iOS) 용 잠금화면 위젯 스크립트를 words.json 에서 생성한다.

맥/유료 개발자 계정 없이 아이폰 잠금화면에 오늘의 단어를 띄우기 위한 경로.
Swift 앱과 데이터를 공유하되, 실행 파일은 완전히 독립적인 단일 .js 다.

설계 의도:
  JS 쪽에 난수(SplitMix64/Fisher-Yates)를 옮기면 실행 검증 없이는 오타를
  잡을 수 없다. 그래서 "섞인 순서" 자체를 여기서 미리 계산해 배열로 박고,
  JS 는 `pool[dayIndex % pool.length]` 만 하도록 만든다.

  전역 순서를 난이도로 필터링해도 "연속한 N일 안에 중복 없음" 은 그대로
  유지된다. (나머지 연산이 전단사이므로 - 아래 self-check 로 확인한다)
"""
import io
import json
import os
import sys

M64 = (1 << 64) - 1
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                       else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
WORDS_PATH = os.path.join(ROOT, "Shared", "Data", "words.json")
OUT_DIR = os.path.join(ROOT, "Scriptable")
OUT_PATH = os.path.join(OUT_DIR, "TodayChinese.js")

WORDS = json.load(io.open(WORDS_PATH, encoding="utf-8"))


# ---------------------------------------------------------------- 검증된 셔플
class SeededRandom:
    def __init__(self, seed):
        self.state = seed & M64

    def next(self):
        self.state = (self.state + 0x9E3779B97F4A7C15) & M64
        z = self.state
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & M64
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & M64
        return z ^ (z >> 31)


def seeded_shuffled(items, seed):
    result = list(items)
    rng = SeededRandom(seed)
    for i in range(len(result) - 1, 0, -1):
        j = rng.next() % (i + 1)
        result[i], result[j] = result[j], result[i]
    return result


def ordering(pool):
    """DailyWordService.ordering(for:) 과 같은 규칙."""
    fp = 0xCBF29CE484222325
    for w in pool:
        fp = ((fp ^ max(0, w["id"])) * 0x100000001B3) & M64
    return seeded_shuffled(pool, fp)


ORDERED = ordering(sorted(WORDS, key=lambda w: w["id"]))
LEVELS = sorted({w["level"] for w in WORDS})

# ------------------------------------------------- self-check: 필터 후에도 유효한가
failures = []
subsets = [LEVELS] + [[lv] for lv in LEVELS] + [
    ["HSK 1", "HSK 2", "HSK 3"],
    ["HSK 4", "HSK 5", "HSK 6"],
    ["HSK 2", "실전 회화"],
]
for subset in subsets:
    pool = [w for w in ORDERED if w["level"] in subset] or ORDERED
    n = len(pool)
    seq = [pool[((d % n) + n) % n]["id"] for d in range(-400, 1200)]
    for start in range(len(seq) - n + 1):
        window = seq[start:start + n]
        if len(set(window)) != n:
            failures.append((subset, start - 400))
            break
    if sorted({w["id"] for w in pool}) != sorted(w["id"] for w in pool):
        failures.append((subset, "pool 중복"))

if failures:
    print("self-check 실패:", failures)
    sys.exit(1)
print("self-check 통과: %d개 난이도 조합 모두 '연속 N일 중복 없음'" % len(subsets))


# ---------------------------------------------------------------- JS 생성
def js_string(value):
    return json.dumps(value, ensure_ascii=False)


rows = []
for w in ORDERED:
    rows.append("  {w:%s,p:%s,m:%s,e:%s,ep:%s,t:%s,l:%s,c:%s}," % (
        js_string(w["word"]), js_string(w["pinyin"]), js_string(w["meaning"]),
        js_string(w["example"]), js_string(w["examplePinyin"]), js_string(w["translation"]),
        js_string(w["level"]), js_string(w["category"]),
    ))

TEMPLATE = '''// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: gray; icon-glyph: language;
//
// ─────────────────────────────────────────────────────────────
//  오늘의 중국어 — 잠금화면에서 하루 한 단어
//
//  쓰는 법
//   1. 이 파일 전체를 복사해 Scriptable 에서 새 스크립트로 붙여넣는다.
//   2. 스크립트 이름을 "오늘의 중국어" 로 바꾼다.
//   3. 잠금화면 길게 누르기 → 사용자화 → 잠금화면 → 위젯 추가 → Scriptable
//   4. 위젯을 탭해서 Script 를 "오늘의 중국어" 로 지정한다.
//   5. Parameter 칸에 난이도를 적으면 그 난이도만 나온다. (비우면 기본값)
//        예) HSK 3
//        예) HSK 1, HSK 2, 실전 회화
//        예) 전체
//
//  이 파일은 자동 생성된다. 단어를 고치려면
//  ios/TodayChinese/Shared/Data/words.json 을 고치고
//  python Tools/gen_scriptable.py 를 다시 돌린다.
// ─────────────────────────────────────────────────────────────

// 위젯 Parameter 가 비어 있을 때 쓰는 난이도.
const DEFAULT_LEVELS = ["HSK 1", "HSK 2", "HSK 3"]

// 고를 수 있는 난이도: %(levels)s

// 단어 %(count)d개. 이미 섞인 순서로 고정되어 있다.
// (난이도로 걸러내도 "연속 N일 안에 중복 없음" 이 유지된다)
const WORDS = [
%(rows)s
]

// ── 오늘의 단어 ────────────────────────────────────────────────

// 2024-01-01 부터 며칠 지났는지. 로컬 자정 기준.
function dayIndex(date) {
  const start = new Date(2024, 0, 1)
  const today = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  return Math.round((today - start) / 86400000)
}

function selectedLevels() {
  const raw = (typeof args !== "undefined" && args.widgetParameter) || ""
  const trimmed = String(raw).trim()
  if (!trimmed || trimmed === "전체" || trimmed.toLowerCase() === "all") {
    return trimmed ? null : DEFAULT_LEVELS   // null = 전체
  }
  const parsed = trimmed.split(",").map(s => s.trim()).filter(Boolean)
  return parsed.length ? parsed : DEFAULT_LEVELS
}

function todayWord(date) {
  const levels = selectedLevels()
  let pool = levels ? WORDS.filter(w => levels.indexOf(w.l) !== -1) : WORDS
  if (pool.length === 0) pool = WORDS
  const n = pool.length
  const i = ((dayIndex(date) %% n) + n) %% n
  return pool[i]
}

// 원형 위젯용. 한자만 뽑고, 길면 앞 2자로 줄인다.
function compactWord(word) {
  const hanzi = (word.w.match(/[\\u4e00-\\u9fff]/g) || []).join("")
  const base = hanzi || word.w
  return base.length > 3 ? base.slice(0, 2) : base
}

function shortMeaning(word) {
  const first = word.m.split(",")[0].trim()
  return first.length > 8 ? first.slice(0, 8) : first
}

function nextMidnight() {
  const d = new Date()
  return new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1, 0, 0, 10)
}

// ── 위젯 ──────────────────────────────────────────────────────
//
// 잠금화면 위젯에는 제목도 앱 이름도 넣지 않는다.
// 한자 → 병음 → 뜻 순서만 지킨다.

function rectangularWidget(word) {
  const w = new ListWidget()
  w.setPadding(0, 0, 0, 0)

  const hanzi = w.addText(word.w)
  hanzi.font = Font.boldSystemFont(20)
  hanzi.textColor = Color.white()
  hanzi.lineLimit = 1
  hanzi.minimumScaleFactor = 0.6

  const pinyin = w.addText(word.p)
  pinyin.font = Font.systemFont(12)
  pinyin.textColor = Color.white()
  pinyin.textOpacity = 0.85
  pinyin.lineLimit = 1
  pinyin.minimumScaleFactor = 0.7

  const meaning = w.addText(word.m)
  meaning.font = Font.systemFont(11.5)
  meaning.textColor = Color.white()
  meaning.textOpacity = 0.85
  meaning.lineLimit = 1
  meaning.minimumScaleFactor = 0.7

  return w
}

function circularWidget(word) {
  const w = new ListWidget()
  w.setPadding(0, 0, 0, 0)
  w.addSpacer()

  const row = w.addStack()
  row.addSpacer()
  const text = compactWord(word)
  const label = row.addText(text)
  label.font = Font.boldSystemFont(text.length <= 1 ? 28 : text.length === 2 ? 21 : 16)
  label.textColor = Color.white()
  label.lineLimit = 1
  label.minimumScaleFactor = 0.5
  row.addSpacer()

  w.addSpacer()
  return w
}

function inlineWidget(word) {
  const w = new ListWidget()
  w.addText(word.w + " · " + shortMeaning(word))
  return w
}

function buildWidget(word, family) {
  let w
  if (family === "accessoryCircular") w = circularWidget(word)
  else if (family === "accessoryInline") w = inlineWidget(word)
  else w = rectangularWidget(word)
  w.refreshAfterDate = nextMidnight()
  return w
}

// ── 연속 학습일 (앱에서 열었을 때만 기록) ────────────────────────

function statePath() {
  const fm = FileManager.local()
  const dir = fm.joinPath(fm.documentsDirectory(), "today-chinese")
  if (!fm.fileExists(dir)) fm.createDirectory(dir, true)
  return fm.joinPath(dir, "state.json")
}

function readState() {
  try {
    const fm = FileManager.local()
    const path = statePath()
    if (!fm.fileExists(path)) return { count: 0, lastDay: null }
    return JSON.parse(fm.readString(path)) || { count: 0, lastDay: null }
  } catch (e) {
    return { count: 0, lastDay: null }
  }
}

function updateStreak() {
  const today = dayIndex(new Date())
  const state = readState()
  if (state.lastDay === today) return state.count || 1
  if (state.lastDay === today - 1) state.count = (state.count || 0) + 1
  else state.count = 1
  state.lastDay = today
  try {
    FileManager.local().writeString(statePath(), JSON.stringify(state))
  } catch (e) {
    // 저장 실패는 조용히 넘어간다. 단어 보는 데는 지장이 없다.
  }
  return state.count
}

// ── 앱에서 실행했을 때 보여줄 상세 ──────────────────────────────

function speak(text) {
  try {
    if (typeof Speech !== "undefined" && Speech.speak) {
      Speech.speak(text)
      return true
    }
  } catch (e) {
    // Scriptable 버전에 따라 없을 수 있다.
  }
  return false
}

async function showDetail(word) {
  const streak = updateStreak()
  const table = new UITable()
  table.showSeparators = false

  const hanzi = new UITableRow()
  hanzi.height = 72
  hanzi.addText(word.w).titleFont = Font.boldSystemFont(40)
  table.addRow(hanzi)

  const head = new UITableRow()
  head.height = 56
  head.addText(word.p, word.m)
  table.addRow(head)

  const meta = new UITableRow()
  meta.height = 36
  meta.addText(word.l + " · " + word.c)
  table.addRow(meta)

  const example = new UITableRow()
  example.height = 64
  example.addText(word.e, word.ep)
  table.addRow(example)

  const translation = new UITableRow()
  translation.height = 44
  translation.addText(word.t)
  table.addRow(translation)

  const listen = new UITableRow()
  listen.height = 48
  listen.dismissOnSelect = false
  listen.onSelect = () => {
    if (!speak(word.w + "。" + word.e)) {
      const alert = new Alert()
      alert.title = "발음 재생을 지원하지 않아요"
      alert.message = "Scriptable 버전에 Speech 기능이 없습니다."
      alert.addCancelAction("확인")
      alert.present()
    }
  }
  listen.addText("🔊 발음 듣기")
  table.addRow(listen)

  const foot = new UITableRow()
  foot.height = 40
  foot.addText(streak > 0 ? "🔥 " + streak + "일 연속 학습 중" : "오늘부터 시작")
  table.addRow(foot)

  await table.present()
}

// ── 진입점 ────────────────────────────────────────────────────

const word = todayWord(new Date())

if (config.runsInWidget) {
  Script.setWidget(buildWidget(word, config.widgetFamily))
} else {
  await showDetail(word)
}

Script.complete()
'''

os.makedirs(OUT_DIR, exist_ok=True)
js = TEMPLATE % {
    "rows": "\n".join(rows),
    "count": len(ORDERED),
    "levels": ", ".join(LEVELS),
}
io.open(OUT_PATH, "w", encoding="utf-8", newline="\n").write(js)

print("wrote %s (%.1f KB, 단어 %d개)" % (OUT_PATH, len(js.encode("utf-8")) / 1024, len(ORDERED)))
print("첫 7일:", ", ".join(
    "%s(%s)" % (ORDERED[d % len(ORDERED)]["word"], ORDERED[d % len(ORDERED)]["level"])
    for d in range(7)))
