import SwiftUI

/// 단어 하나의 상세. 위젯에서 들어오면 시트로, 단어장에서 들어오면 푸시로 열린다.
struct WordDetailView: View {
    let word: ChineseWord
    var showsCloseButton = false

    @Environment(\.dismiss) private var dismiss

    var body: some View {
        if showsCloseButton {
            NavigationStack {
                content
                    .toolbar {
                        ToolbarItem(placement: .topBarTrailing) {
                            Button("닫기") { dismiss() }
                                .font(.system(size: 16, weight: .medium))
                        }
                    }
                    .navigationBarTitleDisplayMode(.inline)
            }
        } else {
            content
                .navigationBarTitleDisplayMode(.inline)
        }
    }

    private var content: some View {
        ZStack {
            Theme.background.ignoresSafeArea()

            ScrollView {
                VStack(spacing: 18) {
                    WordHeadlineCard(word: word, hanziSize: 54)
                        .cardStyle(padding: 26)

                    ExampleCard(word: word)
                        .cardStyle()

                    WordActionButtons(word: word)
                        .padding(.bottom, 24)
                }
                .padding(.horizontal, Theme.pagePadding)
                .padding(.top, 8)
            }
            .scrollIndicators(.hidden)
        }
    }
}
