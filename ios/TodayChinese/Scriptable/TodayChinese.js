// Variables used by Scriptable.
// These must be at the very top of the file. Do not edit.
// icon-color: gray; icon-glyph: language;
//
// ─────────────────────────────────────────────────────────────
//  오늘의 중국어 — 잠금화면에서 하루 한 단어
//
//  쓰는 법
//   1. 이 파일 전체를 복사해 Scriptable 에서 새 스크립트로 붙여넣는다.
//   2. 스크립트 이름을 "오늘의 중국어" 로 바꾼다.
//   3. 잠금화면 길게 누르기 → 사용자화 → 잠금화면 → 위젯 추가 → Scriptable
//   4. 위젯을 탭해서 Script 를 "오늘의 중국어" 로 지정한다.
//   5. Parameter 칸에 난이도를 적으면 그 난이도만 나온다. (비우면 기본값)
//        예) HSK 3
//        예) HSK 1, HSK 2, 실전 회화
//        예) 전체
//
//  이 파일은 자동 생성된다. 단어를 고치려면
//  ios/TodayChinese/Shared/Data/words.json 을 고치고
//  python Tools/gen_scriptable.py 를 다시 돌린다.
// ─────────────────────────────────────────────────────────────

// 위젯 Parameter 가 비어 있을 때 쓰는 난이도.
const DEFAULT_LEVELS = ["HSK 1", "HSK 2", "HSK 3"]

// 고를 수 있는 난이도: HSK 1, HSK 2, HSK 3, HSK 4, HSK 5, HSK 6, 실전 회화

