"""TodayChinese.xcodeproj/project.pbxproj 생성기.

손으로 pbxproj 를 쓰면 ID 충돌/누락이 나기 쉬워서 스크립트로 만든다.
파일을 추가하면 아래 목록만 고치고 다시 실행하면 된다.
"""
import hashlib
import os

import sys

# 기본값은 이 스크립트의 상위 폴더(프로젝트 루트). 인자로 덮어쓸 수 있다.
ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                       else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

APP_NAME = "TodayChinese"
WIDGET_NAME = "TodayChineseWidgetExtension"
APP_BUNDLE_ID = "com.jamidusu.todaychinese"
WIDGET_BUNDLE_ID = "com.jamidusu.todaychinese.widget"
DEPLOYMENT_TARGET = "17.0"


def oid(key: str) -> str:
    return hashlib.md5(key.encode("utf-8")).hexdigest()[:24].upper()


FILE_TYPES = {
    ".swift": "sourcecode.swift",
    ".json": "text.json",
    ".plist": "text.plist.xml",
    ".entitlements": "text.plist.entitlements",
    ".xcassets": "folder.assetcatalog",
}


class Ref:
    def __init__(self, path, group=""):
        self.path = path                      # 그룹 기준 상대 경로 (pbxproj 에 쓰는 값)
        self.name = os.path.basename(path)
        # Assets.xcassets / Info.plist 처럼 이름이 겹치는 파일이 있으므로
        # ID 는 반드시 프로젝트 루트 기준 전체 경로로 만든다.
        self.key = (group + "/" + path) if group else path
        self.id = oid("fileref:" + self.key)
        ext = os.path.splitext(path)[1]
        self.type = FILE_TYPES.get(ext, "text")

    @property
    def is_source(self):
        return self.path.endswith(".swift")

    @property
    def is_resource(self):
        return self.path.endswith(".json") or self.path.endswith(".xcassets")


# ---------------------------------------------------------------- 파일 목록
SHARED_ROOT = [Ref("AppGroup.swift", "Shared")]
SHARED_MODELS = [Ref("ChineseWord.swift", "Shared/Models"), Ref("StudyLevel.swift", "Shared/Models")]
SHARED_DATA = [Ref("WordRepository.swift", "Shared/Data"), Ref("words.json", "Shared/Data")]
SHARED_SERVICES = [
    Ref("AppSettingsStore.swift", "Shared/Services"),
    Ref("DailyWordService.swift", "Shared/Services"),
    Ref("SavedWordsStore.swift", "Shared/Services"),
    Ref("SeededRandom.swift", "Shared/Services"),
    Ref("StreakService.swift", "Shared/Services"),
]

APP_ROOT = [
    Ref("TodayChineseApp.swift", "TodayChinese"),
    Ref("AppModel.swift", "TodayChinese"),
    Ref("Theme.swift", "TodayChinese"),
]
APP_VIEWS = [
    Ref("RootView.swift", "TodayChinese/Views"),
    Ref("TodayView.swift", "TodayChinese/Views"),
    Ref("WordCardView.swift", "TodayChinese/Views"),
    Ref("WordDetailView.swift", "TodayChinese/Views"),
    Ref("SavedWordsView.swift", "TodayChinese/Views"),
    Ref("SettingsView.swift", "TodayChinese/Views"),
    Ref("OnboardingView.swift", "TodayChinese/Views"),
    Ref("Components.swift", "TodayChinese/Views"),
]
APP_SERVICES = [
    Ref("SpeechService.swift", "TodayChinese/Services"),
    Ref("NotificationService.swift", "TodayChinese/Services"),
]
APP_SUPPORT = [
    Ref("Assets.xcassets", "TodayChinese"),
    Ref("Info.plist", "TodayChinese"),
    Ref("TodayChinese.entitlements", "TodayChinese"),
]

