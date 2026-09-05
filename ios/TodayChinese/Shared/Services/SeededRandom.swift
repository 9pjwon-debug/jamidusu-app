import Foundation

/// SplitMix64. 시드가 같으면 플랫폼과 무관하게 항상 같은 수열을 만든다.
/// 앱과 위젯이 "오늘의 단어"를 각자 계산해도 결과가 같아야 하므로
/// 표준 라이브러리의 난수 대신 이 구현을 쓴다.
struct SeededRandom: RandomNumberGenerator {
    private var state: UInt64

    init(seed: UInt64) {
        state = seed
    }

    mutating func next() -> UInt64 {
        state &+= 0x9E37_79B9_7F4A_7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58_476D_1CE4_E5B9
        z = (z ^ (z >> 27)) &* 0x94D0_49BB_1331_11EB
        return z ^ (z >> 31)
    }
}

extension Array {
    /// Fisher-Yates. `shuffle(using:)` 은 표준 라이브러리 구현에 의존하므로
    /// 결과를 완전히 고정하기 위해 직접 구현한다.
    func seededShuffled(seed: UInt64) -> [Element] {
        guard count > 1 else { return self }
        var result = self
        var rng = SeededRandom(seed: seed)
        for i in stride(from: result.count - 1, to: 0, by: -1) {
            let j = Int(rng.next() % UInt64(i + 1))
            result.swapAt(i, j)
        }
        return result
    }
}
