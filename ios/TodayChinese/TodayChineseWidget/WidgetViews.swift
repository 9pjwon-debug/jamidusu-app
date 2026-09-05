import WidgetKit
import SwiftUI

struct TodayChineseWidgetEntryView: View {
    @Environment(\.widgetFamily) private var family
    let entry: WordEntry

    var body: some View {
        switch family {
        case .accessoryCircular:
            CircularWordView(word: entry.word)
        case .accessoryInline:
            InlineWordView(word: entry.word)
        default:
            RectangularWordView(word: entry.word)
        }
    }
}

/// 가장 중요한 위젯.
/// 제목이나 앱 이름은 넣지 않고, 한자 -> 병음 -> 뜻 순서로만 보여준다.
/// 세로 공간이 남으면 3줄, 좁으면 2줄로 자연스럽게 접힌다.
struct RectangularWordView: View {
    let word: ChineseWord

    var body: some View {
        ViewThatFits(in: .vertical) {
            threeLine
            twoLine
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .leading)
    }

    private var threeLine: some View {
        VStack(alignment: .leading, spacing: 1) {
            hanzi(size: 22)
            Text(word.pinyin)
                .font(.system(size: 13, weight: .regular))
                .foregroundStyle(.secondary)
                .lineLimit(1)
                .minimumScaleFactor(0.8)
            Text(word.meaning)
                .font(.system(size: 12, weight: .regular))
                .lineLimit(1)
                .minimumScaleFactor(0.8)
        }
    }

    private var twoLine: some View {
        VStack(alignment: .leading, spacing: 1) {
            hanzi(size: 20)
            Text("\(word.pinyin) · \(word.meaning)")
                .font(.system(size: 12, weight: .regular))
                .foregroundStyle(.secondary)
                .lineLimit(1)
                .minimumScaleFactor(0.75)
        }
    }

    private func hanzi(size: CGFloat) -> some View {
        Text(word.word)
            .font(.system(size: size, weight: .semibold))
            .lineLimit(1)
            .minimumScaleFactor(0.6)
    }
}

/// 원형 위젯. 뜻이나 병음을 억지로 넣지 않고 한자만 크게 보여준다.
struct CircularWordView: View {
    let word: ChineseWord

    private var text: String { word.compactWord }

    private var fontSize: CGFloat {
        switch text.count {
        case 0, 1: return 30
        case 2: return 22
        default: return 16
        }
    }

    var body: some View {
        ZStack {
            AccessoryWidgetBackground()
            Text(text)
                .font(.system(size: fontSize, weight: .semibold))
                .lineLimit(1)
                .minimumScaleFactor(0.5)
                .padding(3)
        }
    }
}

/// 시간 아래 한 줄. 최대한 짧게.
struct InlineWordView: View {
    let word: ChineseWord

    var body: some View {
        Text("\(word.word) · \(word.shortMeaning)")
    }
}

#Preview("Rectangular", as: .accessoryRectangular) {
    TodayChineseWidget()
} timeline: {
    WordEntry(date: .now, word: .placeholder)
}

#Preview("Circular", as: .accessoryCircular) {
    TodayChineseWidget()
} timeline: {
    WordEntry(date: .now, word: .placeholder)
}

#Preview("Inline", as: .accessoryInline) {
    TodayChineseWidget()
} timeline: {
    WordEntry(date: .now, word: .placeholder)
}