// 단어 122개. 이미 섞인 순서로 고정되어 있다.
// (난이도로 걸러내도 "연속 N일 안에 중복 없음" 이 유지된다)
const WORDS = [
  {w:"幸亏",p:"xìngkuī",m:"다행히",e:"幸亏你提醒我了。",ep:"Xìngkuī nǐ tíxǐng wǒ le.",t:"다행히 네가 알려줬어.",l:"HSK 5",c:"표현"},
  {w:"完成",p:"wánchéng",m:"끝내다, 완성하다",e:"这个项目下周完成。",ep:"Zhège xiàngmù xià zhōu wánchéng.",t:"이 프로젝트는 다음 주에 끝나요.",l:"HSK 3",c:"일"},
  {w:"突然",p:"tūrán",m:"갑자기",e:"他突然打电话给我。",ep:"Tā tūrán dǎ diànhuà gěi wǒ.",t:"그가 갑자기 전화했어요.",l:"HSK 3",c:"표현"},
  {w:"重要",p:"zhòngyào",m:"중요하다",e:"健康比什么都重要。",ep:"Jiànkāng bǐ shénme dōu zhòngyào.",t:"건강이 무엇보다 중요해요.",l:"HSK 4",c:"일상"},
  {w:"一起",p:"yìqǐ",m:"함께",e:"我们一起去吧。",ep:"Wǒmen yìqǐ qù ba.",t:"우리 같이 가요.",l:"HSK 2",c:"관계"},
  {w:"多少",p:"duōshao",m:"얼마, 몇",e:"这个多少钱？",ep:"Zhège duōshao qián?",t:"이거 얼마예요?",l:"HSK 1",c:"쇼핑"},
  {w:"真的假的",p:"zhēn de jiǎ de",m:"진짜야?",e:"真的假的？我不敢相信。",ep:"Zhēn de jiǎ de? Wǒ bù gǎn xiāngxìn.",t:"진짜야? 못 믿겠어.",l:"실전 회화",c:"회화"},
  {w:"一定",p:"yídìng",m:"반드시",e:"你一定可以做到。",ep:"Nǐ yídìng kěyǐ zuòdào.",t:"너는 반드시 해낼 수 있어.",l:"HSK 2",c:"감정"},
  {w:"推迟",p:"tuīchí",m:"미루다",e:"会议推迟到明天了。",ep:"Huìyì tuīchí dào míngtiān le.",t:"회의가 내일로 미뤄졌어요.",l:"HSK 4",c:"일"},
  {w:"无论",p:"wúlùn",m:"~에 관계없이",e:"无论多忙，我都会去。",ep:"Wúlùn duō máng, wǒ dōu huì qù.",t:"아무리 바빠도 저는 갈 거예요.",l:"HSK 4",c:"표현"},
  {w:"慢走",p:"màn zǒu",m:"조심히 가세요",e:"慢走，路上小心。",ep:"Màn zǒu, lùshang xiǎoxīn.",t:"조심히 가세요, 길 조심하고요.",l:"실전 회화",c:"회화"},
  {w:"算了",p:"suàn le",m:"됐어, 관두자",e:"算了，下次再说吧。",ep:"Suàn le, xià cì zài shuō ba.",t:"됐어, 다음에 얘기하자.",l:"실전 회화",c:"회화"},
  {w:"准备",p:"zhǔnbèi",m:"준비하다",e:"我在准备考试。",ep:"Wǒ zài zhǔnbèi kǎoshì.",t:"나는 시험을 준비하고 있어요.",l:"HSK 2",c:"학습"},
  {w:"力所能及",p:"lì suǒ néng jí",m:"힘닿는 데까지",e:"我做了力所能及的事。",ep:"Wǒ zuò le lì suǒ néng jí de shì.",t:"나는 할 수 있는 만큼 했다.",l:"HSK 6",c:"표현"},
  {w:"到时候",p:"dào shíhou",m:"그때 가서",e:"到时候再说吧。",ep:"Dào shíhou zài shuō ba.",t:"그때 가서 다시 얘기하자.",l:"실전 회화",c:"회화"},
  {w:"觉得",p:"juéde",m:"~라고 생각하다",e:"我觉得这个主意不错。",ep:"Wǒ juéde zhège zhǔyi búcuò.",t:"이 아이디어 괜찮은 것 같아요.",l:"HSK 2",c:"감정"},
  {w:"遇到",p:"yùdào",m:"마주치다, 겪다",e:"我在路上遇到了老同学。",ep:"Wǒ zài lùshang yùdào le lǎo tóngxué.",t:"길에서 옛 동창을 만났어요.",l:"HSK 3",c:"관계"},
  {w:"喜欢",p:"xǐhuan",m:"좋아하다",e:"我很喜欢喝咖啡。",ep:"Wǒ hěn xǐhuan hē kāfēi.",t:"나는 커피 마시는 걸 좋아해요.",l:"HSK 1",c:"감정"},
  {w:"解决",p:"jiějué",m:"해결하다",e:"这个问题已经解决了。",ep:"Zhège wèntí yǐjīng jiějué le.",t:"이 문제는 이미 해결됐어요.",l:"HSK 3",c:"일"},
  {w:"安静",p:"ānjìng",m:"조용하다",e:"请安静一点儿。",ep:"Qǐng ānjìng yìdiǎnr.",t:"조금만 조용히 해주세요.",l:"HSK 3",c:"일상"},
  {w:"我先走了",p:"wǒ xiān zǒu le",m:"먼저 갈게",e:"时间不早了，我先走了。",ep:"Shíjiān bù zǎo le, wǒ xiān zǒu le.",t:"시간이 늦었네, 먼저 갈게.",l:"실전 회화",c:"회화"},
  {w:"兼顾",p:"jiāngù",m:"두루 챙기다",e:"很难兼顾工作和生活。",ep:"Hěn nán jiāngù gōngzuò hé shēnghuó.",t:"일과 삶을 모두 챙기기는 어렵다.",l:"HSK 6",c:"일"},
  {w:"不好意思",p:"bù hǎoyìsi",m:"미안해요, 실례해요",e:"不好意思，我来晚了。",ep:"Bù hǎoyìsi, wǒ lái wǎn le.",t:"죄송해요, 늦었어요.",l:"실전 회화",c:"회화"},
  {w:"好久不见",p:"hǎojiǔ bú jiàn",m:"오랜만이야",e:"好久不见，最近怎么样？",ep:"Hǎojiǔ bú jiàn, zuìjìn zěnmeyàng?",t:"오랜만이야, 요즘 어때?",l:"실전 회화",c:"회화"},
  {w:"分享",p:"fēnxiǎng",m:"나누다, 공유하다",e:"我想跟你分享一个好消息。",ep:"Wǒ xiǎng gēn nǐ fēnxiǎng yí ge hǎo xiāoxi.",t:"좋은 소식을 나누고 싶어요.",l:"HSK 5",c:"관계"},
  {w:"微妙",p:"wēimiào",m:"미묘하다",e:"他们之间的关系有点微妙。",ep:"Tāmen zhījiān de guānxi yǒudiǎn wēimiào.",t:"그들 사이의 관계는 좀 미묘하다.",l:"HSK 6",c:"관계"},
  {w:"承认",p:"chéngrèn",m:"인정하다",e:"我承认是我错了。",ep:"Wǒ chéngrèn shì wǒ cuò le.",t:"제가 틀렸다는 걸 인정해요.",l:"HSK 5",c:"관계"},
  {w:"责任",p:"zérèn",m:"책임",e:"这是我的责任。",ep:"Zhè shì wǒ de zérèn.",t:"이건 제 책임이에요.",l:"HSK 4",c:"일"},
  {w:"后悔",p:"hòuhuǐ",m:"후회하다",e:"我有点后悔当时的决定。",ep:"Wǒ yǒudiǎn hòuhuǐ dāngshí de juédìng.",t:"그때의 결정을 좀 후회해요.",l:"HSK 4",c:"감정"},
  {w:"天气",p:"tiānqì",m:"날씨",e:"今天天气很好。",ep:"Jīntiān tiānqì hěn hǎo.",t:"오늘 날씨가 좋아요.",l:"HSK 1",c:"일상"},
  {w:"辛苦了",p:"xīnkǔ le",m:"수고했어요",e:"今天辛苦了，早点休息。",ep:"Jīntiān xīnkǔ le, zǎodiǎn xiūxi.",t:"오늘 수고했어요, 일찍 쉬어요.",l:"실전 회화",c:"회화"},
  {w:"循序渐进",p:"xúnxù jiànjìn",m:"차근차근 나아가다",e:"学语言要循序渐进。",ep:"Xué yǔyán yào xúnxù jiànjìn.",t:"언어 공부는 차근차근 해야 한다.",l:"HSK 6",c:"학습"},
  {w:"保持",p:"bǎochí",m:"유지하다",e:"保持好心情很重要。",ep:"Bǎochí hǎo xīnqíng hěn zhòngyào.",t:"좋은 기분을 유지하는 게 중요해요.",l:"HSK 5",c:"감정"},
  {w:"提高",p:"tígāo",m:"향상시키다",e:"我想提高我的口语。",ep:"Wǒ xiǎng tígāo wǒ de kǒuyǔ.",t:"회화 실력을 높이고 싶어요.",l:"HSK 3",c:"학습"},
  {w:"主动",p:"zhǔdòng",m:"자발적이다, 먼저 나서다",e:"他主动帮我解决了问题。",ep:"Tā zhǔdòng bāng wǒ jiějué le wèntí.",t:"그가 먼저 나서서 문제를 해결해 줬어요.",l:"HSK 5",c:"일"},
  {w:"琐碎",p:"suǒsuì",m:"자질구레하다",e:"每天都有很多琐碎的事。",ep:"Měitiān dōu yǒu hěn duō suǒsuì de shì.",t:"매일 자잘한 일이 많다.",l:"HSK 6",c:"일상"},
  {w:"从容",p:"cóngróng",m:"여유롭다, 침착하다",e:"他面对压力依然很从容。",ep:"Tā miànduì yālì yīrán hěn cóngróng.",t:"그는 압박 속에서도 여전히 여유롭다.",l:"HSK 6",c:"감정"},
  {w:"朋友",p:"péngyou",m:"친구",e:"他是我最好的朋友。",ep:"Tā shì wǒ zuì hǎo de péngyou.",t:"그는 나의 가장 친한 친구예요.",l:"HSK 1",c:"관계"},
  {w:"谢谢",p:"xièxie",m:"고맙습니다",e:"谢谢你的帮助。",ep:"Xièxie nǐ de bāngzhù.",t:"도와줘서 고마워요.",l:"HSK 1",c:"인사"},
  {w:"想开点",p:"xiǎng kāi diǎn",m:"마음 편히 가져",e:"想开点，别难过了。",ep:"Xiǎng kāi diǎn, bié nánguò le.",t:"마음 편히 가져, 너무 슬퍼하지 마.",l:"실전 회화",c:"회화"},
  {w:"竟然",p:"jìngrán",m:"뜻밖에도",e:"他竟然一句话都没说。",ep:"Tā jìngrán yí jù huà dōu méi shuō.",t:"그는 뜻밖에도 한 마디도 하지 않았어요.",l:"HSK 5",c:"표현"},
  {w:"相信",p:"xiāngxìn",m:"믿다",e:"我相信你。",ep:"Wǒ xiāngxìn nǐ.",t:"나는 너를 믿어.",l:"HSK 3",c:"감정"},
  {w:"陪伴",p:"péibàn",m:"곁에서 함께하다",e:"谢谢你一直陪伴我。",ep:"Xièxie nǐ yìzhí péibàn wǒ.",t:"늘 곁에 있어 줘서 고마워요.",l:"HSK 5",c:"관계"},
  {w:"打算",p:"dǎsuàn",m:"~할 계획이다",e:"你周末打算做什么？",ep:"Nǐ zhōumò dǎsuàn zuò shénme?",t:"주말에 뭐 할 계획이에요?",l:"HSK 2",c:"일상"},
  {w:"情不自禁",p:"qíng bù zì jīn",m:"저도 모르게",e:"我情不自禁地笑了。",ep:"Wǒ qíng bù zì jīn de xiào le.",t:"나도 모르게 웃음이 났다.",l:"HSK 6",c:"감정"},
  {w:"沟通",p:"gōutōng",m:"소통하다",e:"有问题就好好沟通。",ep:"Yǒu wèntí jiù hǎohāo gōutōng.",t:"문제가 있으면 잘 소통해요.",l:"HSK 5",c:"관계"},
  {w:"顺利",p:"shùnlì",m:"순조롭다",e:"祝你一切顺利。",ep:"Zhù nǐ yíqiè shùnlì.",t:"모든 일이 순조롭길 바랍니다.",l:"HSK 4",c:"인사"},
  {w:"环境",p:"huánjìng",m:"환경",e:"这里的环境很安静。",ep:"Zhèlǐ de huánjìng hěn ānjìng.",t:"이곳은 환경이 아주 조용해요.",l:"HSK 3",c:"일상"},
  {w:"学习",p:"xuéxí",m:"공부하다",e:"我每天学习中文。",ep:"Wǒ měitiān xuéxí Zhōngwén.",t:"나는 매일 중국어를 공부해요.",l:"HSK 1",c:"학습"},
  {w:"机会",p:"jīhuì",m:"기회",e:"别放过这个机会。",ep:"Bié fàngguò zhège jīhuì.",t:"이 기회를 놓치지 마세요.",l:"HSK 3",c:"일"},
  {w:"稳定",p:"wěndìng",m:"안정적이다",e:"他的工作一直很稳定。",ep:"Tā de gōngzuò yìzhí hěn wěndìng.",t:"그의 일은 늘 안정적이에요.",l:"HSK 5",c:"일"},
  {w:"你好",p:"nǐ hǎo",m:"안녕하세요",e:"你好，很高兴认识你。",ep:"Nǐ hǎo, hěn gāoxìng rènshi nǐ.",t:"안녕하세요, 만나서 반가워요.",l:"HSK 1",c:"인사"},
  {w:"太夸张了",p:"tài kuāzhāng le",m:"너무 오버야",e:"你这也太夸张了吧。",ep:"Nǐ zhè yě tài kuāzhāng le ba.",t:"너 이건 좀 너무 오버다.",l:"실전 회화",c:"회화"},
  {w:"温柔",p:"wēnróu",m:"다정하다, 부드럽다",e:"她说话很温柔。",ep:"Tā shuōhuà hěn wēnróu.",t:"그녀는 말투가 다정해요.",l:"HSK 4",c:"감정"},
  {w:"面对",p:"miànduì",m:"마주하다, 직면하다",e:"我们要勇敢面对问题。",ep:"Wǒmen yào yǒnggǎn miànduì wèntí.",t:"우리는 문제를 용감히 마주해야 해요.",l:"HSK 5",c:"감정"},
  {w:"有点儿",p:"yǒudiǎnr",m:"조금, 약간",e:"今天有点儿冷。",ep:"Jīntiān yǒudiǎnr lěng.",t:"오늘 좀 추워요.",l:"HSK 2",c:"표현"},
  {w:"到底",p:"dàodǐ",m:"도대체",e:"你到底想说什么？",ep:"Nǐ dàodǐ xiǎng shuō shénme?",t:"도대체 무슨 말이 하고 싶은 거예요?",l:"HSK 4",c:"회화"},
  {w:"睡觉",p:"shuìjiào",m:"잠을 자다",e:"我每天十一点睡觉。",ep:"Wǒ měitiān shíyī diǎn shuìjiào.",t:"나는 매일 11시에 자요.",l:"HSK 1",c:"일상"},
  {w:"高兴",p:"gāoxìng",m:"기쁘다",e:"听到这个消息我很高兴。",ep:"Tīngdào zhège xiāoxi wǒ hěn gāoxìng.",t:"그 소식을 들으니 정말 기뻐요.",l:"HSK 1",c:"감정"},
  {w:"放心吧",p:"fàngxīn ba",m:"걱정 마",e:"放心吧，交给我。",ep:"Fàngxīn ba, jiāo gěi wǒ.",t:"걱정 마, 나한테 맡겨.",l:"실전 회화",c:"회화"},
  {w:"意外",p:"yìwài",m:"뜻밖이다",e:"这个结果有点意外。",ep:"Zhège jiéguǒ yǒudiǎn yìwài.",t:"이 결과는 좀 뜻밖이에요.",l:"HSK 5",c:"표현"},
  {w:"我请客",p:"wǒ qǐngkè",m:"내가 살게",e:"今天我请客，别客气。",ep:"Jīntiān wǒ qǐngkè, bié kèqi.",t:"오늘은 내가 살게, 사양하지 마.",l:"실전 회화",c:"회화"},
  {w:"工作",p:"gōngzuò",m:"일하다, 일",e:"他在北京工作。",ep:"Tā zài Běijīng gōngzuò.",t:"그는 베이징에서 일해요.",l:"HSK 1",c:"일"},
  {w:"认真",p:"rènzhēn",m:"성실하다, 진지하다",e:"他工作很认真。",ep:"Tā gōngzuò hěn rènzhēn.",t:"그는 일을 아주 성실히 해요.",l:"HSK 3",c:"일"},
  {w:"简单",p:"jiǎndān",m:"간단하다",e:"这个问题没那么简单。",ep:"Zhège wèntí méi nàme jiǎndān.",t:"이 문제는 그렇게 간단하지 않아요.",l:"HSK 3",c:"표현"},
  {w:"有道理",p:"yǒu dàolǐ",m:"일리 있다",e:"你说的很有道理。",ep:"Nǐ shuō de hěn yǒu dàolǐ.",t:"네 말이 아주 일리 있어.",l:"실전 회화",c:"회화"},
  {w:"复杂",p:"fùzá",m:"복잡하다",e:"情况有点复杂。",ep:"Qíngkuàng yǒudiǎn fùzá.",t:"상황이 좀 복잡해요.",l:"HSK 4",c:"표현"},
  {w:"压力",p:"yālì",m:"스트레스, 압박",e:"最近工作压力有点大。",ep:"Zuìjìn gōngzuò yālì yǒudiǎn dà.",t:"요즘 업무 스트레스가 좀 커요.",l:"HSK 4",c:"일"},
  {w:"熟悉",p:"shúxī",m:"익숙하다, 잘 알다",e:"我对这条路很熟悉。",ep:"Wǒ duì zhè tiáo lù hěn shúxī.",t:"이 길은 아주 잘 알아요.",l:"HSK 4",c:"일상"},
  {w:"大概",p:"dàgài",m:"대략, 아마",e:"大概还要半个小时。",ep:"Dàgài hái yào bàn ge xiǎoshí.",t:"대략 30분쯤 더 걸려요.",l:"HSK 4",c:"시간"},
  {w:"反正",p:"fǎnzhèng",m:"어차피",e:"反正时间还早。",ep:"Fǎnzhèng shíjiān hái zǎo.",t:"어차피 시간은 아직 일러요.",l:"HSK 4",c:"회화"},
  {w:"拜托了",p:"bàituō le",m:"부탁해",e:"这件事就拜托你了。",ep:"Zhè jiàn shì jiù bàituō nǐ le.",t:"이 일은 너에게 부탁할게.",l:"실전 회화",c:"회화"},
  {w:"踏实",p:"tāshi",m:"착실하다, 마음이 놓이다",e:"做事踏实的人最可靠。",ep:"Zuòshì tāshi de rén zuì kěkào.",t:"일을 착실히 하는 사람이 가장 믿음직하다.",l:"HSK 6",c:"일"},
  {w:"慢慢",p:"mànmàn",m:"천천히",e:"慢慢来，别着急。",ep:"Mànmàn lái, bié zháojí.",t:"천천히 해요, 조급해하지 말고.",l:"HSK 2",c:"표현"},
  {w:"差不多",p:"chàbuduō",m:"거의 다 됐다, 비슷하다",e:"差不多了，再等五分钟。",ep:"Chàbuduō le, zài děng wǔ fēnzhōng.",t:"거의 다 됐어, 5분만 더 기다려.",l:"실전 회화",c:"회화"},
  {w:"潜移默化",p:"qiányí mòhuà",m:"은연중에 감화되다",e:"环境对人的影响是潜移默化的。",ep:"Huánjìng duì rén de yǐngxiǎng shì qiányí mòhuà de.",t:"환경이 사람에게 주는 영향은 은연중에 스며든다.",l:"HSK 6",c:"표현"},
  {w:"回家",p:"huí jiā",m:"집에 가다",e:"下班以后我就回家。",ep:"Xiàbān yǐhòu wǒ jiù huí jiā.",t:"퇴근한 뒤에 바로 집에 가요.",l:"HSK 1",c:"일상"},
  {w:"关系",p:"guānxi",m:"관계, 사이",e:"他们的关系一直很好。",ep:"Tāmen de guānxi yìzhí hěn hǎo.",t:"그들은 사이가 늘 좋아요.",l:"HSK 3",c:"관계"},
  {w:"及时",p:"jíshí",m:"제때에",e:"谢谢你及时提醒我。",ep:"Xièxie nǐ jíshí tíxǐng wǒ.",t:"제때 알려줘서 고마워요.",l:"HSK 4",c:"관계"},
  {w:"习惯",p:"xíguàn",m:"습관, 익숙해지다",e:"我已经习惯这里的生活了。",ep:"Wǒ yǐjīng xíguàn zhèlǐ de shēnghuó le.",t:"이곳 생활에 이미 익숙해졌어요.",l:"HSK 3",c:"일상"},
  {w:"特别",p:"tèbié",m:"특히, 특별하다",e:"今天特别累。",ep:"Jīntiān tèbié lèi.",t:"오늘 유난히 피곤해요.",l:"HSK 2",c:"표현"},
  {w:"打扰",p:"dǎrǎo",m:"방해하다",e:"不好意思，打扰一下。",ep:"Bù hǎoyìsi, dǎrǎo yíxià.",t:"실례합니다, 잠시만요.",l:"HSK 4",c:"회화"},
  {w:"休息",p:"xiūxi",m:"쉬다",e:"累了就休息一下。",ep:"Lèi le jiù xiūxi yíxià.",t:"피곤하면 좀 쉬어요.",l:"HSK 2",c:"일상"},
  {w:"明天",p:"míngtiān",m:"내일",e:"明天见！",ep:"Míngtiān jiàn!",t:"내일 봐요!",l:"HSK 1",c:"시간"},
  {w:"随时",p:"suíshí",m:"언제든지",e:"有事随时找我。",ep:"Yǒu shì suíshí zhǎo wǒ.",t:"일 있으면 언제든 연락해.",l:"실전 회화",c:"회화"},
  {w:"随便",p:"suíbiàn",m:"아무거나, 마음대로",e:"你决定吧，我随便。",ep:"Nǐ juédìng ba, wǒ suíbiàn.",t:"네가 정해, 난 아무거나 좋아.",l:"실전 회화",c:"회화"},
  {w:"效率",p:"xiàolǜ",m:"효율",e:"今天工作效率特别高。",ep:"Jīntiān gōngzuò xiàolǜ tèbié gāo.",t:"오늘 업무 효율이 유난히 높아요.",l:"HSK 4",c:"일"},
  {w:"加油",p:"jiāyóu",m:"힘내",e:"加油，你可以的！",ep:"Jiāyóu, nǐ kěyǐ de!",t:"힘내, 넌 할 수 있어!",l:"실전 회화",c:"회화"},
  {w:"努力",p:"nǔlì",m:"노력하다",e:"只要努力就有机会。",ep:"Zhǐyào nǔlì jiù yǒu jīhuì.",t:"노력하기만 하면 기회는 있어요.",l:"HSK 3",c:"감정"},
  {w:"缓解",p:"huǎnjiě",m:"완화하다",e:"散步可以缓解压力。",ep:"Sànbù kěyǐ huǎnjiě yālì.",t:"산책은 스트레스를 완화해 줘요.",l:"HSK 5",c:"일상"},
  {w:"其实",p:"qíshí",m:"사실은",e:"其实我也不太清楚。",ep:"Qíshí wǒ yě bú tài qīngchu.",t:"사실 저도 잘 몰라요.",l:"HSK 3",c:"표현"},
  {w:"逐渐",p:"zhújiàn",m:"점차",e:"天气逐渐暖和起来了。",ep:"Tiānqì zhújiàn nuǎnhuo qǐlái le.",t:"날씨가 점차 따뜻해지고 있어요.",l:"HSK 5",c:"시간"},
  {w:"坚持",p:"jiānchí",m:"꾸준히 하다",e:"坚持学习中文。",ep:"Jiānchí xuéxí Zhōngwén.",t:"중국어 공부를 꾸준히 하다.",l:"HSK 3",c:"일상"},
  {w:"无所谓",p:"wúsuǒwèi",m:"상관없어",e:"怎么都行，我无所谓。",ep:"Zěnme dōu xíng, wǒ wúsuǒwèi.",t:"어떻게 해도 좋아, 난 상관없어.",l:"실전 회화",c:"회화"},
  {w:"建议",p:"jiànyì",m:"제안하다, 제안",e:"我建议你早点休息。",ep:"Wǒ jiànyì nǐ zǎodiǎn xiūxi.",t:"일찍 쉬는 게 좋겠어요.",l:"HSK 4",c:"관계"},
  {w:"值得",p:"zhídé",m:"~할 만하다",e:"这部电影很值得看。",ep:"Zhè bù diànyǐng hěn zhídé kàn.",t:"이 영화는 볼 만해요.",l:"HSK 4",c:"감정"},
  {w:"没关系",p:"méi guānxi",m:"괜찮아요",e:"没关系，别放在心上。",ep:"Méi guānxi, bié fàng zài xīn shàng.",t:"괜찮아요, 마음에 두지 마세요.",l:"실전 회화",c:"회화"},
  {w:"坚强",p:"jiānqiáng",m:"강인하다",e:"她比我想象的更坚强。",ep:"Tā bǐ wǒ xiǎngxiàng de gèng jiānqiáng.",t:"그녀는 내 생각보다 더 강인해요.",l:"HSK 5",c:"감정"},
  {w:"满意",p:"mǎnyì",m:"만족하다",e:"我对结果很满意。",ep:"Wǒ duì jiéguǒ hěn mǎnyì.",t:"결과에 아주 만족해요.",l:"HSK 3",c:"감정"},
  {w:"看情况",p:"kàn qíngkuàng",m:"상황 봐서",e:"去不去看情况吧。",ep:"Qù bu qù kàn qíngkuàng ba.",t:"갈지 말지는 상황 봐서 정하자.",l:"실전 회화",c:"회화"},
  {w:"便宜",p:"piányi",m:"싸다",e:"这家店的东西很便宜。",ep:"Zhè jiā diàn de dōngxi hěn piányi.",t:"이 가게 물건은 싸요.",l:"HSK 2",c:"쇼핑"},
  {w:"珍惜",p:"zhēnxī",m:"소중히 여기다",e:"要珍惜眼前的人。",ep:"Yào zhēnxī yǎnqián de rén.",t:"곁에 있는 사람을 소중히 해야 해요.",l:"HSK 5",c:"감정"},
  {w:"日积月累",p:"rì jī yuè lěi",m:"나날이 쌓이다",e:"语感是日积月累形成的。",ep:"Yǔgǎn shì rì jī yuè lěi xíngchéng de.",t:"언어 감각은 나날이 쌓여 만들어진다.",l:"HSK 6",c:"학습"},
  {w:"吃饭",p:"chīfàn",m:"밥을 먹다",e:"你吃饭了吗？",ep:"Nǐ chīfàn le ma?",t:"밥 먹었어요?",l:"HSK 1",c:"음식"},
  {w:"恰好",p:"qiàhǎo",m:"마침",e:"我到的时候他恰好出门了。",ep:"Wǒ dào de shíhou tā qiàhǎo chūmén le.",t:"내가 도착했을 때 그는 마침 나가고 없었다.",l:"HSK 6",c:"표현"},
  {w:"干杯",p:"gānbēi",m:"건배",e:"来，干杯！",ep:"Lái, gānbēi!",t:"자, 건배!",l:"실전 회화",c:"회화"},
  {w:"希望",p:"xīwàng",m:"바라다",e:"希望明天一切顺利。",ep:"Xīwàng míngtiān yíqiè shùnlì.",t:"내일 모든 게 잘 되길 바라요.",l:"HSK 2",c:"감정"},
  {w:"决定",p:"juédìng",m:"결정하다",e:"我决定先休息一天。",ep:"Wǒ juédìng xiān xiūxi yì tiān.",t:"나는 먼저 하루 쉬기로 했어요.",l:"HSK 3",c:"일상"},
  {w:"因为",p:"yīnwèi",m:"~때문에",e:"因为下雨，所以我没出门。",ep:"Yīnwèi xiàyǔ, suǒyǐ wǒ méi chūmén.",t:"비가 와서 나가지 않았어요.",l:"HSK 2",c:"표현"},
  {w:"出发",p:"chūfā",m:"출발하다",e:"我们八点出发。",ep:"Wǒmen bā diǎn chūfā.",t:"우리 8시에 출발해요.",l:"HSK 2",c:"여행"},
  {w:"商量",p:"shāngliang",m:"상의하다",e:"这件事我们再商量一下。",ep:"Zhè jiàn shì wǒmen zài shāngliang yíxià.",t:"이 일은 다시 상의해 봐요.",l:"HSK 4",c:"일"},
  {w:"有点意思",p:"yǒudiǎn yìsi",m:"좀 재미있네",e:"这个游戏还挺有点意思。",ep:"Zhège yóuxì hái tǐng yǒudiǎn yìsi.",t:"이 게임 꽤 재밌네.",l:"실전 회화",c:"회화"},
  {w:"记得",p:"jìde",m:"기억하다",e:"记得带伞。",ep:"Jìde dài sǎn.",t:"우산 챙기는 거 잊지 마요.",l:"HSK 2",c:"일상"},
  {w:"一般",p:"yìbān",m:"보통이다, 그저 그렇다",e:"味道一般，不太特别。",ep:"Wèidào yìbān, bú tài tèbié.",t:"맛은 그냥 그래요, 별로 특별하지 않아요.",l:"HSK 3",c:"표현"},
  {w:"已经",p:"yǐjīng",m:"이미, 벌써",e:"我已经到公司了。",ep:"Wǒ yǐjīng dào gōngsī le.",t:"저 벌써 회사에 도착했어요.",l:"HSK 2",c:"시간"},
  {w:"尽量",p:"jǐnliàng",m:"가능한 한",e:"我尽量早点到。",ep:"Wǒ jǐnliàng zǎodiǎn dào.",t:"되도록 일찍 도착할게요.",l:"HSK 4",c:"표현"},
  {w:"帮忙",p:"bāngmáng",m:"돕다",e:"能帮我一个忙吗？",ep:"Néng bāng wǒ yí ge máng ma?",t:"저 좀 도와줄 수 있어요?",l:"HSK 2",c:"관계"},
  {w:"坚定",p:"jiāndìng",m:"확고하다",e:"他的态度非常坚定。",ep:"Tā de tàidu fēicháng jiāndìng.",t:"그의 태도는 아주 확고하다.",l:"HSK 6",c:"감정"},
  {w:"犹豫",p:"yóuyù",m:"망설이다",e:"别犹豫了，快决定吧。",ep:"Bié yóuyù le, kuài juédìng ba.",t:"망설이지 말고 빨리 결정해요.",l:"HSK 5",c:"표현"},
  {w:"着急",p:"zháojí",m:"조급해하다",e:"别着急，还有时间。",ep:"Bié zháojí, hái yǒu shíjiān.",t:"조급해하지 마요, 아직 시간 있어요.",l:"HSK 3",c:"감정"},
  {w:"说不定",p:"shuōbudìng",m:"어쩌면",e:"说不定他已经走了。",ep:"Shuōbudìng tā yǐjīng zǒu le.",t:"어쩌면 그는 벌써 갔을지도 몰라.",l:"실전 회화",c:"회화"},
  {w:"时间",p:"shíjiān",m:"시간",e:"我今天没有时间。",ep:"Wǒ jīntiān méiyǒu shíjiān.",t:"나는 오늘 시간이 없어요.",l:"HSK 1",c:"시간"},
]

