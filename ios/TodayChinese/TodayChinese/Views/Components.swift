import SwiftUI

/// 라운드 캡슐 버튼. 채움형과 외곽선형 두 가지.
struct PillButtonStyle: ButtonStyle {
    enum Kind { case filled, outlined }

    var kind: Kind = .outlined

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 16, weight: .medium))
            .frame(maxWidth: .infinity)
            .padding(.vertical, 14)
            .foregroundStyle(kind == .filled ? Theme.card : Theme.ink)
            .background(
                Capsule(style: .continuous)
                    .fill(kind == .filled ? Theme.ink : Theme.card)
            )
            .overlay(
                Capsule(style: .continuous)
                    .stroke(kind == .filled ? .clear : Theme.hairline, lineWidth: 1)
            )
            .scaleEffect(configuration.isPressed ? 0.975 : 1)
            .animation(.easeOut(duration: 0.14), value: configuration.isPressed)
    }
}

/// "HSK 3", "일상" 같은 작은 라벨.
struct MetaChip: View {
    let text: String

    var body: some View {
        Text(text)
            .font(.system(size: 12, weight: .medium))
            .foregroundStyle(Theme.secondary)
            .padding(.horizontal, 10)
            .padding(.vertical, 5)
            .background(
                Capsule(style: .continuous)
                    .fill(Theme.ink.opacity(0.05))
            )
    }
}

/// 하단의 조용한 streak 표시. 게임처럼 요란하게 만들지 않는다.
struct StreakBadge: View {
    let days: Int

    var body: some View {
        Group {
            if days > 0 {
                Text("🔥 \(days)일 연속 학습 중")
            } else {
                Text("오늘부터 다시 시작해요")
            }
        }
        .font(.system(size: 13))
        .foregroundStyle(Theme.tertiary)
    }
}

/// 목록에 쓰는 한 줄짜리 단어 행.
struct WordRow: View {
    let word: ChineseWord

    var body: some View {
        HStack(alignment: .firstTextBaseline, spacing: 12) {
            Text(word.word)
                .font(.system(size: 22, weight: .semibold))
                .foregroundStyle(Theme.ink)

            VStack(alignment: .leading, spacing: 2) {
                Text(word.pinyin)
                    .font(.system(size: 13))
                    .foregroundStyle(Theme.secondary)
                Text(word.meaning)
                    .font(.system(size: 14))
                    .foregroundStyle(Theme.ink.opacity(0.85))
            }

            Spacer(minLength: 8)
        }
        .padding(.vertical, 10)
        .contentShape(Rectangle())
    }
}

/// 내용이 비었을 때 보여주는 조용한 안내.
struct EmptyStateView: View {
    let title: String
    let message: String

    var body: some View {
        VStack(spacing: 8) {
            Text(title)
                .font(.system(size: 17, weight: .semibold))
                .foregroundStyle(Theme.ink)
            Text(message)
                .font(.system(size: 14))
                .foregroundStyle(Theme.secondary)
                .multilineTextAlignment(.center)
        }
        .padding(.horizontal, 32)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
