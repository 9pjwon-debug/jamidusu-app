"""project.pbxproj 정합성 검사 (macOS 없이 할 수 있는 범위)."""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1])
PBX = os.path.join(ROOT, "TodayChinese.xcodeproj", "project.pbxproj")
text = open(PBX, encoding="utf-8").read()

errors = []
warnings = []

# 1) 중괄호 균형
if text.count("{") != text.count("}"):
    errors.append("중괄호 불균형: { %d개, } %d개" % (text.count("{"), text.count("}")))
if text.count("(") != text.count(")"):
    errors.append("괄호 불균형: ( %d개, ) %d개" % (text.count("("), text.count(")")))

# 2) 객체 정의 수집
defined = {}
for m in re.finditer(r"^\t\t([0-9A-F]{24}) /\* (.*?) \*/ = \{", text, re.M):
    oid, label = m.group(1), m.group(2)
    if oid in defined:
        errors.append("ID 중복 정의: %s (%s / %s)" % (oid, defined[oid], label))
    defined[oid] = label

# 3) 참조된 모든 ID 가 정의돼 있는지
referenced = set(re.findall(r"[0-9A-F]{24}", text))
missing = sorted(referenced - set(defined))
for oid in missing:
    errors.append("정의되지 않은 ID 참조: %s" % oid)

unused = sorted(set(defined) - (referenced - set()))
# 정의부 자체가 참조에 포함되므로 unused 계산은 생략

# 4) isa 값 확인
isas = set(re.findall(r"isa = (\w+);", text))
required = {
    "PBXBuildFile", "PBXFileReference", "PBXGroup", "PBXNativeTarget", "PBXProject",
    "PBXSourcesBuildPhase", "PBXResourcesBuildPhase", "PBXFrameworksBuildPhase",
    "PBXCopyFilesBuildPhase", "PBXTargetDependency", "PBXContainerItemProxy",
    "XCBuildConfiguration", "XCConfigurationList",
}
for r in sorted(required - isas):
    errors.append("빠진 섹션: %s" % r)

# 5) rootObject 존재
m = re.search(r"rootObject = ([0-9A-F]{24})", text)
if not m or m.group(1) not in defined:
    errors.append("rootObject 가 정의되지 않음")

# 6) 파일 경로가 실제로 존재하는지 (그룹 경로를 따라 조립)
group_paths = {}
# 라벨에 .*? + DOTALL 을 쓰면 앞 섹션의 ID 와 잘못 짝지어지므로 줄 안에서만 찾는다.
for m in re.finditer(r"^\t\t([0-9A-F]{24}) /\* [^\n]*? \*/ = \{\n\t\t\tisa = PBXGroup;(.*?)\n\t\t\};",
                     text, re.M | re.S):
    gid, body = m.group(1), m.group(2)
    pm = re.search(r"\n\t\t\tpath = (.*?);", body)
    children = re.findall(r"\n\t\t\t\t([0-9A-F]{24})", body)
    group_paths[gid] = (pm.group(1).strip('"') if pm else "", children)

file_paths = {}
for m in re.finditer(r'^\t\t([0-9A-F]{24}) /\* .*? \*/ = \{isa = PBXFileReference;'
                     r'.*?path = (.*?); sourceTree = "<group>"', text, re.M):
    file_paths[m.group(1)] = m.group(2).strip('"')

# mainGroup 부터 재귀
main = re.search(r"mainGroup = ([0-9A-F]{24});", text).group(1)
resolved = {}


def walk(gid, prefix):
    path, children = group_paths.get(gid, ("", []))
    base = os.path.join(prefix, path) if path else prefix
    for child in children:
        if child in group_paths:
            walk(child, base)
        elif child in file_paths:
            resolved[child] = os.path.normpath(os.path.join(base, file_paths[child]))


walk(main, "")
for oid, rel in sorted(resolved.items()):
    if not os.path.exists(os.path.join(ROOT, rel)):
        errors.append("파일 없음: %s" % rel)

# 7) 디스크의 소스 파일이 전부 프로젝트에 들어갔는지
on_disk = set()
for base in ("Shared", "TodayChinese", "TodayChineseWidget"):
    for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, base)):
        dirnames[:] = [d for d in dirnames if not d.endswith(".xcassets")]
        for name in filenames:
            if name.endswith((".swift", ".json")):
                on_disk.add(os.path.relpath(os.path.join(dirpath, name), ROOT).replace("\\", "/"))
in_project = {p.replace("\\", "/") for p in resolved.values()}
for p in sorted(on_disk - in_project):
    errors.append("프로젝트에 빠진 파일: %s" % p)

# 8) 빌드 페이즈 중복 검사
for phase in ("PBXSourcesBuildPhase", "PBXResourcesBuildPhase"):
    for m in re.finditer(r"= \{\n\t\t\tisa = " + phase + r";(.*?)\n\t\t\};", text, re.S):
        ids = re.findall(r"\n\t\t\t\t([0-9A-F]{24})", m.group(1))
        dupes = {i for i in ids if ids.count(i) > 1}
        for d in dupes:
            errors.append("%s 에 중복 빌드파일: %s" % (phase, d))

# 9) 각 PBXBuildFile 의 fileRef 가 PBXFileReference 인지
for m in re.finditer(r"isa = PBXBuildFile; fileRef = ([0-9A-F]{24})", text):
    if m.group(1) not in file_paths and m.group(1) not in defined:
        errors.append("PBXBuildFile 의 fileRef 가 없음: %s" % m.group(1))

# 10) 타깃별 소스 개수 요약
print("objects defined:", len(defined))
for m in re.finditer(r"^\t\t([0-9A-F]{24}) /\* Sources \*/ = \{\n\t\t\tisa = PBXSourcesBuildPhase;"
                     r"(.*?)\n\t\t\};", text, re.M | re.S):
    print("  Sources phase %s -> %d files" % (m.group(1)[:8], len(re.findall(r"\n\t\t\t\t[0-9A-F]{24}", m.group(2)))))

if warnings:
    print("\n경고:")
    for x in warnings:
        print("  -", x)

if errors:
    print("\n오류 %d건:" % len(errors))
    for x in errors:
        print("  -", x)
    sys.exit(1)

print("\nOK: pbxproj 구조 검사 통과")
