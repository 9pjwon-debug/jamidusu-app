import SwiftUI

struct SavedWordsView: View {
    @Environment(SavedWordsStore.self) private var savedWords

    var body: some View {
        NavigationStack {
            ZStack {
                Theme.background.ignoresSafeArea()

                if savedWords.count == 0 {
                    EmptyStateView(
                        title: "아직 저장한 단어가 없어요",
                        message: "오늘의 단어에서 ♡ 를 누르면 여기에 모여요."
                    )
                } else {
                    List {
                        Section {
                            ForEach(savedWords.words) { word in
                                NavigationLink {
                                    WordDetailView(word: word)
                                } label: {
                                    WordRow(word: word)
                                }
                                .listRowBackground(Theme.card)
                            }
                            .onDelete(perform: delete)
                        } header: {
                            Text("我的单词")
                                .font(.system(size: 15, weight: .medium))
                                .foregroundStyle(Theme.secondary)
                                .textCase(nil)
                        }
                    }
                    .listStyle(.insetGrouped)
                    .scrollContentBackground(.hidden)
                }
            }
            .navigationTitle("내 단어장")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                if savedWords.count > 0 {
                    ToolbarItem(placement: .topBarTrailing) { EditButton() }
                }
            }
        }
    }

    private func delete(at offsets: IndexSet) {
        let words = savedWords.words
        for index in offsets where words.indices.contains(index) {
            savedWords.remove(words[index])
        }
    }
}