// ── 오늘의 단어 ────────────────────────────────────────────────

// 2024-01-01 부터 며칠 지났는지. 로컬 자정 기준.
function dayIndex(date) {
  const start = new Date(2024, 0, 1)
  const today = new Date(date.getFullYear(), date.getMonth(), date.getDate())
  return Math.round((today - start) / 86400000)
}

function selectedLevels() {
  const raw = (typeof args !== "undefined" && args.widgetParameter) || ""
  const trimmed = String(raw).trim()
  if (!trimmed || trimmed === "전체" || trimmed.toLowerCase() === "all") {
    return trimmed ? null : DEFAULT_LEVELS   // null = 전체
  }
  const parsed = trimmed.split(",").map(s => s.trim()).filter(Boolean)
  return parsed.length ? parsed : DEFAULT_LEVELS
}

function todayWord(date) {
  const levels = selectedLevels()
  let pool = levels ? WORDS.filter(w => levels.indexOf(w.l) !== -1) : WORDS
  if (pool.length === 0) pool = WORDS
  const n = pool.length
  const i = ((dayIndex(date) % n) + n) % n
  return pool[i]
}

// 원형 위젯용. 한자만 뽑고, 길면 앞 2자로 줄인다.
function compactWord(word) {
  const hanzi = (word.w.match(/[\u4e00-\u9fff]/g) || []).join("")
  const base = hanzi || word.w
  return base.length > 3 ? base.slice(0, 2) : base
}