WIDGET_FILES = [
    Ref("TodayChineseWidgetBundle.swift", "TodayChineseWidget"),
    Ref("TodayChineseWidget.swift", "TodayChineseWidget"),
    Ref("TodayChineseWidgetProvider.swift", "TodayChineseWidget"),
    Ref("WidgetViews.swift", "TodayChineseWidget"),
    Ref("Assets.xcassets", "TodayChineseWidget"),
    Ref("Info.plist", "TodayChineseWidget"),
    Ref("TodayChineseWidget.entitlements", "TodayChineseWidget"),
]

SHARED_ALL = SHARED_ROOT + SHARED_MODELS + SHARED_DATA + SHARED_SERVICES
APP_ALL = APP_ROOT + APP_VIEWS + APP_SERVICES + APP_SUPPORT

# 타깃별 빌드 파일 (같은 파일이 두 타깃에 들어가면 PBXBuildFile 이 두 개 필요)
app_sources = [r for r in SHARED_ALL if r.is_source] + [r for r in APP_ALL if r.is_source]
app_resources = [r for r in SHARED_ALL if r.is_resource] + [r for r in APP_ALL if r.is_resource]
widget_sources = [r for r in SHARED_ALL if r.is_source] + [r for r in WIDGET_FILES if r.is_source]
widget_resources = [r for r in SHARED_ALL if r.is_resource] + [r for r in WIDGET_FILES if r.is_resource]

# ---------------------------------------------------------------- 고정 ID
IDS = {k: oid("obj:" + k) for k in [
    "project", "mainGroup", "productsGroup", "sharedGroup", "sharedModelsGroup",
    "sharedDataGroup", "sharedServicesGroup", "appGroup", "appViewsGroup",
    "appServicesGroup", "widgetGroup", "appTarget", "widgetTarget", "appProduct",
    "widgetProduct", "projectConfigList", "appConfigList", "widgetConfigList",
    "projectDebug", "projectRelease", "appDebug", "appRelease", "widgetDebug",
    "widgetRelease", "appSources", "appFrameworks", "appResources", "appEmbed",
    "widgetSources", "widgetFrameworks", "widgetResources", "targetDependency",
    "containerProxy", "embedBuildFile",
]}


def build_file_id(target, ref):
    return oid("buildfile:%s:%s" % (target, ref.key))


out = []
w = out.append

w("// !$*UTF8*$!")
w("{")
w("\tarchiveVersion = 1;")
w("\tclasses = {")
w("\t};")
w("\tobjectVersion = 56;")
w("\tobjects = {")

# ------------------------------------------------------------ PBXBuildFile
w("")
w("/* Begin PBXBuildFile section */")
for target, refs in (("app", app_sources + app_resources),
                     ("widget", widget_sources + widget_resources)):
    for ref in refs:
        w("\t\t%s /* %s in %s */ = {isa = PBXBuildFile; fileRef = %s /* %s */; };" % (
            build_file_id(target, ref), ref.name,
            "Sources" if ref.is_source else "Resources", ref.id, ref.name))
w("\t\t%s /* %s.appex in Embed Foundation Extensions */ = {isa = PBXBuildFile; "
  "fileRef = %s /* %s.appex */; settings = {ATTRIBUTES = (RemoveHeadersOnCopy, ); }; };" % (
      IDS["embedBuildFile"], WIDGET_NAME, IDS["widgetProduct"], WIDGET_NAME))
w("/* End PBXBuildFile section */")

# --------------------------------------------------- PBXContainerItemProxy
w("")
w("/* Begin PBXContainerItemProxy section */")
w("\t\t%s /* PBXContainerItemProxy */ = {" % IDS["containerProxy"])
w("\t\t\tisa = PBXContainerItemProxy;")
w("\t\t\tcontainerPortal = %s /* Project object */;" % IDS["project"])
w("\t\t\tproxyType = 1;")
w("\t\t\tremoteGlobalIDString = %s;" % IDS["widgetTarget"])
w("\t\t\tremoteInfo = %s;" % WIDGET_NAME)
w("\t\t};")
w("/* End PBXContainerItemProxy section */")

