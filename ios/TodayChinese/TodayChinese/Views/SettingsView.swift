import SwiftUI

struct SettingsView: View {
    @Environment(AppModel.self) private var model
    @Environment(SavedWordsStore.self) private var savedWords

    @State private var notificationsOn = false
    @State private var notificationTime = Date()
    @State private var showsPermissionAlert = false
    @State private var isApplyingNotification = false

    private let repository = WordRepository.shared

    var body: some View {
        NavigationStack {
            Form {
                levelSection
                categorySection
                notificationSection
                streakSection
                infoSection
            }
            .scrollContentBackground(.hidden)
            .background(Theme.background.ignoresSafeArea())
            .navigationTitle("설정")
            .alert("알림 권한이 필요해요", isPresented: $showsPermissionAlert) {
                Button("확인", role: .cancel) {}
            } message: {
                Text("설정 앱 > 오늘의 중국어 > 알림에서 허용해 주세요.")
            }
        }
        .onAppear(perform: syncFromModel)
    }

    // MARK: - 난이도

    private var levelSection: some View {
        Section {
            ForEach(StudyLevel.allCases) { level in
                Button {
                    toggle(level)
                } label: {
                    HStack {
                        VStack(alignment: .leading, spacing: 2) {
                            Text(level.title)
                                .foregroundStyle(Theme.ink)
                            Text("\(level.subtitle) · \(repository.count(for: level))개")
                                .font(.system(size: 12))
                                .foregroundStyle(Theme.tertiary)
                        }
                        Spacer()
                        if model.settings.levels.contains(level) {
                            Image(systemName: "checkmark")
                                .font(.system(size: 14, weight: .semibold))
                                .foregroundStyle(Theme.ink)
                        }
                    }
                }
            }

            Button("랜덤 (전체에서 고르기)") {
                model.updateLevels(StudyLevel.all)
            }
            .foregroundStyle(Theme.secondary)
        } header: {
            Text("난이도")
        } footer: {
            Text("여러 개를 고를 수 있어요. 하나도 고르지 않으면 기본값으로 돌아갑니다.")
        }
    }

    private func toggle(_ level: StudyLevel) {
        var levels = model.settings.levels
        if levels.contains(level) {
            levels.remove(level)
        } else {
            levels.insert(level)
        }
        model.updateLevels(levels)
    }

    // MARK: - 카테고리

    private var categorySection: some View {
        Section {
            NavigationLink {
                CategorySelectionView()
            } label: {
                HStack {
                    Text("카테고리")
                    Spacer()
                    Text(model.settings.categories.isEmpty ? "전체" : "\(model.settings.categories.count)개 선택")
                        .foregroundStyle(Theme.tertiary)
                }
            }
        }
    }

    // MARK: - 알림

    private var notificationSection: some View {
        Section {
            Toggle("하루 한 번 알림", isOn: Binding(
                get: { notificationsOn },
                set: { newValue in
                    // 스위치가 즉시 따라오도록 먼저 반영하고,
                    // 권한이 거부되면 setNotifications 에서 되돌린다.
                    notificationsOn = newValue
                    Task { await setNotifications(enabled: newValue) }
                }
            ))
            .disabled(isApplyingNotification)

            if notificationsOn {
                DatePicker(
                    "알림 시간",
                    selection: $notificationTime,
                    displayedComponents: .hourAndMinute
                )
                .onChange(of: notificationTime) { _, _ in
                    Task { await applyScheduledTime() }
                }
            }
        } header: {
            Text("알림")
        } footer: {
            Text("켤 때만 권한을 요청해요. 기본 시간은 오전 8시입니다.")
        }
    }

    @MainActor
    private func setNotifications(enabled: Bool) async {
        isApplyingNotification = true
        defer { isApplyingNotification = false }

        guard enabled else {
            NotificationService.cancel()
            notificationsOn = false
            persistNotificationSettings(enabled: false)
            return
        }

        let status = await NotificationService.authorizationStatus()
        let granted: Bool
        switch status {
        case .notDetermined:
            granted = await NotificationService.requestAuthorization()
        case .denied:
            granted = false
        default:
            granted = true
        }

        guard granted else {
            notificationsOn = false
            persistNotificationSettings(enabled: false)
            showsPermissionAlert = true
            return
        }

        notificationsOn = true
        await applyScheduledTime()
    }