function shortMeaning(word) {
  const first = word.m.split(",")[0].trim()
  return first.length > 8 ? first.slice(0, 8) : first
}

function nextMidnight() {
  const d = new Date()
  return new Date(d.getFullYear(), d.getMonth(), d.getDate() + 1, 0, 0, 10)
}

// ── 위젯 ──────────────────────────────────────────────────────
//
// 잠금화면 위젯에는 제목도 앱 이름도 넣지 않는다.
// 한자 → 병음 → 뜻 순서만 지킨다.

function rectangularWidget(word) {
  const w = new ListWidget()
  w.setPadding(0, 0, 0, 0)

  const hanzi = w.addText(word.w)
  hanzi.font = Font.boldSystemFont(20)
  hanzi.textColor = Color.white()
  hanzi.lineLimit = 1
  hanzi.minimumScaleFactor = 0.6

  const pinyin = w.addText(word.p)
  pinyin.font = Font.systemFont(12)
  pinyin.textColor = Color.white()
  pinyin.textOpacity = 0.85
  pinyin.lineLimit = 1
  pinyin.minimumScaleFactor = 0.7

  const meaning = w.addText(word.m)
  meaning.font = Font.systemFont(11.5)
  meaning.textColor = Color.white()
  meaning.textOpacity = 0.85
  meaning.lineLimit = 1
  meaning.minimumScaleFactor = 0.7

  return w
}

