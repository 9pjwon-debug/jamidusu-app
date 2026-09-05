"""Swift 소스 정적 점검 (macOS 없이 가능한 범위).

- 문자열/주석을 제거한 뒤 괄호 균형 확인
- 최상위 타입 이름 중복 선언 확인
- 파일별 import 목록 요약
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1])
errors = []
decls = {}


def strip_literals(src):
    out = []
    i = 0
    n = len(src)
    while i < n:
        c = src[i]
        if c == '"':
            # 멀티라인 문자열
            if src.startswith('"""', i):
                j = src.find('"""', i + 3)
                i = n if j == -1 else j + 3
                continue
            i += 1
            while i < n:
                if src[i] == '\\':
                    i += 2
                    continue
                if src[i] == '"':
                    i += 1
                    break
                if src[i] == '\n':      # 닫히지 않은 문자열
                    break
                i += 1
            continue
        if src.startswith('//', i):
            j = src.find('\n', i)
            i = n if j == -1 else j
            continue
        if src.startswith('/*', i):
            depth = 1
            i += 2
            while i < n and depth:
                if src.startswith('/*', i):
                    depth += 1
                    i += 2
                elif src.startswith('*/', i):
                    depth -= 1
                    i += 2
                else:
                    i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


swift_files = []
for base in ("Shared", "TodayChinese", "TodayChineseWidget"):
    for dirpath, _, names in os.walk(os.path.join(ROOT, base)):
        for name in sorted(names):
            if name.endswith(".swift"):
                swift_files.append(os.path.join(dirpath, name))

for path in sorted(swift_files):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    src = open(path, encoding="utf-8").read()
    code = strip_literals(src)

    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}
    line = 1
    for ch in code:
        if ch == '\n':
            line += 1
        elif ch in '([{':
            stack.append((ch, line))
        elif ch in ')]}':
            if not stack or stack[-1][0] != pairs[ch]:
                errors.append("%s:%d 짝이 맞지 않는 '%s'" % (rel, line, ch))
                break
            stack.pop()
    else:
        if stack:
            errors.append("%s 닫히지 않은 '%s' (line %d)" % (rel, stack[-1][0], stack[-1][1]))

    # 홀수 개의 큰따옴표 = 문자열이 안 닫힘
    if src.count('"') % 2 != 0 and '"""' not in src:
        errors.append("%s 따옴표 개수가 홀수" % rel)

    for m in re.finditer(r"^(?:@\w+\s+)*(?:public |internal |private |fileprivate |final |)*"
                         r"(struct|class|enum|protocol|actor)\s+(\w+)", code, re.M):
        name = m.group(2)
        decls.setdefault(name, []).append(rel)

    imports = re.findall(r"^import (\w+)", src, re.M)
    print("%-52s %s" % (rel, ", ".join(imports)))

print()
for name, files in sorted(decls.items()):
    if len(files) > 1:
        errors.append("타입 이름 중복 선언: %s -> %s" % (name, files))

print("선언된 최상위 타입 %d개" % len(decls))

if errors:
    print("\n오류 %d건:" % len(errors))
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("\nOK: 괄호 균형 / 중복 선언 검사 통과")
