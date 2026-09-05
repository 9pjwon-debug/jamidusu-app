import SwiftUI

struct RootView: View {
    @Environment(AppModel.self) private var model

    var body: some View {
        Group {
            if model.hasCompletedOnboarding {
                MainTabView()
                    .transition(.opacity)
            } else {
                OnboardingView()
                    .transition(.opacity)
            }
        }
        .animation(.easeInOut(duration: 0.28), value: model.hasCompletedOnboarding)
    }
}

struct MainTabView: View {
    @Environment(AppModel.self) private var model

    var body: some View {
        @Bindable var model = model

        TabView(selection: $model.selectedTab) {
            TodayView()
                .tabItem { Label("오늘", systemImage: "text.book.closed") }
                .tag(AppModel.Tab.today)

            SavedWordsView()
                .tabItem { Label("내 단어장", systemImage: "bookmark") }
                .tag(AppModel.Tab.saved)

            SettingsView()
                .tabItem { Label("설정", systemImage: "gearshape") }
                .tag(AppModel.Tab.settings)
        }
    }
}
