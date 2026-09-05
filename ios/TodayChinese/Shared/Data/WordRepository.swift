import Foundation

/// 번들에 들어 있는 `words.json` 을 읽어 두는 저장소.
/// 앱 번들과 위젯 익스텐션 번들 각각에 `words.json` 이 복사되므로
/// 양쪽 모두 `Bundle.main` 으로 접근할 수 있다.
struct WordRepository: Sendable {
    static let shared = WordRepository()

    let allWords: [ChineseWord]

    init(words: [ChineseWord]? = nil) {
        allWords = words ?? Self.loadBundledWords()
    }

    private static func loadBundledWords() -> [ChineseWord] {
        guard let url = Bundle.main.url(forResource: "words", withExtension: "json") else {
            assertionFailure("words.json 이 번들에 없습니다. Target Membership 을 확인하세요.")
            return [.placeholder]
        }
        do {
            let data = try Data(contentsOf: url)
            let decoded = try JSONDecoder().decode([ChineseWord].self, from: data)
            return decoded.isEmpty ? [.placeholder] : decoded
        } catch {
            assertionFailure("words.json 디코딩 실패: \(error)")
            return [.placeholder]
        }
    }

    /// 난이도와 카테고리로 거른 목록. 조건에 맞는 단어가 하나도 없으면
    /// 빈 화면 대신 전체 목록으로 폴백한다.
    func words(levels: Set<StudyLevel>, categories: Set<String> = []) -> [ChineseWord] {
        let levelValues = Set(levels.map(\.rawValue))
        var filtered = levelValues.isEmpty ? allWords : allWords.filter { levelValues.contains($0.level) }
        if !categories.isEmpty {
            let byCategory = filtered.filter { categories.contains($0.category) }
            if !byCategory.isEmpty { filtered = byCategory }
        }
        return filtered.isEmpty ? allWords : filtered
    }

    func word(id: Int) -> ChineseWord? {
        allWords.first { $0.id == id }
    }

    func words(ids: [Int]) -> [ChineseWord] {
        ids.compactMap(word(id:))
    }

    var allCategories: [String] {
        Array(Set(allWords.map(\.category))).sorted()
    }

    func count(for level: StudyLevel) -> Int {
        allWords.filter { $0.level == level.rawValue }.count
    }
}
