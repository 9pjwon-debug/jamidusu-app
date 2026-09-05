import Foundation
import UserNotifications

/// 하루 한 번 알림. 앱 첫 실행에서는 권한을 묻지 않고,
/// 사용자가 설정에서 알림을 켤 때만 권한을 요청한다.
enum NotificationService {
    static let requestIdentifier = "todaychinese.daily"

    static func authorizationStatus() async -> UNAuthorizationStatus {
        await UNUserNotificationCenter.current().notificationSettings().authorizationStatus
    }

    /// 권한을 요청하고 허용 여부를 돌려준다.
    static func requestAuthorization() async -> Bool {
        do {
            return try await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .sound])
        } catch {
            return false
        }
    }

    /// 매일 지정한 시각에 반복되는 알림 하나만 유지한다.
    static func schedule(hour: Int, minute: Int) async {
        let center = UNUserNotificationCenter.current()
        center.removePendingNotificationRequests(withIdentifiers: [requestIdentifier])

        let content = UNMutableNotificationContent()
        content.title = "🇨🇳"
        content.body = "오늘의 중국어가 도착했어요."
        content.sound = .default

        var components = DateComponents()
        components.hour = hour
        components.minute = minute

        let trigger = UNCalendarNotificationTrigger(dateMatching: components, repeats: true)
        let request = UNNotificationRequest(identifier: requestIdentifier, content: content, trigger: trigger)
        try? await center.add(request)
    }

    static func cancel() {
        UNUserNotificationCenter.current()
            .removePendingNotificationRequests(withIdentifiers: [requestIdentifier])
    }
}
