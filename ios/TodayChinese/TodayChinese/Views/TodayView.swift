import SwiftUI

struct TodayView: View {
    @Environment(AppModel.self) private var model
    @State private var appeared = false

    private var today: String {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "ko_KR")
        formatter.dateFormat = "M월 d일 EEEE"
        return formatter.string(from: Date())
    }

    var body: some View {
        @Bindable var model = model

        NavigationStack {
            ZStack {
                Theme.background.ignoresSafeArea()

                ScrollView {
                    VStack(spacing: 18) {
                        Text(today)
                            .font(.system(size: 13, weight: .medium))
                            .foregroundStyle(Theme.tertiary)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.top, 4)

                        WordHeadlineCard(word: model.todayWord)
                            .cardStyle(padding: 26)

                        ExampleCard(word: model.todayWord)
                            .cardStyle()

                        WordActionButtons(word: model.todayWord)
                            .padding(.top, 2)

                        StreakBadge(days: model.streak)
                            .padding(.top, 6)
                            .padding(.bottom, 24)
                    }
                    .padding(.horizontal, Theme.pagePadding)
                    .opacity(appeared ? 1 : 0)
                    .offset(y: appeared ? 0 : 8)
                }
                .scrollIndicators(.hidden)
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbar(.hidden, for: .navigationBar)
            .sheet(item: $model.presentedWord) { word in
                WordDetailView(word: word, showsCloseButton: true)
            }
        }
        .onAppear {
            model.refreshIfNeeded()
            model.markTodayAsStudied()
            withAnimation(.easeOut(duration: 0.32)) { appeared = true }
        }
    }
}

#Preview {
    TodayView()
        .environment(AppModel())
        .environment(SavedWordsStore.shared)
}