function circularWidget(word) {
  const w = new ListWidget()
  w.setPadding(0, 0, 0, 0)
  w.addSpacer()

  const row = w.addStack()
  row.addSpacer()
  const text = compactWord(word)
  const label = row.addText(text)
  label.font = Font.boldSystemFont(text.length <= 1 ? 28 : text.length === 2 ? 21 : 16)
  label.textColor = Color.white()
  label.lineLimit = 1
  label.minimumScaleFactor = 0.5
  row.addSpacer()

  w.addSpacer()
  return w
}

function inlineWidget(word) {
  const w = new ListWidget()
  w.addText(word.w + " · " + shortMeaning(word))
  return w
}

function buildWidget(word, family) {
  let w
  if (family === "accessoryCircular") w = circularWidget(word)
  else if (family === "accessoryInline") w = inlineWidget(word)
  else w = rectangularWidget(word)
  w.refreshAfterDate = nextMidnight()
  return w
}

// ── 연속 학습일 (앱에서 열었을 때만 기록) ────────────────────────

function statePath() {
  const fm = FileManager.local()
  const dir = fm.joinPath(fm.documentsDirectory(), "today-chinese")
  if (!fm.fileExists(dir)) fm.createDirectory(dir, true)
  return fm.joinPath(dir, "state.json")
}

