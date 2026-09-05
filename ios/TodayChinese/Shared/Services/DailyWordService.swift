import Foundation

/// "오늘의 단어" 를 정하는 순수 함수 모음.
///
/// 앱과 위젯은 서로 통신하지 않고 각자 이 함수를 호출한다.
/// 따라서 계산은 (날짜 + 설정) 만으로 완전히 결정되어야 한다.
///
/// 선택 방식:
///  1. 조건에 맞는 단어를 id 순으로 정렬해 pool 을 만든다.
///  2. pool 구성으로 지문(fingerprint)을 만들어 한 번 결정적으로 섞는다.
///  3. 날짜 인덱스를 pool.count 로 나눈 나머지 위치의 단어를 고른다.
///
/// 이렇게 하면 "연속한 어떤 pool.count 일을 잘라 봐도 같은 단어가 두 번
/// 나오지 않는다" 가 수학적으로 보장된다. (나머지 연산이 전단사이므로)
///
/// 주기마다 순서를 다시 섞으면 주기 경계에서 같은 단어가 이틀 연속
/// 나올 수 있다. 실제로 시뮬레이션에서 그런 사례가 나와서, 순서를 매번
/// 바꾸는 대신 "절대 가까이 반복되지 않는" 쪽을 택했다.
/// (대신 순서는 pool.count 일마다 그대로 반복된다 - 122단어 기준 약 4개월)
enum DailyWordService {
    /// 기준일(2024-01-01)부터 며칠이 지났는지.
    static func dayIndex(for date: Date = Date(), calendar: Calendar = .current) -> Int {
        var components = DateComponents()
        components.year = 2024
        components.month = 1
        components.day = 1
        guard let reference = calendar.date(from: components) else { return 0 }
        let start = calendar.startOfDay(for: date)
        return calendar.dateComponents([.day], from: calendar.startOfDay(for: reference), to: start).day ?? 0
    }

    static func word(
        for date: Date = Date(),
        settings: AppSettings,
        repository: WordRepository = .shared,
        calendar: Calendar = .current
    ) -> ChineseWord {
        let pool = repository
            .words(levels: settings.levels, categories: settings.categories)
            .sorted { $0.id < $1.id }
        guard let first = pool.first else { return .placeholder }
        guard pool.count > 1 else { return first }

        let order = ordering(for: pool)
        let count = order.count
        let index = dayIndex(for: date, calendar: calendar)
        let offset = ((index % count) + count) % count
        return order[offset]
    }

    /// pool 구성이 같으면 언제 호출해도 같은 순서를 돌려준다.
    /// 난이도/카테고리를 바꾸면 pool 이 달라지므로 순서도 함께 달라진다.
    static func ordering(for pool: [ChineseWord]) -> [ChineseWord] {
        var fingerprint: UInt64 = 0xCBF2_9CE4_8422_2325   // FNV-1a offset basis
        for word in pool {
            fingerprint = (fingerprint ^ UInt64(max(0, word.id))) &* 0x1000_0000_01B3
        }
        return pool.seededShuffled(seed: fingerprint)
    }

    /// 위젯 타임라인용. 오늘 이후 `days` 일치의 (자정, 단어) 목록.
    static func upcoming(
        days: Int,
        from date: Date = Date(),
        settings: AppSettings,
        repository: WordRepository = .shared,
        calendar: Calendar = .current
    ) -> [(date: Date, word: ChineseWord)] {
        let today = calendar.startOfDay(for: date)
        return (0..<max(1, days)).compactMap { offset in
            guard let day = calendar.date(byAdding: .day, value: offset, to: today) else { return nil }
            // 첫 항목만 "지금"으로 시작해 위젯이 즉시 갱신되게 한다.
            let entryDate = offset == 0 ? date : day
            return (entryDate, word(for: day, settings: settings, repository: repository, calendar: calendar))
        }
    }

    /// 다음 자정. 타임라인 갱신 시점으로 쓴다.
    static func nextMidnight(after date: Date = Date(), calendar: Calendar = .current) -> Date {
        let start = calendar.startOfDay(for: date)
        return calendar.date(byAdding: .day, value: 1, to: start) ?? date.addingTimeInterval(86_400)
    }
}
