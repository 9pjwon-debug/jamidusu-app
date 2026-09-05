import Foundation

/// 앱과 위젯이 함께 읽는 사용자 설정 값.
struct AppSettings: Equatable, Sendable {
    var levels: Set<StudyLevel>
    var categories: Set<String>          // 비어 있으면 "전체"
    var hasCompletedOnboarding: Bool
    var notificationsEnabled: Bool
    var notificationHour: Int
    var notificationMinute: Int

    static let `default` = AppSettings(
        levels: StudyLevel.defaultSelection,
        categories: [],
        hasCompletedOnboarding: false,
        notificationsEnabled: false,
        notificationHour: 8,
        notificationMinute: 0
    )
}

/// App Group UserDefaults 를 감싼 얇은 읽기/쓰기 계층.
enum AppSettingsStore {
    static func load(from defaults: UserDefaults = AppGroup.defaults) -> AppSettings {
        var settings = AppSettings.default

        if let raw = defaults.array(forKey: DefaultsKey.selectedLevels) as? [String] {
            let parsed = Set(raw.compactMap(StudyLevel.init(rawValue:)))
            if !parsed.isEmpty { settings.levels = parsed }
        }
        if let raw = defaults.array(forKey: DefaultsKey.selectedCategories) as? [String] {
            settings.categories = Set(raw)
        }
        settings.hasCompletedOnboarding = defaults.bool(forKey: DefaultsKey.hasCompletedOnboarding)
        settings.notificationsEnabled = defaults.bool(forKey: DefaultsKey.notificationsEnabled)
        if defaults.object(forKey: DefaultsKey.notificationHour) != nil {
            settings.notificationHour = defaults.integer(forKey: DefaultsKey.notificationHour)
        }
        if defaults.object(forKey: DefaultsKey.notificationMinute) != nil {
            settings.notificationMinute = defaults.integer(forKey: DefaultsKey.notificationMinute)
        }
        return settings
    }

    static func save(_ settings: AppSettings, to defaults: UserDefaults = AppGroup.defaults) {
        defaults.set(settings.levels.map(\.rawValue).sorted(), forKey: DefaultsKey.selectedLevels)
        defaults.set(settings.categories.sorted(), forKey: DefaultsKey.selectedCategories)
        defaults.set(settings.hasCompletedOnboarding, forKey: DefaultsKey.hasCompletedOnboarding)
        defaults.set(settings.notificationsEnabled, forKey: DefaultsKey.notificationsEnabled)
        defaults.set(settings.notificationHour, forKey: DefaultsKey.notificationHour)
        defaults.set(settings.notificationMinute, forKey: DefaultsKey.notificationMinute)
    }
}