# -------------------------------------------------- PBXCopyFilesBuildPhase
w("")
w("/* Begin PBXCopyFilesBuildPhase section */")
w("\t\t%s /* Embed Foundation Extensions */ = {" % IDS["appEmbed"])
w("\t\t\tisa = PBXCopyFilesBuildPhase;")
w("\t\t\tbuildActionMask = 2147483647;")
w("\t\t\tdstPath = \"\";")
w("\t\t\tdstSubfolderSpec = 13;")
w("\t\t\tfiles = (")
w("\t\t\t\t%s /* %s.appex in Embed Foundation Extensions */," % (IDS["embedBuildFile"], WIDGET_NAME))
w("\t\t\t);")
w("\t\t\tname = \"Embed Foundation Extensions\";")
w("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
w("\t\t};")
w("/* End PBXCopyFilesBuildPhase section */")

# --------------------------------------------------------- PBXFileReference
w("")
w("/* Begin PBXFileReference section */")
for ref in SHARED_ALL + APP_ALL + WIDGET_FILES:
    w("\t\t%s /* %s */ = {isa = PBXFileReference; lastKnownFileType = %s; path = %s; sourceTree = \"<group>\"; };" % (
        ref.id, ref.name, ref.type, ref.path))
w("\t\t%s /* %s.app */ = {isa = PBXFileReference; explicitFileType = wrapper.application; "
  "includeInIndex = 0; path = %s.app; sourceTree = BUILT_PRODUCTS_DIR; };" % (
      IDS["appProduct"], APP_NAME, APP_NAME))
w("\t\t%s /* %s.appex */ = {isa = PBXFileReference; explicitFileType = \"wrapper.app-extension\"; "
  "includeInIndex = 0; path = %s.appex; sourceTree = BUILT_PRODUCTS_DIR; };" % (
      IDS["widgetProduct"], WIDGET_NAME, WIDGET_NAME))
w("/* End PBXFileReference section */")

# --------------------------------------------------- PBXFrameworksBuildPhase
w("")
w("/* Begin PBXFrameworksBuildPhase section */")
for key, label in ((IDS["appFrameworks"], APP_NAME), (IDS["widgetFrameworks"], WIDGET_NAME)):
    w("\t\t%s /* Frameworks */ = {" % key)
    w("\t\t\tisa = PBXFrameworksBuildPhase;")
    w("\t\t\tbuildActionMask = 2147483647;")
    w("\t\t\tfiles = (")
    w("\t\t\t);")
    w("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
    w("\t\t};")
w("/* End PBXFrameworksBuildPhase section */")


# ----------------------------------------------------------------- PBXGroup
def group(gid, name, children, path=None):
    w("\t\t%s /* %s */ = {" % (gid, name))
    w("\t\t\tisa = PBXGroup;")
    w("\t\t\tchildren = (")
    for cid, cname in children:
        w("\t\t\t\t%s /* %s */," % (cid, cname))
    w("\t\t\t);")
    if path is None:
        w("\t\t\tname = %s;" % name)
    else:
        w("\t\t\tpath = %s;" % path)
    w("\t\t\tsourceTree = \"<group>\";")
    w("\t\t};")


w("")
w("/* Begin PBXGroup section */")
group(IDS["mainGroup"], "TodayChinese", [
    (IDS["sharedGroup"], "Shared"),
    (IDS["appGroup"], APP_NAME),
    (IDS["widgetGroup"], "TodayChineseWidget"),
    (IDS["productsGroup"], "Products"),
])
group(IDS["sharedGroup"], "Shared",
      [(r.id, r.name) for r in SHARED_ROOT] + [
          (IDS["sharedModelsGroup"], "Models"),
          (IDS["sharedDataGroup"], "Data"),
          (IDS["sharedServicesGroup"], "Services"),
      ], path="Shared")
group(IDS["sharedModelsGroup"], "Models", [(r.id, r.name) for r in SHARED_MODELS], path="Models")
group(IDS["sharedDataGroup"], "Data", [(r.id, r.name) for r in SHARED_DATA], path="Data")
group(IDS["sharedServicesGroup"], "Services", [(r.id, r.name) for r in SHARED_SERVICES], path="Services")
group(IDS["appGroup"], APP_NAME,
      [(r.id, r.name) for r in APP_ROOT] + [
          (IDS["appViewsGroup"], "Views"),
          (IDS["appServicesGroup"], "Services"),
      ] + [(r.id, r.name) for r in APP_SUPPORT], path=APP_NAME)
group(IDS["appViewsGroup"], "Views", [(r.id, r.name) for r in APP_VIEWS], path="Views")
group(IDS["appServicesGroup"], "Services", [(r.id, r.name) for r in APP_SERVICES], path="Services")
group(IDS["widgetGroup"], "TodayChineseWidget", [(r.id, r.name) for r in WIDGET_FILES],
      path="TodayChineseWidget")
group(IDS["productsGroup"], "Products", [
    (IDS["appProduct"], APP_NAME + ".app"),
    (IDS["widgetProduct"], WIDGET_NAME + ".appex"),
])
w("/* End PBXGroup section */")

# ----------------------------------------------------------- PBXNativeTarget
w("")
w("/* Begin PBXNativeTarget section */")

w("\t\t%s /* %s */ = {" % (IDS["appTarget"], APP_NAME))
w("\t\t\tisa = PBXNativeTarget;")
w("\t\t\tbuildConfigurationList = %s /* Build configuration list for PBXNativeTarget \"%s\" */;" % (
    IDS["appConfigList"], APP_NAME))
w("\t\t\tbuildPhases = (")
w("\t\t\t\t%s /* Sources */," % IDS["appSources"])
w("\t\t\t\t%s /* Frameworks */," % IDS["appFrameworks"])
w("\t\t\t\t%s /* Resources */," % IDS["appResources"])
w("\t\t\t\t%s /* Embed Foundation Extensions */," % IDS["appEmbed"])
w("\t\t\t);")
w("\t\t\tbuildRules = (")
w("\t\t\t);")
w("\t\t\tdependencies = (")
w("\t\t\t\t%s /* PBXTargetDependency */," % IDS["targetDependency"])
w("\t\t\t);")
w("\t\t\tname = %s;" % APP_NAME)
w("\t\t\tproductName = %s;" % APP_NAME)
w("\t\t\tproductReference = %s /* %s.app */;" % (IDS["appProduct"], APP_NAME))
w("\t\t\tproductType = \"com.apple.product-type.application\";")
w("\t\t};")

w("\t\t%s /* %s */ = {" % (IDS["widgetTarget"], WIDGET_NAME))
w("\t\t\tisa = PBXNativeTarget;")
w("\t\t\tbuildConfigurationList = %s /* Build configuration list for PBXNativeTarget \"%s\" */;" % (
    IDS["widgetConfigList"], WIDGET_NAME))
w("\t\t\tbuildPhases = (")
w("\t\t\t\t%s /* Sources */," % IDS["widgetSources"])
w("\t\t\t\t%s /* Frameworks */," % IDS["widgetFrameworks"])
w("\t\t\t\t%s /* Resources */," % IDS["widgetResources"])
w("\t\t\t);")
w("\t\t\tbuildRules = (")
w("\t\t\t);")
w("\t\t\tdependencies = (")
w("\t\t\t);")
w("\t\t\tname = %s;" % WIDGET_NAME)
w("\t\t\tproductName = %s;" % WIDGET_NAME)
w("\t\t\tproductReference = %s /* %s.appex */;" % (IDS["widgetProduct"], WIDGET_NAME))
w("\t\t\tproductType = \"com.apple.product-type.app-extension\";")
w("\t\t};")
w("/* End PBXNativeTarget section */")

# ---------------------------------------------------------------- PBXProject
w("")
w("/* Begin PBXProject section */")
w("\t\t%s /* Project object */ = {" % IDS["project"])
w("\t\t\tisa = PBXProject;")
w("\t\t\tattributes = {")
w("\t\t\t\tBuildIndependentTargetsInParallel = 1;")
w("\t\t\t\tLastSwiftUpdateCheck = 1600;")
w("\t\t\t\tLastUpgradeCheck = 1600;")
w("\t\t\t\tTargetAttributes = {")
w("\t\t\t\t\t%s = {" % IDS["appTarget"])
w("\t\t\t\t\t\tCreatedOnToolsVersion = 16.0;")
w("\t\t\t\t\t};")
w("\t\t\t\t\t%s = {" % IDS["widgetTarget"])
w("\t\t\t\t\t\tCreatedOnToolsVersion = 16.0;")
w("\t\t\t\t\t};")
w("\t\t\t\t};")
w("\t\t\t};")
w("\t\t\tbuildConfigurationList = %s /* Build configuration list for PBXProject \"%s\" */;" % (
    IDS["projectConfigList"], APP_NAME))
w("\t\t\tcompatibilityVersion = \"Xcode 14.0\";")
w("\t\t\tdevelopmentRegion = ko;")
w("\t\t\thasScannedForEncodings = 0;")
w("\t\t\tknownRegions = (")
w("\t\t\t\tko,")
w("\t\t\t\ten,")
w("\t\t\t\tBase,")
w("\t\t\t);")
w("\t\t\tmainGroup = %s;" % IDS["mainGroup"])
w("\t\t\tproductRefGroup = %s /* Products */;" % IDS["productsGroup"])
w("\t\t\tprojectDirPath = \"\";")
w("\t\t\tprojectRoot = \"\";")
w("\t\t\ttargets = (")
w("\t\t\t\t%s /* %s */," % (IDS["appTarget"], APP_NAME))
w("\t\t\t\t%s /* %s */," % (IDS["widgetTarget"], WIDGET_NAME))
w("\t\t\t);")
w("\t\t};")
w("/* End PBXProject section */")

# ---------------------------------------------------- PBXResourcesBuildPhase
w("")
w("/* Begin PBXResourcesBuildPhase section */")
for key, target, refs in ((IDS["appResources"], "app", app_resources),
                          (IDS["widgetResources"], "widget", widget_resources)):
    w("\t\t%s /* Resources */ = {" % key)
    w("\t\t\tisa = PBXResourcesBuildPhase;")
    w("\t\t\tbuildActionMask = 2147483647;")
    w("\t\t\tfiles = (")
    for ref in refs:
        w("\t\t\t\t%s /* %s in Resources */," % (build_file_id(target, ref), ref.name))
    w("\t\t\t);")
    w("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
    w("\t\t};")
w("/* End PBXResourcesBuildPhase section */")

# ------------------------------------------------------ PBXSourcesBuildPhase
w("")
w("/* Begin PBXSourcesBuildPhase section */")
for key, target, refs in ((IDS["appSources"], "app", app_sources),
                          (IDS["widgetSources"], "widget", widget_sources)):
    w("\t\t%s /* Sources */ = {" % key)
    w("\t\t\tisa = PBXSourcesBuildPhase;")
    w("\t\t\tbuildActionMask = 2147483647;")
    w("\t\t\tfiles = (")
    for ref in refs:
        w("\t\t\t\t%s /* %s in Sources */," % (build_file_id(target, ref), ref.name))
    w("\t\t\t);")
    w("\t\t\trunOnlyForDeploymentPostprocessing = 0;")
    w("\t\t};")
w("/* End PBXSourcesBuildPhase section */")

# ------------------------------------------------------ PBXTargetDependency
w("")
w("/* Begin PBXTargetDependency section */")
w("\t\t%s /* PBXTargetDependency */ = {" % IDS["targetDependency"])
w("\t\t\tisa = PBXTargetDependency;")
w("\t\t\ttarget = %s /* %s */;" % (IDS["widgetTarget"], WIDGET_NAME))
w("\t\t\ttargetProxy = %s /* PBXContainerItemProxy */;" % IDS["containerProxy"])
w("\t\t};")
w("/* End PBXTargetDependency section */")

# ---------------------------------------------------- XCBuildConfiguration
BASE = [
    "ALWAYS_SEARCH_USER_PATHS = NO",
    "ASSETCATALOG_COMPILER_GENERATE_SWIFT_ASSET_SYMBOL_EXTENSIONS = YES",
    "CLANG_ANALYZER_NONNULL = YES",
    "CLANG_ANALYZER_NUMBER_OBJECT_CONVERSION = YES_AGGRESSIVE",
    "CLANG_ENABLE_MODULES = YES",
    "CLANG_ENABLE_OBJC_ARC = YES",
    "CLANG_ENABLE_OBJC_WEAK = YES",
    "CLANG_WARN_BOOL_CONVERSION = YES",
    "CLANG_WARN_DOCUMENTATION_COMMENTS = YES",
    "CLANG_WARN_EMPTY_BODY = YES",
    "CLANG_WARN_UNREACHABLE_CODE = YES",
    "COPY_PHASE_STRIP = NO",
    "ENABLE_STRICT_OBJC_MSGSEND = YES",
    "ENABLE_USER_SCRIPT_SANDBOXING = YES",
    "GCC_C_LANGUAGE_STANDARD = gnu17",
    "GCC_NO_COMMON_BLOCKS = YES",
    "GCC_WARN_UNDECLARED_SELECTOR = YES",
    "GCC_WARN_UNUSED_FUNCTION = YES",
    "GCC_WARN_UNUSED_VARIABLE = YES",
    "IPHONEOS_DEPLOYMENT_TARGET = " + DEPLOYMENT_TARGET,
    "LOCALIZATION_PREFERS_STRING_CATALOGS = YES",
    "MTL_FAST_MATH = YES",
    "SDKROOT = iphoneos",
    "SWIFT_EMIT_LOC_STRINGS = YES",
    "SWIFT_VERSION = 5.0",
    "TARGETED_DEVICE_FAMILY = \"1\"",
]
DEBUG_ONLY = [
    "DEBUG_INFORMATION_FORMAT = dwarf",
    "ENABLE_TESTABILITY = YES",
    "GCC_DYNAMIC_NO_PIC = NO",
    "GCC_OPTIMIZATION_LEVEL = 0",
    "GCC_PREPROCESSOR_DEFINITIONS = (\n\t\t\t\t\t\"DEBUG=1\",\n\t\t\t\t\t\"$(inherited)\",\n\t\t\t\t)",
    "MTL_ENABLE_DEBUG_INFO = INCLUDE_SOURCE",
    "ONLY_ACTIVE_ARCH = YES",
    "SWIFT_ACTIVE_COMPILATION_CONDITIONS = \"DEBUG $(inherited)\"",
    "SWIFT_OPTIMIZATION_LEVEL = \"-Onone\"",
]
RELEASE_ONLY = [
    "DEBUG_INFORMATION_FORMAT = \"dwarf-with-dsym\"",
    "ENABLE_NS_ASSERTIONS = NO",
    "MTL_ENABLE_DEBUG_INFO = NO",
    "SWIFT_COMPILATION_MODE = wholemodule",
    "VALIDATE_PRODUCT = YES",
]

APP_SETTINGS = [
    "ASSETCATALOG_COMPILER_APPICON_NAME = AppIcon",
    "ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor",
    "CODE_SIGN_ENTITLEMENTS = TodayChinese/TodayChinese.entitlements",
    "CODE_SIGN_STYLE = Automatic",
    "CURRENT_PROJECT_VERSION = 1",
    "ENABLE_PREVIEWS = YES",
    "GENERATE_INFOPLIST_FILE = NO",
    "INFOPLIST_FILE = TodayChinese/Info.plist",
    "LD_RUNPATH_SEARCH_PATHS = (\n\t\t\t\t\t\"$(inherited)\",\n\t\t\t\t\t\"@executable_path/Frameworks\",\n\t\t\t\t)",
    "MARKETING_VERSION = 1.0",
    "PRODUCT_BUNDLE_IDENTIFIER = " + APP_BUNDLE_ID,
    "PRODUCT_NAME = \"$(TARGET_NAME)\"",
    "SWIFT_EMIT_LOC_STRINGS = YES",
]
WIDGET_SETTINGS = [
    "ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME = AccentColor",
    "ASSETCATALOG_COMPILER_WIDGET_BACKGROUND_COLOR_NAME = WidgetBackground",
    "CODE_SIGN_ENTITLEMENTS = TodayChineseWidget/TodayChineseWidget.entitlements",
    "CODE_SIGN_STYLE = Automatic",
    "CURRENT_PROJECT_VERSION = 1",
    "ENABLE_PREVIEWS = YES",
    "GENERATE_INFOPLIST_FILE = NO",
    "INFOPLIST_FILE = TodayChineseWidget/Info.plist",
    "LD_RUNPATH_SEARCH_PATHS = (\n\t\t\t\t\t\"$(inherited)\",\n\t\t\t\t\t\"@executable_path/Frameworks\",\n\t\t\t\t\t\"@executable_path/../../Frameworks\",\n\t\t\t\t)",
    "MARKETING_VERSION = 1.0",
    "PRODUCT_BUNDLE_IDENTIFIER = " + WIDGET_BUNDLE_ID,
    "PRODUCT_NAME = \"$(TARGET_NAME)\"",
    "SKIP_INSTALL = YES",
    "SWIFT_EMIT_LOC_STRINGS = YES",
]


def config(cid, name, settings):
    w("\t\t%s /* %s */ = {" % (cid, name))
    w("\t\t\tisa = XCBuildConfiguration;")
    w("\t\t\tbuildSettings = {")
    for line in sorted(settings):
        w("\t\t\t\t%s;" % line)
    w("\t\t\t};")
    w("\t\t\tname = %s;" % name)
    w("\t\t};")


w("")
w("/* Begin XCBuildConfiguration section */")
config(IDS["projectDebug"], "Debug", BASE + DEBUG_ONLY)
config(IDS["projectRelease"], "Release", BASE + RELEASE_ONLY)
config(IDS["appDebug"], "Debug", APP_SETTINGS)
config(IDS["appRelease"], "Release", APP_SETTINGS)
config(IDS["widgetDebug"], "Debug", WIDGET_SETTINGS)
config(IDS["widgetRelease"], "Release", WIDGET_SETTINGS)
w("/* End XCBuildConfiguration section */")

# ---------------------------------------------------- XCConfigurationList
w("")
w("/* Begin XCConfigurationList section */")
for cid, label, debug, release in (
    (IDS["projectConfigList"], "PBXProject \"%s\"" % APP_NAME, IDS["projectDebug"], IDS["projectRelease"]),
    (IDS["appConfigList"], "PBXNativeTarget \"%s\"" % APP_NAME, IDS["appDebug"], IDS["appRelease"]),
    (IDS["widgetConfigList"], "PBXNativeTarget \"%s\"" % WIDGET_NAME, IDS["widgetDebug"], IDS["widgetRelease"]),
):
    w("\t\t%s /* Build configuration list for %s */ = {" % (cid, label))
    w("\t\t\tisa = XCConfigurationList;")
    w("\t\t\tbuildConfigurations = (")
    w("\t\t\t\t%s /* Debug */," % debug)
    w("\t\t\t\t%s /* Release */," % release)
    w("\t\t\t);")
    w("\t\t\tdefaultConfigurationIsVisible = 0;")
    w("\t\t\tdefaultConfigurationName = Release;")
    w("\t\t};")
w("/* End XCConfigurationList section */")

w("\t};")
w("\trootObject = %s /* Project object */;" % IDS["project"])
w("}")

proj_dir = os.path.join(ROOT, "TodayChinese.xcodeproj")
os.makedirs(proj_dir, exist_ok=True)
with open(os.path.join(proj_dir, "project.pbxproj"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(out) + "\n")

# ---------------------------------------------------------------- 스킴 2개
schemes_dir = os.path.join(proj_dir, "xcshareddata", "xcschemes")
os.makedirs(schemes_dir, exist_ok=True)

SCHEME = """<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion = "1600" version = "1.7">
   <BuildAction parallelizeBuildables = "YES" buildImplicitDependencies = "YES">
      <BuildActionEntries>
         <BuildActionEntry buildForTesting = "YES" buildForRunning = "YES" buildForProfiling = "YES" buildForArchiving = "YES" buildForAnalyzing = "YES">
            <BuildableReference
               BuildableIdentifier = "primary"
               BlueprintIdentifier = "{target_id}"
               BuildableName = "{buildable_name}"
               BlueprintName = "{target_name}"
               ReferencedContainer = "container:TodayChinese.xcodeproj">
            </BuildableReference>
         </BuildActionEntry>
      </BuildActionEntries>
   </BuildAction>
   <TestAction buildConfiguration = "Debug" selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB" shouldUseLaunchSchemeArgsEnv = "YES">
      <Testables>
      </Testables>
   </TestAction>
   <LaunchAction buildConfiguration = "Debug" selectedDebuggerIdentifier = "Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier = "Xcode.DebuggerFoundation.Launcher.LLDB" launchStyle = "0" useCustomWorkingDirectory = "NO" ignoresPersistentStateOnLaunch = "NO" debugDocumentVersioning = "YES" debugServiceExtension = "internal" allowLocationSimulation = "YES">
      <BuildableProductRunnable runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{run_target_id}"
            BuildableName = "TodayChinese.app"
            BlueprintName = "TodayChinese"
            ReferencedContainer = "container:TodayChinese.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </LaunchAction>
   <ProfileAction buildConfiguration = "Release" shouldUseLaunchSchemeArgsEnv = "YES" savedToolIdentifier = "" useCustomWorkingDirectory = "NO" debugDocumentVersioning = "YES">
      <BuildableProductRunnable runnableDebuggingMode = "0">
         <BuildableReference
            BuildableIdentifier = "primary"
            BlueprintIdentifier = "{run_target_id}"
            BuildableName = "TodayChinese.app"
            BlueprintName = "TodayChinese"
            ReferencedContainer = "container:TodayChinese.xcodeproj">
         </BuildableReference>
      </BuildableProductRunnable>
   </ProfileAction>
   <AnalyzeAction buildConfiguration = "Debug">
   </AnalyzeAction>
   <ArchiveAction buildConfiguration = "Release" revealArchiveInOrganizer = "YES">
   </ArchiveAction>
</Scheme>
"""

with open(os.path.join(schemes_dir, "TodayChinese.xcscheme"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(SCHEME.format(target_id=IDS["appTarget"], buildable_name="TodayChinese.app",
                           target_name="TodayChinese", run_target_id=IDS["appTarget"]))

with open(os.path.join(schemes_dir, "TodayChineseWidgetExtension.xcscheme"), "w",
          encoding="utf-8", newline="\n") as fh:
    fh.write(SCHEME.format(target_id=IDS["widgetTarget"],
                           buildable_name="TodayChineseWidgetExtension.appex",
                           target_name="TodayChineseWidgetExtension",
                           run_target_id=IDS["appTarget"]))

# workspace 설정 (Xcode 가 자동 생성하지만 미리 넣어두면 첫 열기가 매끄럽다)
ws_dir = os.path.join(proj_dir, "project.xcworkspace")
os.makedirs(ws_dir, exist_ok=True)
with open(os.path.join(ws_dir, "contents.xcworkspacedata"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<Workspace\n   version = "1.0">\n'
             '   <FileRef\n      location = "self:">\n   </FileRef>\n'
             '</Workspace>\n')

print("wrote", os.path.join(proj_dir, "project.pbxproj"))
print("app sources:", len(app_sources), "widget sources:", len(widget_sources))
print("app resources:", len(app_resources), "widget resources:", len(widget_resources))
