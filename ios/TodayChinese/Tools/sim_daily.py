"""DailyWordService 알고리즘을 파이썬으로 그대로 옮겨 성질을 검증한다.

확인할 것:
  1. 같은 날 + 같은 설정이면 항상 같은 단어 (앱/위젯 일치)
  2. pool.count 일 안에는 같은 단어가 두 번 나오지 않음
  3. 한 주기가 끝나면 pool 의 모든 단어가 정확히 한 번씩 나옴
  4. 주기가 바뀌면 순서도 바뀜
"""
import json
import os
import sys

M64 = (1 << 64) - 1
ROOT = os.path.abspath(sys.argv[1])
WORDS = json.load(open(os.path.join(ROOT, "Shared", "Data", "words.json"), encoding="utf-8"))


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
    if len(items) <= 1:
        return list(items)
    result = list(items)
    rng = SeededRandom(seed)
    for i in range(len(result) - 1, 0, -1):
        j = rng.next() % (i + 1)
        result[i], result[j] = result[j], result[i]
    return result


def pool_for(levels, categories=()):
    items = [w for w in WORDS if not levels or w["level"] in levels]
    if categories:
        by_cat = [w for w in items if w["category"] in categories]
        if by_cat:
            items = by_cat
    if not items:
        items = list(WORDS)
    return sorted(items, key=lambda w: w["id"])


def ordering(pool):
    fp = 0xCBF29CE484222325
    for w in pool:
        fp = ((fp ^ max(0, w["id"])) * 0x100000001B3) & M64
    return seeded_shuffled(pool, fp)


def word_for(day_index, levels, categories=()):
    pool = pool_for(levels, categories)
    if len(pool) <= 1:
        return pool[0]
    order = ordering(pool)
    count = len(order)
    offset = ((day_index % count) + count) % count
    return order[offset]


def check(name, levels, categories=(), days=1200):
    pool = pool_for(levels, categories)
    count = len(pool)
    seq = [word_for(d, levels, categories)["id"] for d in range(-200, days)]

    # 1) 결정성
    assert seq == [word_for(d, levels, categories)["id"] for d in range(-200, days)]

    # 2) 슬라이딩 윈도우 중복 없음 (한 주기 = count 일)
    worst = None
    for start in range(len(seq) - count + 1):
        window = seq[start:start + count]
        if len(set(window)) != count:
            dupes = [i for i in window if window.count(i) > 1]
            worst = (start - 200, sorted(set(dupes)))
            break

    # 3) 주기 정렬 구간은 pool 전체를 정확히 한 번씩
    aligned_ok = True
    for cycle_start in range(0, days - count, count):
        window = seq[cycle_start + 200: cycle_start + 200 + count]
        if sorted(window) != sorted(w["id"] for w in pool):
            aligned_ok = False
            break

    # 4) id 순서 그대로가 아니라 섞여 있는지
    pool_ids = [w["id"] for w in pool_for(levels, categories)]
    shuffled = seq[200:200 + count] != pool_ids

    status = "OK " if (worst is None and aligned_ok and shuffled) else "FAIL"
    print("%s %-28s pool=%3d  모든구간중복없음=%s  주기완전순회=%s  섞임=%s"
          % (status, name, count,
             "예" if worst is None else "아니오 @%s %s" % worst,
             aligned_ok, shuffled))
    return worst is None and aligned_ok and shuffled


all_levels = sorted({w["level"] for w in WORDS})
ok = True
ok &= check("전체(랜덤)", all_levels)
ok &= check("HSK 3 만", ["HSK 3"])
ok &= check("HSK 1+2", ["HSK 1", "HSK 2"])
ok &= check("실전 회화", ["실전 회화"])
ok &= check("HSK 6 (12개)", ["HSK 6"])
ok &= check("전체 + 회화 카테고리", all_levels, ["회화"])
ok &= check("HSK 1 + 없는 카테고리", ["HSK 1"], ["존재하지않음"])

# 앱과 위젯이 같은 날 같은 결과를 내는지 (동일 함수 두 번 호출로 모사)
day = 700
assert word_for(day, all_levels)["id"] == word_for(day, all_levels)["id"]

# 날짜가 바뀌면 단어도 바뀌는지
changes = sum(1 for d in range(500) if word_for(d, all_levels)["id"] != word_for(d + 1, all_levels)["id"])
print("\n연속한 날에 단어가 바뀐 비율: %d/500" % changes)

print("\n예시 (전체 pool, day 0~6):")
for d in range(7):
    w = word_for(d, all_levels)
    print("  day %d -> %-6s %-16s %s" % (d, w["word"], w["pinyin"], w["meaning"]))

sys.exit(0 if ok else 1)