function readState() {
  try {
    const fm = FileManager.local()
    const path = statePath()
    if (!fm.fileExists(path)) return { count: 0, lastDay: null }
    return JSON.parse(fm.readString(path)) || { count: 0, lastDay: null }
  } catch (e) {
    return { count: 0, lastDay: null }
  }
}

function updateStreak() {
  const today = dayIndex(new Date())
  const state = readState()
  if (state.lastDay === today) return state.count || 1
  if (state.lastDay === today - 1) state.count = (state.count || 0) + 1
  else state.count = 1
  state.lastDay = today
  try {
    FileManager.local().writeString(statePath(), JSON.stringify(state))
  } catch (e) {
    // 저장 실패는 조용히 넘어간다. 단어 보는 데는 지장이 없다.
  }
  return state.count
}

// ── 앱에서 실행했을 때 보여줄 상세 ──────────────────────────────

function speak(text) {
  try {
    if (typeof Speech !== "undefined" && Speech.speak) {
      Speech.speak(text)
      return true
    }
  } catch (e) {
    // Scriptable 버전에 따라 없을 수 있다.
  }
  return false
}

async function showDetail(word) {
  const streak = updateStreak()
  const table = new UITable()
  table.showSeparators = false

  const hanzi = new UITableRow()
  hanzi.height = 72
  hanzi.addText(word.w).titleFont = Font.boldSystemFont(40)
  table.addRow(hanzi)

  const head = new UITableRow()
  head.height = 56
  head.addText(word.p, word.m)
  table.addRow(head)

  const meta = new UITableRow()
  meta.height = 36
  meta.addText(word.l + " · " + word.c)
  table.addRow(meta)

  const example = new UITableRow()
  example.height = 64
  example.addText(word.e, word.ep)
  table.addRow(example)

  const translation = new UITableRow()
  translation.height = 44
  translation.addText(word.t)
  table.addRow(translation)

  const listen = new UITableRow()
  listen.height = 48
  listen.dismissOnSelect = false
  listen.onSelect = () => {
    if (!speak(word.w + "。" + word.e)) {
      const alert = new Alert()
      alert.title = "발음 재생을 지원하지 않아요"
      alert.message = "Scriptable 버전에 Speech 기능이 없습니다."
      alert.addCancelAction("확인")
      alert.present()
    }
  }
  listen.addText("🔊 발음 듣기")
  table.addRow(listen)

  const foot = new UITableRow()
  foot.height = 40
  foot.addText(streak > 0 ? "🔥 " + streak + "일 연속 학습 중" : "오늘부터 시작")
  table.addRow(foot)

  await table.present()
}

// ── 진입점 ────────────────────────────────────────────────────

const word = todayWord(new Date())

if (config.runsInWidget) {
  Script.setWidget(buildWidget(word, config.widgetFamily))
} else {
  await showDetail(word)
}

Script.complete()
