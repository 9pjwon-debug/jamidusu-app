import WidgetKit
import SwiftUI

struct TodayChineseWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: AppGroup.widgetKind, provider: TodayChineseWidgetProvider()) { entry in
            TodayChineseWidgetEntryView(entry: entry)
                // 잠금화면 위젯은 배경을 그리지 않는다.
                .containerBackground(.clear, for: .widget)
                // 탭하면 오늘의 단어 상세로 이동.
                .widgetURL(URL(string: "\(AppGroup.urlScheme)://detail"))
        }
        // 아래 두 값은 '위젯 추가' 갤러리에서만 쓰인다.
        // 잠금화면에 실제로 표시되는 위젯에는 제목이 들어가지 않는다.
        .configurationDisplayName("오늘의 중국어")
        .description("잠금화면에서 하루 한 단어.")
        .supportedFamilies([.accessoryRectangular, .accessoryCircular, .accessoryInline])
    }
}
