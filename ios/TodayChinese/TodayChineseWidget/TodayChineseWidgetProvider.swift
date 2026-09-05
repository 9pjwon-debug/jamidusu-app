import WidgetKit
import Foundation

struct WordEntry: TimelineEntry {
    let date: Date
    let word: ChineseWord
}

/// 하루에 하나씩, 자정마다 바뀌는 타임라인.
/// 단어는 App Group 에 저장된 설정만으로 계산하므로 앱과 항상 같은 결과가 나온다.
struct TodayChineseWidgetProvider: TimelineProvider {
    /// 한 번에 미리 만들어 두는 일수. 앱을 열지 않아도 일주일은 알아서 넘어간다.
    private let preparedDays = 7

    func placeholder(in context: Context) -> WordEntry {
        WordEntry(date: Date(), word: .placeholder)
    }

    func getSnapshot(in context: Context, completion: @escaping (WordEntry) -> Void) {
        let word = context.isPreview
            ? ChineseWord.placeholder
            : DailyWordService.word(settings: AppSettingsStore.load())
        completion(WordEntry(date: Date(), word: word))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<WordEntry>) -> Void) {
        let settings = AppSettingsStore.load()
        let upcoming = DailyWordService.upcoming(days: preparedDays, settings: settings)
        let entries = upcoming.map { WordEntry(date: $0.date, word: $0.word) }

        let lastDate = entries.last?.date ?? Date()
        let refreshDate = DailyWordService.nextMidnight(after: lastDate)

        completion(Timeline(entries: entries, policy: .after(refreshDate)))
    }
}
