import Foundation

/// 앱과 위젯 익스텐션이 공유하는 상수 모음.
enum AppGroup {
    /// Signing & Capabilities 의 App Groups 에 등록하는 식별자.
    /// 값을 바꾸면 두 타깃의 .entitlements 파일도 함께 바꿔야 한다.
    static let identifier = "group.com.jamidusu.todaychinese"

    /// 위젯 탭 -> 앱 이동에 쓰는 URL scheme.
    static let urlScheme = "todaychinese"

    /// WidgetKit 의 `kind`. 앱에서 타임라인을 새로고침할 때 쓴다.
    static let widgetKind = "TodayChineseWidget"

    /// App Group entitlement 이 실제로 부여됐는지.
    ///
    /// `UserDefaults(suiteName:)` 는 권한이 없어도 non-nil 을 돌려주고
    /// 조용히 앱 자기 컨테이너에 쓴다. 그래서 공유 컨테이너 URL 로 판별한다.
    /// (무료 Apple ID 로 사이드로드하면 App Groups 가 지원되지 않아 false 가 된다.)
    static let isSharedStoreAvailable: Bool = {
        FileManager.default
            .containerURL(forSecurityApplicationGroupIdentifier: identifier) != nil
    }()

    /// App Group 을 못 쓰는 환경에서도 앱이 죽지 않도록 standard 로 폴백한다.
    /// 폴백 상태에서는 앱과 위젯이 값을 공유하지 못하고,
    /// 위젯은 `AppSettings.default` 기준으로 단어를 고른다.
    static let defaults: UserDefaults = {
        guard isSharedStoreAvailable, let shared = UserDefaults(suiteName: identifier) else {
            return .standard
        }
        return shared
    }()
}

/// UserDefaults 키. 앱과 위젯이 같은 문자열을 봐야 하므로 한곳에 모아둔다.
enum DefaultsKey {
    static let selectedLevels = "settings.selectedLevels"
    static let selectedCategories = "settings.selectedCategories"
    static let hasCompletedOnboarding = "settings.hasCompletedOnboarding"
    static let notificationsEnabled = "settings.notificationsEnabled"
    static let notificationHour = "settings.notificationHour"
    static let notificationMinute = "settings.notificationMinute"

    static let savedWordIDs = "words.saved"
    static let historyWordIDs = "words.history"

    static let streakCount = "streak.count"
    static let streakLastDay = "streak.lastDay"
}
