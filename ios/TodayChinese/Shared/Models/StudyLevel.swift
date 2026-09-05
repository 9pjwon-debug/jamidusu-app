import Foundation

/// 온보딩과 설정에서 고르는 학습 난이도.
/// rawValue 는 `words.json` 의 `level` 값과 정확히 일치해야 한다.
enum StudyLevel: String, CaseIterable, Codable, Identifiable, Sendable {
    case hsk1 = "HSK 1"
    case hsk2 = "HSK 2"
    case hsk3 = "HSK 3"
    case hsk4 = "HSK 4"
    case hsk5 = "HSK 5"
    case hsk6 = "HSK 6"
    case conversation = "실전 회화"

    var id: String { rawValue }

    var title: String { rawValue }

    var subtitle: String {
        switch self {
        case .hsk1: return "가장 기본이 되는 단어"
        case .hsk2: return "일상에서 매일 쓰는 표현"
        case .hsk3: return "생활 회화의 중심"
        case .hsk4: return "생각과 의견을 말하는 단어"
        case .hsk5: return "뉘앙스가 살아 있는 표현"
        case .hsk6: return "글과 대화를 다듬는 어휘"
        case .conversation: return "중국인이 실제로 쓰는 말"
        }
    }

    /// 사용자가 아무것도 고르지 않았을 때의 기본값.
    static let defaultSelection: Set<StudyLevel> = [.hsk1, .hsk2, .hsk3]

    /// "랜덤" 은 별도 케이스가 아니라 "전부 선택" 으로 다룬다.
    static var all: Set<StudyLevel> { Set(allCases) }
}
