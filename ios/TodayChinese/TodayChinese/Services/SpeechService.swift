import AVFoundation
import Observation

/// 중국어 발음 재생. MVP 이므로 서버 TTS 없이 AVSpeechSynthesizer 만 쓴다.
@Observable
final class SpeechService: NSObject, AVSpeechSynthesizerDelegate {
    static let shared = SpeechService()

    private let synthesizer = AVSpeechSynthesizer()
    private(set) var isSpeaking = false

    override private init() {
        super.init()
        synthesizer.delegate = self
    }

    /// 단어를 읽고, 잠깐 쉬었다가 예문을 읽는다.
    func speak(_ word: ChineseWord) {
        stop()
        activateSession()
        synthesizer.speak(utterance(for: word.word, rate: 0.40))
        synthesizer.speak(utterance(for: word.example, rate: 0.44, delay: 0.45))
    }

    func speakWordOnly(_ text: String) {
        stop()
        activateSession()
        synthesizer.speak(utterance(for: text, rate: 0.40))
    }

    func stop() {
        guard synthesizer.isSpeaking else { return }
        synthesizer.stopSpeaking(at: .immediate)
    }

    private func utterance(for text: String, rate: Float, delay: TimeInterval = 0) -> AVSpeechUtterance {
        let utterance = AVSpeechUtterance(string: text)
        utterance.voice = Self.chineseVoice
        utterance.rate = rate
        utterance.pitchMultiplier = 1.0
        utterance.preUtteranceDelay = delay
        utterance.postUtteranceDelay = 0.1
        return utterance
    }

    /// zh-CN 음성이 없는 기기에서는 사용 가능한 중국어 음성으로 폴백한다.
    private static let chineseVoice: AVSpeechSynthesisVoice? = {
        if let voice = AVSpeechSynthesisVoice(language: "zh-CN") { return voice }
        return AVSpeechSynthesisVoice.speechVoices().first { $0.language.hasPrefix("zh") }
    }()

    private func activateSession() {
        #if os(iOS)
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.playback, mode: .spokenAudio, options: [.duckOthers])
        try? session.setActive(true, options: [])
        #endif
    }

    private func deactivateSession() {
        #if os(iOS)
        try? AVAudioSession.sharedInstance().setActive(false, options: [.notifyOthersOnDeactivation])
        #endif
    }

    // MARK: - AVSpeechSynthesizerDelegate

    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didStart utterance: AVSpeechUtterance) {
        isSpeaking = true
    }

    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        guard !synthesizer.isSpeaking else { return }
        isSpeaking = false
        deactivateSession()
    }

    func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didCancel utterance: AVSpeechUtterance) {
        isSpeaking = false
        deactivateSession()
    }
}
