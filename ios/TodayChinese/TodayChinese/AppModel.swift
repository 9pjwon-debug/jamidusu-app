import Foundation
import Observation
import WidgetKit

/// 앱 전역 상태. 설정을 바꾸면 위젯 타임라인도 함께 새로고침한다.
@Observable
final class AppModel {
    enum Tab: Hashable {
        case today, saved, settings
    }

    private(set) var settings: AppSettings
    private(set) var todayWord: ChineseWord
    private(set) var streak: Int

    var selectedTab: Tab = .today
    /// 위젯을 탭해서 들어왔을 때 띄우는 상세 화면.
    var presentedWord: ChineseWord?

    private var lastRefreshedDayIndex: Int

    init() {
        let loaded = AppSettingsStore.load()
        settings = loaded
        todayWord = DailyWordService.word(settings: loaded)
        streak = StreakService.displayCount()
        lastRefreshedDayIndex = DailyWordService.dayIndex()
    }

    var hasCompletedOnboarding: Bool { settings.hasCompletedOnboarding }

    // MARK: - 오늘의 단어

    /// 앱이 다시 활성화될 때 호출. 날짜가 바뀌었으면 단어를 새로 고른다.
    func refreshIfNeeded() {
        let today = DailyWordService.dayIndex()
        guard today != lastRefreshedDayIndex else { return }
        lastRefreshedDayIndex = today
        recomputeTodayWord()
    }

    /// 오늘의 단어를 실제로 "본" 순간에 호출한다. streak 과 history 를 갱신한다.
    func markTodayAsStudied() {
        streak = StreakService.registerVisit()
        WordHistoryStore.record(todayWord)
    }

    private func recomputeTodayWord() {
        todayWord = DailyWordService.word(settings: settings)
    }

    // MARK: - 설정

    func completeOnboarding(levels: Set<StudyLevel>) {
        var updated = settings
        updated.levels = levels.isEmpty ? StudyLevel.defaultSelection : levels
        updated.hasCompletedOnboarding = true
        apply(updated)
    }

    func updateLevels(_ levels: Set<StudyLevel>) {
        var updated = settings
        updated.levels = levels.isEmpty ? StudyLevel.defaultSelection : levels
        apply(updated)
    }

    func updateCategories(_ categories: Set<String>) {
        var updated = settings
        updated.categories = categories
        apply(updated)
    }

    func updateNotification(enabled: Bool, hour: Int, minute: Int) {
        var updated = settings
        updated.notificationsEnabled = enabled
        updated.notificationHour = hour
        updated.notificationMinute = minute
        apply(updated)
    }

    private func apply(_ updated: AppSettings) {
        settings = updated
        AppSettingsStore.save(updated)
        recomputeTodayWord()
        reloadWidgets()
    }

    func reloadWidgets() {
        WidgetCenter.shared.reloadTimelines(ofKind: AppGroup.widgetKind)
    }

    // MARK: - 위젯 딥링크

    /// `todaychinese://today` 로 들어오면 오늘 탭, `/detail` 이면 상세까지 연다.
    func handle(url: URL) {
        guard url.scheme == AppGroup.urlScheme else { return }
        selectedTab = .today
        let wantsDetail = url.host() == "detail"
            || url.pathComponents.contains("detail")
        presentedWord = wantsDetail ? todayWord : nil
    }
}
