import SwiftUI

@main
struct TodayChineseApp: App {
    @State private var model = AppModel()
    @State private var savedWords = SavedWordsStore.shared
    @Environment(\.scenePhase) private var scenePhase

    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(model)
                .environment(savedWords)
                .tint(Theme.ink)
                .onOpenURL { url in
                    model.handle(url: url)
                }
                .onChange(of: scenePhase) { _, phase in
                    guard phase == .active else { return }
                    model.refreshIfNeeded()
                    model.reloadWidgets()
                }
        }
    }
}
