import SwiftUI

/// 한자 -> 병음 -> 뜻 순서의 시각적 계층. 앱과 위젯이 같은 순서를 지킨다.
struct WordHeadlineCard: View {
    let word: ChineseWord
    var hanziSize: CGFloat = 60

    var body: some View {
        VStack(spacing: 10) {
            Text(word.word)
                .font(.system(size: hanziSize, weight: .semibold))
                .foregroundStyle(Theme.ink)
                .minimumScaleFactor(0.5)
                .lineLimit(1)

            Text(word.pinyin)
                .font(.system(size: 20, weight: .regular))
                .foregroundStyle(Theme.secondary)

            Text(word.meaning)
                .font(.system(size: 19, weight: .medium))
                .foregroundStyle(Theme.ink.opacity(0.9))
                .multilineTextAlignment(.center)

            HStack(spacing: 6) {
                MetaChip(text: word.level)
                MetaChip(text: word.category)
            }
            .padding(.top, 4)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 8)
    }
}

/// 예문 카드. 중국어 -> 병음 -> 한국어 순서.
struct ExampleCard: View {
    let word: ChineseWord

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(word.example)
                .font(.system(size: 22, weight: .medium))
                .foregroundStyle(Theme.ink)
                .fixedSize(horizontal: false, vertical: true)

            Text(word.examplePinyin)
                .font(.system(size: 14))
                .foregroundStyle(Theme.secondary)
                .fixedSize(horizontal: false, vertical: true)

            Text(word.translation)
                .font(.system(size: 15))
                .foregroundStyle(Theme.ink.opacity(0.85))
                .fixedSize(horizontal: false, vertical: true)
                .padding(.top, 2)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}

/// 발음 듣기 / 저장하기 두 개의 버튼.
struct WordActionButtons: View {
    let word: ChineseWord
    @Environment(SavedWordsStore.self) private var savedWords
    @State private var speech = SpeechService.shared

    private var isSaved: Bool { savedWords.contains(word) }

    var body: some View {
        HStack(spacing: 12) {
            Button {
                speech.speak(word)
            } label: {
                Label(speech.isSpeaking ? "재생 중" : "발음 듣기", systemImage: "speaker.wave.2")
            }
            .buttonStyle(PillButtonStyle(kind: .filled))

            Button {
                withAnimation(.easeOut(duration: 0.18)) {
                    savedWords.toggle(word)
                }
            } label: {
                Label(isSaved ? "저장됨" : "저장하기", systemImage: isSaved ? "heart.fill" : "heart")
            }
            .buttonStyle(PillButtonStyle())
        }
    }
}
