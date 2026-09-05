import SwiftUI
import UIKit

/// 앱 전체의 색과 여백. 아주 연한 아이보리 배경 + 잉크빛 텍스트.
/// 중국풍 장식이나 빨강/금색은 쓰지 않는다.
enum Theme {
    static let background = Color(uiColor: UIColor { trait in
        trait.userInterfaceStyle == .dark
            ? UIColor(red: 0.07, green: 0.07, blue: 0.075, alpha: 1)
            : UIColor(red: 0.985, green: 0.981, blue: 0.972, alpha: 1)
    })

    static let card = Color(uiColor: UIColor { trait in
        trait.userInterfaceStyle == .dark
            ? UIColor(red: 0.125, green: 0.125, blue: 0.132, alpha: 1)
            : UIColor.white
    })

    static let ink = Color(uiColor: UIColor { trait in
        trait.userInterfaceStyle == .dark
            ? UIColor(white: 0.96, alpha: 1)
            : UIColor(red: 0.11, green: 0.11, blue: 0.12, alpha: 1)
    })

    static let secondary = Color(uiColor: UIColor { trait in
        trait.userInterfaceStyle == .dark
            ? UIColor(white: 0.68, alpha: 1)
            : UIColor(red: 0.42, green: 0.42, blue: 0.44, alpha: 1)
    })

    static let tertiary = Color(uiColor: UIColor { trait in
        trait.userInterfaceStyle == .dark
            ? UIColor(white: 0.48, alpha: 1)
            : UIColor(red: 0.62, green: 0.62, blue: 0.64, alpha: 1)
    })

    static let hairline = Color(uiColor: UIColor { trait in
        trait.userInterfaceStyle == .dark
            ? UIColor(white: 1, alpha: 0.10)
            : UIColor(red: 0, green: 0, blue: 0, alpha: 0.06)
    })

    static let cardRadius: CGFloat = 20
    static let pagePadding: CGFloat = 20
}

/// 둥근 카드 한 장. 그림자는 아주 옅게만 준다.
struct CardBackground: ViewModifier {
    var padding: CGFloat = 22

    func body(content: Content) -> some View {
        content
            .padding(padding)
            .frame(maxWidth: .infinity)
            .background(
                RoundedRectangle(cornerRadius: Theme.cardRadius, style: .continuous)
                    .fill(Theme.card)
            )
            .overlay(
                RoundedRectangle(cornerRadius: Theme.cardRadius, style: .continuous)
                    .stroke(Theme.hairline, lineWidth: 1)
            )
            .shadow(color: .black.opacity(0.04), radius: 12, x: 0, y: 4)
    }
}

extension View {
    func cardStyle(padding: CGFloat = 22) -> some View {
        modifier(CardBackground(padding: padding))
    }
}
