"""생성된 Scriptable 스크립트 점검 (node 없이 가능한 범위).

- 템플릿 치환 잔재 확인 (%% 나 %(name)s 가 남아 있으면 실패)
- 문자열/주석/정규식을 걷어낸 뒤 괄호 균형 확인
- 임베드된 WORDS 배열을 다시 파싱해 words.json 과 일치하는지 확인
- Scriptable 진입점(config.runsInWidget / Script.setWidget) 존재 확인

실제 실행 검증은 아이폰의 Scriptable 에서만 가능하다.
"""
import io
import json
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                       else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
JS_PATH = os.path.join(ROOT, "Scriptable", "TodayChinese.js")
WORDS_PATH = os.path.join(ROOT, "Shared", "Data", "words.json")

src = io.open(JS_PATH, encoding="utf-8").read()
errors = []

# 1) 템플릿 치환 잔재
for bad in ("%(rows)s", "%(count)d", "%(levels)s"):
    if bad in src:
        errors.append("치환되지 않은 placeholder: %s" % bad)
for m in re.finditer(r"%%", src):
    errors.append("이스케이프가 안 풀린 '%%' at offset %d" % m.start())

# 2) 한자 판별 정규식이 깨지지 않았는지
#    JS 파일에는 이스케이프 문자열 그대로 들어가야 한다: /[一-鿿]/g
CJK_PATTERN = "[" + chr(92) + "u4e00-" + chr(92) + "u9fff]"
if CJK_PATTERN not in src:
    errors.append("한자 판별 정규식이 깨졌다 (%s 를 찾지 못함)" % CJK_PATTERN)

# 3) 문자열/주석/정규식 제거 후 괄호 균형
def strip_literals(text):
    out = []
    i, n = 0, len(text)
    prev_significant = ""
    while i < n:
        c = text[i]
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j == -1 else j
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j == -1 else j + 2
            continue
        if c in "\"'`":
            quote = c
            i += 1
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == quote:
                    i += 1
                    break
                i += 1
            prev_significant = "x"
            continue
        # 정규식 리터럴: 앞에 피연산자가 없을 때만 (여기서는 = 나 ( 뒤)
        if c == "/" and prev_significant in "=(,:[!&|":
            i += 1
            in_class = False
            while i < n:
                if text[i] == "\\":
                    i += 2
                    continue
                if text[i] == "[":
                    in_class = True
                elif text[i] == "]":
                    in_class = False
                elif text[i] == "/" and not in_class:
                    i += 1
                    break
                elif text[i] == "\n":
                    break
                i += 1
            prev_significant = "x"
            continue
        out.append(c)
        if not c.isspace():
            prev_significant = c
        i += 1
    return "".join(out)


code = strip_literals(src)
stack = []
pairs = {")": "(", "]": "[", "}": "{"}
line = 1
for ch in code:
    if ch == "\n":
        line += 1
    elif ch in "([{":
        stack.append((ch, line))
    elif ch in ")]}":
        if not stack or stack[-1][0] != pairs[ch]:
            errors.append("line %d: 짝이 맞지 않는 '%s'" % (line, ch))
            break
        stack.pop()
else:
    if stack:
        errors.append("닫히지 않은 '%s' (line %d)" % (stack[-1][0], stack[-1][1]))

# 4) 진입점
for needed in ("config.runsInWidget", "Script.setWidget", "Script.complete()",
               "refreshAfterDate", "args.widgetParameter"):
    if needed not in src:
        errors.append("빠진 호출: %s" % needed)

# 5) 임베드된 WORDS 를 다시 파싱해 원본과 대조
m = re.search(r"const WORDS = \[\n(.*?)\n\]\n", src, re.S)
if not m:
    errors.append("WORDS 배열을 찾지 못함")
    embedded = []
else:
    body = m.group(1)
    # {w:"..",p:".."} 형태의 축약 키를 JSON 으로 되돌린다
    jsonish = re.sub(r"(\{|,)\s*([a-z]+):", lambda mm: '%s"%s":' % (mm.group(1), mm.group(2)), body)
    jsonish = "[" + jsonish.rstrip().rstrip(",") + "]"
    try:
        embedded = json.loads(jsonish)
    except json.JSONDecodeError as exc:
        errors.append("WORDS 배열 파싱 실패: %s" % exc)
        embedded = []

original = json.load(io.open(WORDS_PATH, encoding="utf-8"))
if embedded:
    if len(embedded) != len(original):
        errors.append("단어 개수 불일치: js %d vs json %d" % (len(embedded), len(original)))

    by_word = {w["word"]: w for w in original}
    for row in embedded:
        src_word = by_word.get(row["w"])
        if src_word is None:
            errors.append("words.json 에 없는 단어: %s" % row["w"])
            continue
        for js_key, json_key in (("p", "pinyin"), ("m", "meaning"), ("e", "example"),
                                 ("ep", "examplePinyin"), ("t", "translation"),
                                 ("l", "level"), ("c", "category")):
            if row[js_key] != src_word[json_key]:
                errors.append("%s 의 %s 불일치" % (row["w"], json_key))

    if len({r["w"] for r in embedded}) != len(embedded):
        errors.append("임베드된 배열에 중복 단어")

    # 섞였는지 (id 순 그대로면 셔플이 안 된 것)
    if [r["w"] for r in embedded] == [w["word"] for w in sorted(original, key=lambda x: x["id"])]:
        errors.append("순서가 섞이지 않았다")

print("파일 크기: %.1f KB" % (len(src.encode("utf-8")) / 1024))
print("임베드된 단어: %d개" % len(embedded))
print("난이도:", ", ".join(sorted({r["l"] for r in embedded})) if embedded else "-")

if errors:
    print("\n오류 %d건:" % len(errors))
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nOK: Scriptable 스크립트 검사 통과")
