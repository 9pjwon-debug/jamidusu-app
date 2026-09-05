import Foundation

/// 하나의 중국어 단어와 예문. `words.json` 의 한 항목과 1:1로 대응한다.
struct ChineseWord: Codable, Identifiable, Hashable, Sendable {
    let id: Int
    let word: String
    let pinyin: String
    let meaning: String
    let example: String
    let examplePinyin: String
    let translation: String
    let level: String
    let category: String
}

extension ChineseWord {
    /// 원형 위젯처럼 공간이 극단적으로 좁은 곳에서 쓰는 축약형.
    /// 한자가 3자를 넘으면 앞의 2자만 보여준다. (`真的假的？` -> `真的`)
    var compactWord: String {
        let cjk: ClosedRange<UInt32> = 0x4E00...0x9FFF
        let hanzi = word.filter { character in
            character.unicodeScalars.contains { cjk.contains($0.value) }
        }
        let base = hanzi.isEmpty ? word : hanzi
        return base.count > 3 ? String(base.prefix(2)) : base
    }

    /// 인라인 위젯 등에서 쓰는 아주 짧은 뜻.
    var shortMeaning: String {
        guard let first = meaning.split(separator: ",").first else { return meaning }
        let trimmed = first.trimmingCharacters(in: .whitespaces)
        return trimmed.count > 8 ? String(trimmed.prefix(8)) : trimmed
    }

    static let placeholder = ChineseWord(
        id: 1,
        word: "坚持",
        pinyin: "jiānchí",
        meaning: "꾸준히 하다",
        example: "坚持学习中文。",
        examplePinyin: "Jiānchí xuéxí Zhōngwén.",
        translation: "중국어 공부를 꾸준히 하다.",
        level: "HSK 3",
        category: "일상"
    )
}
