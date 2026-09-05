import Foundation

/// 연속 학습일 관리. 하루에 한 번 오늘의 단어를 보면 1 올라가고,
/// 하루라도 건너뛰면 1부터 다시 시작한다.
enum StreakService {
    /// 화면에 보여줄 현재 streak. 어제까지도 안 봤다면 0.
    static func displayCount(
        asOf date: Date = Date(),
        defaults: UserDefaults = AppGroup.defaults,
        calendar: Calendar = .current
    ) -> Int {
        guard defaults.object(forKey: DefaultsKey.streakLastDay) != nil else { return 0 }
        let lastDay = defaults.integer(forKey: DefaultsKey.streakLastDay)
        let today = DailyWordService.dayIndex(for: date, calendar: calendar)
        guard today - lastDay <= 1 else { return 0 }
        return max(0, defaults.integer(forKey: DefaultsKey.streakCount))
    }

    /// 오늘 학습을 기록하고 갱신된 streak 을 돌려준다. 같은 날 여러 번 불러도 안전하다.
    @discardableResult
    static func registerVisit(
        on date: Date = Date(),
        defaults: UserDefaults = AppGroup.defaults,
        calendar: Calendar = .current
    ) -> Int {
        let today = DailyWordService.dayIndex(for: date, calendar: calendar)
        let stored = defaults.integer(forKey: DefaultsKey.streakCount)

        guard defaults.object(forKey: DefaultsKey.streakLastDay) != nil else {
            return persist(count: 1, day: today, to: defaults)
        }

        let lastDay = defaults.integer(forKey: DefaultsKey.streakLastDay)
        switch today - lastDay {
        case 0:
            return persist(count: max(1, stored), day: today, to: defaults)
        case 1:
            return persist(count: max(1, stored) + 1, day: today, to: defaults)
        default:
            // 미래로 시간을 되돌린 경우(음수)까지 포함해 새로 시작한다.
            return persist(count: 1, day: today, to: defaults)
        }
    }

    @discardableResult
    private static func persist(count: Int, day: Int, to defaults: UserDefaults) -> Int {
        defaults.set(count, forKey: DefaultsKey.streakCount)
        defaults.set(day, forKey: DefaultsKey.streakLastDay)
        return count
    }

    static func reset(defaults: UserDefaults = AppGroup.defaults) {
        defaults.removeObject(forKey: DefaultsKey.streakCount)
        defaults.removeObject(forKey: DefaultsKey.streakLastDay)
    }
}
