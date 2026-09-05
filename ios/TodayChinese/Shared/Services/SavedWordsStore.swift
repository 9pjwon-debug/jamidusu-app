import Foundation
import Observation

/// 내 단어장. 저장한 단어의 id 를 App Group 에 순서대로 보관한다.
@Observable
final class SavedWordsStore {
    static let shared = SavedWordsStore()

    private let defaults: UserDefaults
    private(set) var ids: [Int]

    init(defaults: UserDefaults = AppGroup.defaults) {
        self.defaults = defaults
        self.ids = (defaults.array(forKey: DefaultsKey.savedWordIDs) as? [Int]) ?? []
    }

    var words: [ChineseWord] {
        // 최근에 저장한 단어가 위로 오도록 뒤집는다.
        WordRepository.shared.words(ids: ids.reversed())
    }

    var count: Int { ids.count }

    func contains(_ word: ChineseWord) -> Bool {
        ids.contains(word.id)
    }

    func toggle(_ word: ChineseWord) {
        if ids.contains(word.id) {
            remove(word)
        } else {
            add(word)
        }
    }

    func add(_ word: ChineseWord) {
        guard !ids.contains(word.id) else { return }
        ids.append(word.id)
        persist()
    }

    func remove(_ word: ChineseWord) {
        guard let index = ids.firstIndex(of: word.id) else { return }
        ids.remove(at: index)
        persist()
    }

    func removeAll() {
        guard !ids.isEmpty else { return }
        ids.removeAll()
        persist()
    }

    private func persist() {
        defaults.set(ids, forKey: DefaultsKey.savedWordIDs)
    }
}

/// 최근에 본 단어 기록. 오늘의 단어 선택은 결정적 셔플로 중복을 막고,
/// 이 기록은 "지난 단어 다시 보기" 용도로만 쓴다.
enum WordHistoryStore {
    static let limit = 60

    static func record(_ word: ChineseWord, defaults: UserDefaults = AppGroup.defaults) {
        var ids = (defaults.array(forKey: DefaultsKey.historyWordIDs) as? [Int]) ?? []
        guard ids.last != word.id else { return }
        ids.removeAll { $0 == word.id }
        ids.append(word.id)
        if ids.count > limit { ids.removeFirst(ids.count - limit) }
        defaults.set(ids, forKey: DefaultsKey.historyWordIDs)
    }

    static func recent(defaults: UserDefaults = AppGroup.defaults) -> [ChineseWord] {
        let ids = (defaults.array(forKey: DefaultsKey.historyWordIDs) as? [Int]) ?? []
        return WordRepository.shared.words(ids: ids.reversed())
    }

    static func clear(defaults: UserDefaults = AppGroup.defaults) {
        defaults.removeObject(forKey: DefaultsKey.historyWordIDs)
    }
}