    @MainActor
    private func applyScheduledTime() async {
        let components = Calendar.current.dateComponents([.hour, .minute], from: notificationTime)
        let hour = components.hour ?? 8
        let minute = components.minute ?? 0
        persistNotificationSettings(enabled: notificationsOn)
        guard notificationsOn else { return }
        await NotificationService.schedule(hour: hour, minute: minute)
    }

    private func persistNotificationSettings(enabled: Bool) {
        let components = Calendar.current.dateComponents([.hour, .minute], from: notificationTime)
        model.updateNotification(
            enabled: enabled,
            hour: components.hour ?? 8,
            minute: components.minute ?? 0
        )
    }

    // MARK: - Streak / 정보

    private var streakSection: some View {
        Section("연속 학습") {
            HStack {
                Text("현재")
                Spacer()
                Text(model.streak > 0 ? "\(model.streak)일" : "아직 없음")
                    .foregroundStyle(Theme.tertiary)
            }
            HStack {
                Text("저장한 단어")
                Spacer()
                Text("\(savedWords.count)개")
                    .foregroundStyle(Theme.tertiary)
            }
        }
    }

    private var infoSection: some View {
        Section {
            HStack {
                Text("단어 수")
                Spacer()
                Text("\(repository.allWords.count)개")
                    .foregroundStyle(Theme.tertiary)
            }
            HStack {
                Text("버전")
                Spacer()
                Text(Self.appVersion)
                    .foregroundStyle(Theme.tertiary)
            }
            if !AppGroup.isSharedStoreAvailable {
                VStack(alignment: .leading, spacing: 4) {
                    Text("App Group 이 연결되지 않았어요")
                        .font(.system(size: 13, weight: .medium))
                    Text("위젯이 앱 설정을 읽지 못해 기본 난이도(HSK 1~3)로 표시됩니다. "
                         + "무료 Apple ID 로 설치한 경우 정상입니다.")
                        .font(.system(size: 12))
                        .foregroundStyle(Theme.secondary)
                }
                .padding(.vertical, 2)
            }
        } header: {
            Text("앱 정보")
        } footer: {
            Text("잠금화면을 길게 누르고 '사용자화' → 위젯 추가에서 오늘의 중국어를 선택하세요.")
        }
    }

    private static var appVersion: String {
        let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
        return version
    }

    // MARK: - 동기화

    private func syncFromModel() {
        notificationsOn = model.settings.notificationsEnabled
        let calendar = Calendar.current
        var components = calendar.dateComponents([.year, .month, .day], from: Date())
        components.hour = model.settings.notificationHour
        components.minute = model.settings.notificationMinute
        notificationTime = calendar.date(from: components) ?? Date()
    }
}

/// 카테고리 다중 선택. 아무것도 고르지 않으면 전체가 대상이 된다.
struct CategorySelectionView: View {
    @Environment(AppModel.self) private var model
    private let categories = WordRepository.shared.allCategories

    var body: some View {
        List {
            Section {
                Button("전체") {
                    model.updateCategories([])
                }
                .foregroundStyle(model.settings.categories.isEmpty ? Theme.ink : Theme.secondary)
            }

            Section {
                ForEach(categories, id: \.self) { category in
                    Button {
                        toggle(category)
                    } label: {
                        HStack {
                            Text(category).foregroundStyle(Theme.ink)
                            Spacer()
                            if model.settings.categories.contains(category) {
                                Image(systemName: "checkmark")
                                    .font(.system(size: 14, weight: .semibold))
                                    .foregroundStyle(Theme.ink)
                            }
                        }
                    }
                }
            } footer: {
                Text("선택한 카테고리에 단어가 없으면 자동으로 전체에서 고릅니다.")
            }
        }
        .scrollContentBackground(.hidden)
        .background(Theme.background.ignoresSafeArea())
        .navigationTitle("카테고리")
        .navigationBarTitleDisplayMode(.inline)
    }

    private func toggle(_ category: String) {
        var categories = model.settings.categories
        if categories.contains(category) {
            categories.remove(category)
        } else {
            categories.insert(category)
        }
        model.updateCategories(categories)
    }
}
