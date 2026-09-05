import SwiftUI

struct OnboardingView: View {
    @Environment(AppModel.self) private var model

    @State private var step = 0
    @State private var levels: Set<StudyLevel> = StudyLevel.defaultSelection

    var body: some View {
        ZStack {
            Theme.background.ignoresSafeArea()

            Group {
                if step == 0 {
                    welcome
                        .transition(.opacity.combined(with: .move(edge: .leading)))
                } else {
                    levelPicker
                        .transition(.opacity.combined(with: .move(edge: .trailing)))
                }
            }
            .animation(.easeInOut(duration: 0.28), value: step)
        }
    }

    // MARK: - 1단계

    private var welcome: some View {
        VStack(spacing: 0) {
            Spacer()

            Text("🇨🇳")
                .font(.system(size: 56))

            Text("오늘의 중국어")
                .font(.system(size: 28, weight: .semibold))
                .foregroundStyle(Theme.ink)
                .padding(.top, 20)

            Text("잠금화면에서\n하루 한 단어.")
                .font(.system(size: 17))
                .foregroundStyle(Theme.secondary)
                .multilineTextAlignment(.center)
                .lineSpacing(4)
                .padding(.top, 10)

            Spacer()

            Button("시작하기") { step = 1 }
                .buttonStyle(PillButtonStyle(kind: .filled))
                .padding(.horizontal, 32)
                .padding(.bottom, 40)
        }
    }

    // MARK: - 2단계

    private var levelPicker: some View {
        VStack(spacing: 0) {
            VStack(spacing: 8) {
                Text("어떤 중국어를 공부할까요?")
                    .font(.system(size: 22, weight: .semibold))
                    .foregroundStyle(Theme.ink)
                Text("여러 개를 골라도 좋아요. 나중에 설정에서 바꿀 수 있어요.")
                    .font(.system(size: 14))
                    .foregroundStyle(Theme.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding(.top, 60)
            .padding(.horizontal, 28)

            ScrollView {
                LazyVGrid(columns: [GridItem(.flexible(), spacing: 12), GridItem(.flexible(), spacing: 12)], spacing: 12) {
                    ForEach(StudyLevel.allCases) { level in
                        optionCard(
                            title: level.title,
                            subtitle: level.subtitle,
                            isSelected: levels.contains(level)
                        ) {
                            if levels.contains(level) { levels.remove(level) } else { levels.insert(level) }
                        }
                    }

                    optionCard(
                        title: "랜덤",
                        subtitle: "전체에서 고르기",
                        isSelected: levels == StudyLevel.all
                    ) {
                        levels = levels == StudyLevel.all ? StudyLevel.defaultSelection : StudyLevel.all
                    }
                }
                .padding(.horizontal, 24)
                .padding(.top, 28)
                .padding(.bottom, 12)
            }
            .scrollIndicators(.hidden)

            Button("완료") {
                model.completeOnboarding(levels: levels)
            }
            .buttonStyle(PillButtonStyle(kind: .filled))
            .disabled(levels.isEmpty)
            .opacity(levels.isEmpty ? 0.4 : 1)
            .padding(.horizontal, 32)
            .padding(.bottom, 40)
        }
    }

    private func optionCard(
        title: String,
        subtitle: String,
        isSelected: Bool,
        action: @escaping () -> Void
    ) -> some View {
        Button(action: action) {
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundStyle(Theme.ink)
                Text(subtitle)
                    .font(.system(size: 12))
                    .foregroundStyle(Theme.secondary)
                    .lineLimit(2)
                    .multilineTextAlignment(.leading)
            }
            .frame(maxWidth: .infinity, minHeight: 62, alignment: .leading)
            .padding(14)
            .background(
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .fill(Theme.card)
            )
            .overlay(
                RoundedRectangle(cornerRadius: 16, style: .continuous)
                    .stroke(isSelected ? Theme.ink : Theme.hairline, lineWidth: isSelected ? 1.6 : 1)
            )
        }
        .buttonStyle(.plain)
        .animation(.easeOut(duration: 0.16), value: isSelected)
    }
}

#Preview {
    OnboardingView().environment(AppModel())
}
