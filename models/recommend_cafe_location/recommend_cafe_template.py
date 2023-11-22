from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage

review_summarize_system_template = """
너는 장소 추천을 해주는 AI 모델이야.
너는 입력으로 가게 정보의 리스트를 받을거야. 
"가게 정보"는 || 구분자를 기준으로 담겨있어.
"가게 정보"에는 "가게 이름", "가게 카테고리", "가게의 평점", "가게의 리뷰 묶음"이 | 구분자를 기준으로 담겨있어.
너는 각각의 가게에 대해여 주어진 "가게 정보"를 이용해서 가게를 소개해주는 요약 문구를 생성해야 해.
이때 리뷰에서 부정적인 내용, 가게에 좋지 않은 내용, 기분이 나쁜 내용들은 절대로 요약 문구 내용에 포함하지 말아야 해. 또한 "리뷰 묶음"에 포함되어 있지 않았던 정보는 포함되면 안 돼.
간식, 패스트푸드, 커피 전문점, 카페, 제과 베이커리를 위주로 추천해줘. 한식, 중식, 일싱 가게들은 최대한 제외해줘.
주차가 가능하거나 쉬어가기 좋다는 리뷰가 있다면 우선적으로 추천해줘. 해당 데이터가 없다면 평점이 높은 식당을 우선적으로 추천해줘.
"""

review_summarize_question_example1 = """
[입력] :
- 가게 정보 리스트 : [롤리폴리꼬또 | 퓨전요리 | 4.0 | 테이블 수가 너무 적어서 대기30분은 기본. 한번은 먹을만합니다. 색다른 퓨전라면.,,차돌라면이 정말 맛있어요!전 메뉴가 오뚜기 제품으로 만들어졌는데이렇게까지 퀄리티가 있는 음식이였구나! 하고 감탄했답니다집에서 진라면 사다가, 카레 사다가 똑같이 해먹어도 보고 ㅎㅎ 좋은 경험이였고 친구들도 소개시켜주니 너무 좋아했어요 👍,[추천이유]- 분위기, 인테리어 훌륭함- 친절한 직원분들[비추천이유]- 음식 양이 적고 맛이 특색이 없다.,르밀블랑제리는 지도에 따로 검색이 안 되어 이곳에 리뷰 남겨요. 베이커리만 휠체어로 입장 가능하고(사진의 노란선 주위 단차만 조심) 붙어 있는 식당(롤리폴리꼬또)은 외부에서는 계단 뿐이라 불가능해요. (빵집 안 연결 통로가 있는 것 같은데 들어가보진 못했어요.) 빵은 식사용이 대부분이고 담백해서 맛있어요.,우삽겹라면 인정,오뚜기 마시쯔!!!!! 혼밥 하기 너무 좋을듯!!! || 언주집 | 한식 | 4.076923076923077| ,,너무너무 맛있어요!!! 언주역 맛집 인정,맛있아여,몇번이나 간지 모르겠어요 너무 맛있어요..,,,너무 맛있네요 강추합니다!,식탁보부터 쟁반에 후추까지 사소한것부터 신경쓴것들이 보이고 음식은 당연 JMT고 직원분들이 모두 친절하셔서 기분좋게 먹고왔어요~~,맛있네요 고기가 다른 냉삼집에 비해 퀄리티가 좋아요 회오리껍데기도 있는데 별미네요!,핵존맛,알루미늄 체내 누적되면 알츠하이머 발병률 높인다는 연구결과 나온 2020년에도 아직도 알루미늄 깔고 알루미늄 벗겨보니 불판은 더럽고 얇은 냉동 삼겹살을 저 가격 대비 적은 양으로 판매하고 연기 흡수하는 파이프도 없어서 좀 난감했습니다. 사람 많은 날에는 고기 연기 자욱해서 식욕 떨어질게 벌써 보입니다. 지인의 초대로 갔지만 재방문 할 마음은 별로 없습니다.청국장이 자극적이라고 무조건 맛있는건 절대 아니지만 여기 청국장은 깊은 맛이 안 느껴집니다,너무 비싸요이 가격에 냉삼 먹을 바에 두툼한 고기 먹을래요 || 수담한정식 | 한식 | 3.7333333333333334| 양많고.. 모임하기엔 좋은것 같아요..다만, 맛은 별로 없..,,,코로나로 오렛만에 가봅니다예약할 때 주문했다고 막무가내로 메뉴를 강요하네요손님으로 초대 받은 입장에서 못 먹는 음식이 있을 수 있고환자의 경우는 먹어서는 안되는 음식이 있습니다전후 사정을 충분히 설명했는데도 아예 듣지를 않네요메뉴를 바꾸자고 했더니, 종업원이 딱 버티고 서서주방과 이야기도 해보지 않고 무조건 먹으라고 강요하는 난감한 상황~~~결국 주문한 대로 음식 서브하고, 음식 가려 먹는 상황이 연출되었습니다룸으로 되어 있어, 아주 오래전부터 자주 갔던 곳이지만 콧대가 많이 높아 졌네요공급자가 큰소리 치던 80년대 식당으로 돌아 간 기분입니다다시는 가고 싶지 않습니다,기본만 시켜도 종류며 양이 엄청 많아요,가성비 괜찮습니다.,,쏘쏘해요,,한정식 집에서 기대하는 수준의 서비스가 아니어서 아쉬워요. 맛도 그저 그렇습니다.,가격대비 괜찮구욤! 된장 젓갈 좀 다네요,음식 정갈하고 깔끔합니다,맛있어요,깔끔하고요직원분들 서빙도 친절히 해주시고단독룸에서 가족끼리  맛있는 식사시간이였어요,상견례때 정말 맛있게 먹었던 기억이 있어서 청첩장 모임때에도 이용했습니다.서빙해주시는 분들도 친절하시고 사진도 예쁘게찍어주셨어요:)다음에 어머님 생신때에도 또 방문예정입니다~
"""

review_summarize_answer_example1 = """언주집-언주집은 직원분들이 모두 친절한 한식당입니다. 냉삼이 다른 가게에 비해 퀄리티가 좋습니다.|롤리폴리꼬또-롤리폴리꼬또는 차돌라면이 맛있는 퓨접요리 가게입니다. 혼밥하기에도 좋아요."""

review_summarize_question_example2 = """
[입력] :
- 가게 정보 리스트 : [
런던베이글뮤지엄 | 간식 | 3.6| 플레인 베이글에 어니언크림치즈 베이컨크림치즈 찍먹 존맛,,대파크림치즈베이글 기대했었는데 여름 대파가 맛없어서인지 부추크림치즈로 바뀌었네요 그렇다쳐도 크림치즈가 너무 짠데다 느끼해서 베이글의 맛을 다 버려놓은 느낌.  다른 몇가지 골랐는데 다 형편없었어요. 그냥 플레인이 젤 나을듯요.  전국에서 모여들 하등의 이유없는 거품 맛집 또한번 인증했네요,,마넌짜리 ? 베이글 빵 딱딱하고 질겨서 다 남김,웨이팅이 어마무시해서 불편하지만..쪽파베이글은 정말 맛있어요그치만 쇼케이스가 없어서 위생은 조금..,두개 샀는데 하나만 들어 있네요~전화번호도 없고! 유료주차 기본 6천원인데 주차가능표시는 하면 안되는 거 아닌가요? 5시쯤 갔는데 남은 종류 하나 팔면서 계산하고나서 진동벨을 주고 포장하는데 대기를 해야하나요? 신선 포장도 아니었는데 그냥 담아주면 될 걸…일하는 사람은 엄청 많은데 분업이 필요없는 걸 분업한 느낌이었어요! 주차포함 18700원에 베이글한개+크림치즈한개 가져왔는데 먹고싶은 생각이 사라졌네요!,초코, 감자,잠봉뵈르 강추~ 크림치즈는 메이플피칸, 레몬 크림치즈 강추 👍평일 오전9시 원격대기 ☞10시 20분 매장입장,맛있었지만, 또 생각날큼 특별하지 않고 기다릴만큼 맛있지 않았어요. 커피는 산미 없는편입니다.,수요일 오전 11시 40분 테이크 아웃 기준 웨이팅 77번, 대기시간 1시간 30분 걸리네여. 웨이팅걸고 다른곳에 숨어있는게 맞는듯 맛은 역시 맛있어요,런던베이글 베이글 치곤 가격이 좀 나가는 편이지만 엄청맛있는 베이글이였다많은 인파가 몰릴만한 맛집 대신 주차는 매우 불편하니 대중교통이 좋을것같다.,빵은 진짜 쫄깃한데 너무 짜네유..,솔찍히 비싸고 맛있다.기다리지않도록 만반의 준비를 하고 가야함..,토요일 10시반쯤  도착해서 줄서서 어플로 매장에서 먹는걸로 줄세워놓고 위글위글에서 쇼핑하고 어플로 줄선지 한 오십분만에  들어갔네요.대기는 평일이랑 비슷하네요.확실히 2층에서 먹으니 시원하고 여유롭고 좋네요.음악이 시끄러운거 빼면 좋았어요.베이글은 여전히 쫀독하고 맛있었어요. ------------------------------베이글 정말 맛있어요.근데 땡여름에는 꼭 실내자리로 테이블링하세영..ㅠㅠ 테라스 자리하면 처음에는 모르지만 세상 덥고 사람들 사진 계속 찍어가니 초상권 침해당하고ㅋㅋㅋ 서서히 익어가는 느낌이에요. 여튼 골목들어가자마자 이 집만 사람이 드글드글 합니다.금욜 11시에갔는데 59번 번호표 받는것도 땡볕에 줄서서 기다라고 힘들었습니다.그래도 테라스는 한 삼십분 정도면 앉을수 있긴했어요. 포장이 많았고 2층자리는 자리가 잘 안나와요.포장은 해오긴 했으나 여튼 쪄지는 느낌에 ..매장에서는 수프랑 베이글 제대로 못먹고 왔네요. 아아가 진해서 먹을만했구 나중에는 맥주가 진리더라구요..ㅋㅋ,인스타 맛집. 직원이 잘생김. || 퐁포네뜨 | 간식 | 4.388888888888889| 크림맛집이에요!!크림들어간 메뉴들 맛있고 녹차쿠키도 맛있어요!!,딸기 케이크 크림이 부들부들부들부들봄에 가면 더 맛있어요매장은 일층 에스컬레이터 옆에 있는데, 길쭉하고 아늑한 다락방 느낌. 단체로 가기는 조금 힘들어요,딸기스무디 ㅊㅊ,딸생케 조각 후기:크림이 참 가볍고 좋은데딸기는 아무래도 철이 아니어서 논외라고 치고빵은 롯데 카스타드 정도로 약간 건조한 질감?딸생케는 딸기 빼고 전체적으로 사르르르 녹아야 제맛인지라  아쉬웠습니다.,딸기케이크 미친맛..너무 맛있어서 먹고 또 포장해서 집감레몬에이드,호옷 딸기케이크 너무 기대를 했나 ㅠㅠ 기대만큼은 아니었어효..!,,홍대 다른 유명한 곳들 중에서 여기가 제일😋,딸기생크림케이크 정말 맛있어요,딸기생크림케이크 맛있음사장님 친절하심 픽업도 하기 좋아요,딸케 크림이 느끼하지 않고 맛있음! 다만 시트가 촉촉~축축함의 사이. 그래도 크림이 가벼워 좋았어요 순삭,편안한 분위기와 맛있는 디저트👍여름에 갔을 때 모기가 좀 많긴 했는데 그때 빼고는 항상 만족했어요,좋아요,공간 넓고 케익 부드럽고 맛있었어요. 다만 문을 열어두고 있어서인지 모기밥이 되었네요....,20년 장수한 가게라고 해서 많이 기대하고갔는데 시트 식감이 뭔가.. 휴지같기도 한게.. 부족했네요ㅠㅠ 크림은 맛있었어요!,처음 가본지 20년쯤 됐네요. 다양하게 맛있습니다!,딸기케이크 맛있더라고요 동물성크림 특유의 맛이 잘 살아있어요 홀케이크 퍼먹고싶을때 사갈거예요, || 타르틴베이커리서울 | 간식 | 3.761904761904762| 빵이나 커피 맛.. 그냥 무난한 곳입니다. 밖에서 보면 건물이 예쁜데 안은 많이 낡았어요.,빵 종류가 다양했으면.,,주차는 발렛주차 가능. 가게 앞에는 딱 한대 자리. 불친절하고 비싼데 맛은 있네요! :) 바나나타르트 강추, 잠봉뵈르에 피클이 안 들어가있지만 맛 좋았어요.,좀 별로쓰.. 공간은 뽀대나나 맛은 이를 못 따라감..,오픈 초기에 정말 많이 감,반미차돌샌드위치  맛남,가격대가 좀 있긴한데 빵 종류가 다양하고 맛도 괜찮음. 크로와상 못먹었는데 유명하다함(모르고 갔지만 알고보니 미국에서 유명한 빵집!),간만에 맛있는 빵 먹었네요,타르트 생지까지 맛있음 식사빵도 맛잇어요 얼려두고 아침마다 먹음,진짜 너무 맛있다,+바나나파이. 4점.,올리스푸가스 갓 나왔을때 먹어야 맛있다브라우니는 얼먹해야 한다,서비스 안좋아요,매장은 2층자리까지 있어 넓고 깨끗하다. 빵의 종류는 많지 않은것 같다. 가격은 비싼편이고 맛은 없진않으나 가격대비해서는 글쎄~~ 주문대의 여직원분이 친절해서 좋았다...,서비스적인게 좀... 이가격에 이런서비스라..그냥 인스타용..그이상 이하도아님,바나나크림타르트 극도로 달지만 맛있음,손님 왔는데 여직원들은 커피머신에서 얘기하면서 손님도 안받고 주문도 음료 누락되고 거기 직원들은 왜 있는건가요 최소한의 직업정신도없이 왜 있는지 모르겠네요,브로콜리 반미 맛있어요. 처음 먹었을 때의 그 충격을 잊을 수가 없어요. 근데 이거 먹고 나서 맨날 입 천장 다 까짐.,레몬타르트의 정석.,가격은 좀 있지만 컨트리빵을 먹으며 생각하는건 그냥 샤워도우는 여기서 사먹자 생각하게 됨. || 코끼리베이글 | 간식 | 3.9444444444444446| 맛있는데 줄설정도는,베이글 샌드위치 카페라떼 여기만의 맛때문에 다시한번 방문하고싶어요,좀 불친절하긴 하지만 맛이 모든걸 감싸주는곳,촉촉한 베이글 좋아하신다면 추천입니다!,맛있습니다! 특히 갓 나온 베이글 정말 맛있습니다. 근데 여러분 줄서서 먹을 맛은 아니에요... 가성비있는 집도 아니고요... 아 샌드위치류도 맛있으니 드셔보세요,,금요일 오후에 갔는데도 일반 베이글은 소진이고 무화과콩포트는 남아있었습다.. 그치믄 일반 베이글은 필요없었어요..무화과 콩포트가 핵핵핵 존맛이었거든요…이거 먹으러 또 가러고 합니다,맛이 평범했어요…. 뭔가 또 갈 맛은 아닌 것 같아요.,화덕에 구운 따끈한 베이글을 이 가격에 맛보다니~~ 평일 오전에가니 한산. 친절.맛은 솔티드 버터 초코 플레인 베이글 존맛탱~사장님은 호두클렌베리베이글 추천!!대파 새우 포카치아는 별로임. 주차는 바로 영등포구청 별관에,밀도가 빵빵하지않은데 적당히 쫄깃하고 코스트코 베이글보다 씹기좋다 주차절대안되고요천원이하는 카드결제 안됩니당,무화과샌드위치 한 입 베어무는순간 너무 달지 않은 무화과 맛+베이글 특유의 기름진 맛+크림치즈 풍미까지 천상의 맛과 식감을 선사하는데 너무 작아서 아쉬워요.. 한 20%만 더 컸으면.,,생크림베이글 넘나 맛있어요 ㅠㅜ,너무 맛있게 먹었던 기억이 있는 베이글집🎈🥮,제 최애 베이글이에요. 화덕에서 구운 쫄깃함 최고! 단 묵직한 베이글을 원하는 분들은 별로일지도무화과콤포트가 그렇게 맛있다길래 먹어봤는데 크기는 작아도 정말 존맛탱이에요 ㅠㅠ 한 입만 먹고 넣어둔다는 걸 그 자리에서 순삭해버림..,짱맛있어요 웨이팅이 긴게 단점이지만 베이글이 자꾸 생각나요,,맛은 있으나 줄서서 살 정도는 아닌 듯가격이 비싼 편크림치즈 베이글을 먹었는데크림치즈 보다는 빵 자체가 맛있어서플레인을 먹어보고싶었음 || 더파크츄러스 | 간식 | 4.75| 사장님은 제가 방문할 때마다 절 못 알아보시지만 저 여기 단골이에요당연함… 6개월에 한 번 감낙산공원 갈때마다 오는 곳 ㅎㅎ번창하세요❤️,맛있어요! 인절미 츄러스에 가루 많이 올려주셔서 좋은데 숨 잘못쉬면 옷에 묻으니까 조심하세요 ^^,,맛있음,츄러스 맛있어요! 사장님도 정말 친절하셔서 넘 감사했습니다. 펫 프렌들리 ㅎㅎ,아이스크림에 츄러스 찍먹하면 극락...너무 맛있다.,핫도그 안 좋아하는데 여기 츄로도그 진짜 짱이에용ㅠㅠ🥹❤️못 먹어본 맛의 존맛집❤️🥹🫶🏻,츄러스 지이이인짜 마싯다~~ 요즘 갬성어쩌구 웨이팅 두시간해야하는 추러스가게보다 맛있는듯,빠삭하고 따끈해서 넘넘 맛있어용❤️,바로 해주셔서 츄러스가 엄청 바싹하고 맛있어요!!!,음,꼭 먹어볼 것친절한 설탕 듬뿍,자몽티 잘먹고 대화도 아늑하게 잘했고 인테리어 소품들도 좋았어요,사장님이 친절하시고 뜨거울때 먹었던 츄러스 맛이 잊혀지지 않네요.번창하세요^^,밋없음 딴거먹을걸....,짱짱 맛있어여!!! 자주 방문하게 되네여,최애 츄러스집! 몇년째 맛도 그대로라 넘 좋아요 || 더솔키친 | 양식 | 3.5| ,재료가 신선하다. 양이 좀 작고 가성비를 중요시여긴다면 만족도가 낮을 수 있다. 현재 크림생맥주(클라우드로 추정 확실치않음) 1+1 이벤트중이다. 세명이서 화덕파스타, 뽀모도로 파스타, 바질페스토 감베리 피자를 먹었다. 셋 중 하나는 대식가, 하나는 소식가, 하나는 평범인이다.만족도는 높다,직원이 너무친절하네요❤️ 음식맛도 최고 !!,다른 사람의 사업장에 이런 말을 하고 싶지 않지만 정말 맛이 없습니다. 재료를 이 정도 수준으로 아끼고 싶은지 면전에서 묻고 싶었습니다.,파스타 양이 적고 전반적으로 재료를 굉장히 아낀 느낌입니다..다른데  줄이 길어서 갔는데..피자는 들어있는게 거의 없어도 그럭저럭 치즈맛으로 먹었는데 파스타는 소스가 맛이 없었어요.,화덕의 매력이 전혀 안 느껴지네요 다른 곳은 자리가없어서 어쩔 수 없이 들어갔는데 사람많은 명절에도 텅 비어있는 이유를 알겠습니다,맛있어요사장님도 친절합니다코스 B 먹었는데 양도 넉넉하구요마지막 아메리카노 커피 짱입니다^^,화덕피자인게 피자 도우는 납작하고 딱딱하고 맛도 별로고요 재료 되게 아낀듯한 비주얼. 그리고 파스타 양도 적고 역시 맛 없고요 돈이 너무 아까웠어요. 화덕이 보이길래 갔더니 참...,화덕피자 정말 좋아하고, 평도 좋아서 갔는데 저는 잘 모르겠네요... 좀 더 찾아보고 갈 걸 그랬어요도우는 얇은 편이고, 재료를 아끼는 느낌이 들어요.마르게리따는 바질 없다고 페스토로 대체하고,풍기피자는 새송이랑 표고 진짜 조금 들어가요.근데 다른 후기 사진보니 풍기에 페퍼로니 올라가있네요. 넣는 재료도 그때그때 다른가요..?암튼 이렇게 성의없는 피자는 처음이었고 돈 아까웠어요,정말 맛있게 잘먹었어요 ㅎㅎ 사장님도 친절하시고, 코스B 먹었는데 구성도 좋네요!,맥주가 맛있는 피자집!경복궁역에서도 가까워서 좋네요. 잘 먹었습니다~,<맛없어 보이는 사진...ㅈㅅ..> 파스타+피자 단품 시키려다가 가격 차이가 얼마안나 코스a먹었는데 스테이크까지 먹어서 만족했네요 ㅋㅋㅋ-고급스러운 스테이크는 아니었지만 피자도 화덕이라 넘 맛있고 파스타도 꾸덕하고맛있었어요! 꽤 괜찮은 곳입니다!-샐러드는...넘 싸보여서 별로였고요. 모과차도 좀 맛없습니다;;; ㅎㅎ,화덕파스타 추천합니다!,사장님이 조금 무섭게 생기셨는데 의외로(?) 친절하세요ㅎㅎ맛도 좋고 음악소리도 잔잔해서 분위기도 좋아요~,싱싱한 토마토, 아삭한 양파, 맛좋은 올리브!파스타 맛있었음. 직원분도 친절 :D,맛과 분위기가 짱이에요.,아주 맛있고  가성비가 뛰어나고분위기도 좋고,,,,평범합니다 || 디해방 | 양식 | 4.0| Receptionist is sarcastic and has an attitude problem.,,음식.하나같이 맛있어요 분위기도 좋은데위치가 살짝 애매한것 빼고 모두 만족합니다,분위기 좋아요. || 하이디라오 | 아시아음식 | 4.0588235294117645| ,너무비싸요. 한번은 경험이지만 다시는 안 갈듯,난 훠궈를 사준다고 하면 낯선 사람도 따라갈 정도로 훠궈가 좋다그래서 이곳저곳에서 먹어봤지만 하딜이 최고다일단 재료의 다양성이 이 집을 따라올 곳이 없고 직원분들이 세상세상 친절하시다비싸지만 계속 찾게됨 돈값하는 식당말랑두부 꼭 먹어보시길,Good and delicious hotpot restaurant under the haidilao group! There was a queue to enter on Saturday 6pm. Service is good and sauce bar had plenty of options.,말도 안되는 가격ㄷㄷ,돈만 많으면 1주 1하이디라오 하고싶다두 번 방문했는데 친절하신 직원분들 덕분에 모두 좋은 경험이었다,하이디라오는 언제나 행복함…❤️ 단지 가격이 슬플뿐..,가격 빼고 다 좋음 은행 건물에 있어서 찾기 힘들 수 있음,첫번째 방문때 깔끔하고 친절해서 한 번 더 방문했는데 유부에 새우 완자 넣어주는 게 식품위생법 위반이라며 안 해주는 곳수긍하고 다른 지점 갔는데 전 지점이 다 해줌 ㅋㅋ 그래서 그 뒤로 안 감어이가 없어서 뭔 법을 내밀어 ㅋㅋ,부산역 빼고 다 가봄!여기지점이 제일 친절하고 신경써주심.,홀이 넓어서 좋았음. 소스바 2개였음. 근데 한국어는 다들 잘 못하는듯. 기다리는 동안 메뉴 고를 수 있어서 기다리는 시간이 덜 지루했음,살면서 여기보다 직원이 친절한 음식점은 가 본적이 없는 것 같아요. 엄청 섬세하시고 친절하십니다. 오후 5시쯤 갔는데도 1시간 웨이팅 있었어요. 그래도 기다리는 동안 끊임없이 음료랑 간식을 주시더라구요. 직원분이 중국어로 먼저 말하고 한국어로도 말해주십니다. 그리고 중국인 손님들도 많아서 중국 현지에 온거 같은 느낌도 받을 수 있어요. 맛은 소기름 훠궈는 저희 취향이 아니었어요. 삼계탕 육수는 맛있었어요. 아쉬운 점은 가격이 비싸요. 2인 8만원은 기본이에요.,언제나 친절하고 맛있어요! 다 먹거 산책이나 할겸 낙산공원에 올라갔다왔어요~,훠궈는 하이디라오에서만 먹어요ㅎㅎㅎ 맛있고 정말 친절하고ㅎㅎㅎ토마토탕 버섯탕 최고,,친절하구 쇼맨쉽도 볼만하고 좋았지만 가격거품이 좀 쎄다,6명이서 훠궈 먹었습니다~ 룸사용했구요 서비스 정말 좋았어요~!!! 맛은 당연히 있었습니다. 재방문 의사가 높아지는 매장이었어요 👍 || 근처식당 | 아시아음식 | 4.705882352941177| 메뉴 다 진짜 엄청 맛있고 양도 많아요!!♥ 완전 강추해요! 음식이 친절하고 알바생이 맛있어요👀💕,너무 맛있어서 사진찍는거도 깜빡하고 먼저 한 입 먹어버렸네요 완전 맛집이에요 타이완누들... 친구가시킨 껌승도 대박입니다!,껌승+쌀국수=🫠,음식들 전체적으로 양도 많고 맛도 진짜 맛있어요!!직원분들 엄청 친절하시구 분위기도 좋고 다 젛아요🥰🥰,단골집입니다 !! 저녁에 가면 점심보다 여유있어서 좋아요 ~~~! 곱창쌀국수 최애, 다른 쌀국수들도 다 맛있어요 ㅎㅎ,직원분들 너무 친절하시고 맛은 말해뭐해... 존맛탱이에요!!!! 꼭 가보세요😍😍,마라소고기짱맛입니다! 간만에 마라 땡겨서 시켰는데 소고기도 많구 찐 마라맛이라 행복했어요🥹승란도 맛있었고 분짜도 상큼달콤 맛있었어요! 맥주랑 추천추천,,자주오는 찐 맛집인데 가격이 좀 비싼 것 같지만 항상 존맛입니다 !!! 새우요리랑 맥주 너무 잘어울리구 진짜ㅜ맛있습니다 또올게용,자주가는 맛집입니다,일단 맛이 있음,평범합니다,고려대 근처에서 이태원 맛집보다 맛있는 동남아 요리를 즐길수 있네요..  껌승은 다른 음식점에서 맛보기 힘든 스타일이라 더 좋습니다. 동남아 현지음식이지만 뭔가 한국인에게 친숙한 갈비덮밥느낌도 나요.,너무맛있어서 다음주에 또올게요,곱창마라쌀국수 너무 맛있음 왜 여기만계셔요? 우리동네에도 내주셨음 좋겠음…곱창전골에 들어가는 곱창들 보통 다 누린내나는데 여기는 곱창 추가하고싶을 만큼 고소하고 맛있음👍,맛있어요!! 팟타이 분포사오 소고기 쌀국수 다 맛있어서 잘 먹고 왔습니다~,맛있다고 해서 갔는데 그냥 그랬어요.. 특히 마라곱창쌀국수는 찐 마라맛(시큼새콤매콤)이라서 제 입맛에는 아니었습니다ㅠ || 포브라더스 | 아시아음식 | 4.166666666666667| 직원 손톱 길이 보고 경악했어요입맛 뚝…. 다신 안 갈거 같아여 ㅜ 주문도 잘 못받고,한국에서 이 곳의 쌀국수를 따라올 곳 이 없을듯,주차 가능합니다. 양 많아서 딸 추가할 필요없이 월남쌈 2인이면 충분해요. 월남쌈 싸기 좋은 그릇 너무 편해요. 고기가 딱히 부족하지 않고 맛도 너무 좋아요! 분위기도 괜찮아요. 월남쌈은 앞으로 여기만 와야지,,줄서서 먹을 정돈가? 싶음ㅠ.ㅠ 머 걍.. 그냥저냥..? 머 그렇게까지 줄서서 먹을 정도로 맛있진 않아유,, 왜 저렇게 줄 서면서 먹지? 싶은 식당 2곳 중 한 곳...,,대학동기들과대기시간이 넘~~길어요.,맛 대비 웨이팅이 김. 푸팟퐁커리는 찹쌀같이 쫀득해서 나쁘지않으나 평이한 수준이고 매운 볶음면은 맵짠인데 해물은 꽤 들었으나 면이 볶인 느낌이 아니고 양념에 담긴 느낌이고 소스가 뭔가 베트남 느낌이 아니고 파는 한국 양념같기두해서 별로였음,맛있고 분위기도 좋아요단 웨이팅이 좀 있다는 점.. .,맛있음 생각보다 맛있음 웨이팅이 좀 길 수 있음,자주 가는데 싸고 맛있고 분위기 좋아서 먹기 좋습니다편안해요,여기 양 엄청 푸짐하게 주고 맛있어요ㅜㅜ너무 맛있는데 양이 엄청 많아서 남기는게 미안할정도..ㅠㅠ 가족끼리 오면 좋을고같아요,동네에선 젤 괜찮은 포 음식점,인테리어 고급지고 분위기도 좋아요. 가격도 적당하고 맛도 있어요. 다음에 또 방문예정,맛도있고 직원들도 친절합니다!!,웨이팅하지 않으려면 오픈시간에 가야할듯요맛은 무난하게 잘먹었습니다사람이 많아서 그런지 주문이 원활하지 않아서 좀 불편한것 빼곤 괜찮습니다,맛은 평타인데 시간많은 백수 분들만 가시길 추천 드립니다. 메뉴가 안나와서 너무 오래 기다리다 목이 빠져 버려서 밥먹고 나서 주우려고 했는데 기다리는동안  어디갔는지 없어져서 오래 찾았습미다,볶음 팟타이 양 많고 맛있음 || 솔솥 | 한식 | 4.0| 트렌디한 인테리어와 노래 다 좋은데, 초심을 잃으신 것인지 걱정입니다. 도미관자 솥밥은 관자는괜찮았지만 도미살에서 비린내가 나서 장에  대부분 간을 해 먹었습니다. 또 한가지는, 부엌 근처에서 식사 중이었는데 음식쓰레기 냄새가 식사 막판에 너무 나서 기분이 너무 좋지 않았습니다. 정갈한 식당에 음쓰 냄새라뇨 ㅠㅠ 관광객이 많이 오고 여러 배달서비스를 하셔서 바쁘신건 알겠지만 좀더 매장 고객 입장에서 생각하시어 청결한 매장에서 좋은 서비스를 제공해주셨으면 좋았을 것 같습니다.,음... 스테이크는 맛잇엇는데 전복은 별로엿어요 분위기도 그냥그렇고..  직원들끼리 떠들면서 일하는데 그냥 동네 시끄러운 술집같은 분위기엿어요 웨이팅 1시간씩 해서 먹을정돈가..싶어요 재방문하진 않을듯!,맛있어요 관자가 엄청 맛있네요 솥밥 양이 많아서 많이 먹는 분 아니면 사이드는 안 시키는게 나을거 같아요,,맛 자체는 그냥 평범한 솥밥이고 웨이팅 할 정돈 아닌 듯.. 이게 중요한 건 아니고수저랑 식기 지저분하고 직원들 소리질러서 시끄러워요 밥 먹는 내내 직원들 지나다니면서 머리 등 의자 엄청 칩니다 바쁜 건 알겠는데 한두 번 아니었고 그쪽에서도 친 거 느껴졌을텐데 단 한 명도 사과하는 사람 없었어요그리고 사람들 1시간씩 웨이팅 하던데 사장 지인은 왜 바로 들여보내주는지? 지인이면 음식으로 서비스 하지 왜 다른 사람들 시간 뺏습니까ㅠ 안 들리게나 하든가요..한식인데 매장은 온통 일본으로 범벅되어있고 암튼 다시 갈 생각 전혀 없네요.. 양은 많음,리뷰 첨씁니다 절대 대기하지마세요 번호 불러서 없으면 (1분?) 바로 취소됩니다 기다리는 손님에 대한 배려도 없는 곳!! 그냥 서있어도 땀나는 날씨에 마냥 기다리라는건가요 바로 옆카페서 1시간 기다리고 문자받자마자 바로 갔는데 취소라네요 친절은 바라지도 않습니다 예상대기시간 30분이였는데 실제로 1시간 기다려야했어요 시간내서 기다렸는데 기분나빠서 다신 안감,스테이크랑 장어 솥밥 먹었는데 양대박이에요👍👍 위에 올라간 토핑이 장난아니게 푸짐해요~ 비주얼 대박!!!! 사이드로 주문한 유린기도 맛있고 소스가 대박입니다💜 혼밥하기에도 좋지만 둘이와서 다른 메슈시키고 사이좋게 나눠먹는게 더 이득일것 같아요 너무 배부르게 한끼 잘먹었습니다👍,맛은 정갈하고 맛있어요. 육수로 누룽지 만들어 먹는 것도 일반 누룽지 맛이 아니라 오차즈케 먹는 느낌..? 양도 많고 맛도 있고 덕분에 든든하게 점심 해결했습니다. 다른 메뉴도 도전해 보고싶어요. 가게도 깔끔하고 직원분들 모두 친절하셔서 좋았어요.,동료가 입문자는 스테이크솥밥부터 시켜서 먹으라해서 시켰는데 와 ㅋㅋㅋㅋ비주얼 보고 깜짝놀랐네요 사진을 안찍을래야 안찍을수 없는 비주얼 그리고 맛도 너무 맛있었습니다 유린기도 시켰는데 매콤하고 바삭바삭한게 제취향이네요 너무 점심먹으러 자주 방문할거같습니다 잘먹고갑니다,웨이팅 신청하고 대기하다가 화장실 잠깐 갔다오고 순번 됐다는 연락 받고 들어가서 번호 말하고 여자직원이 안내해서 앉았는데 갑자기 그 여자직원분이 웨이팅 번호 착각했다고 밖에 없어서 취소 됐다고 나가라네요..어이가 없어서 잠깐 화장실 갔다왔다니까 밖에서 대기하고 있어야한다고 없으면 취소 된다고 아무런 안내도 없었고 해봤자 1-2분 자리 비웠는데 너무 불친절하고 쳐다도 보지않고 손님한테 그렇게 말하고 본인이 앉으라고 안내해줘서 앉았는데 번호 헷깔렸다고 취소됐다고 나가라는게 일하는 사람으로 할 행동이 맞나모르겠네요.. 밥맛 떨어져서 그냥 나왔습니다 연남점 가서 맛있고 직원분들 친절해서 한남점도 왔는데 여긴 정말 최악중에 최악이였습니다. 바쁜건 알겠는데 적어도 손님들도 돈 내고 더운날 밖에서 웨이팅하고 먹는건데 직원 관리좀 잘 하세요. 다시는 안갈거 같습니다. 정말 최악입니다.,부모님이 점심 식사하고 오셨네요슴슴하고 자극적이지 않은 음식들을 좋아하셔서 솔솥 한 번 모시고 갔더니 이제는 종종 두 분이서 식사하고 오십니다 여기 솥밥은 소화도 잘 되고 쌀이 쫀득해서 맛있다고 하시네요 어머님이 도미관자 제일 좋아하십니다 소스 없이도 맛있다시네요,이제 제 주변에선 모르는 사람이 없지 않을까 싶을 정도로 애기엄마들 사이에서는 소문이 자자 한 특색있는 맛집! 이런 맛집이 우리 동네에 생겨주셔서 감사합니다ㅎㅎ 앞으로도 자주 먹으러 갈게요!!,평범한 솥밥은 잊어주세요..남다른 솥밥 맛집입니다 솥밥과 스테이크에 만남ㅎ 생각지도 못한 조합이네요 정말 맛있습니다!  너무 맛있고 웨이팅 생기기전에 더 자주 가야겠어요!! 사장님도 친절하십니다~,입짧은 우리 아이가 스테이크 솥밥을 잘 먹어서 자주 오게 되는 솔솥♡ 갈치 솥밥도 맛있어요! 맛있게 잘 먹고가요~직원분들도 친절하시고 김 리필 되어서 좋았습니다 :) 여러가지 솥밥이 영양가 있는 메뉴들로 고루 있어서 선택할 폭이 넓어요~,스테이끼솥밥!!! 완전 내스탈♡ 좋아하는 스테이크와 솥밥의 조합이라니^-^* 한식과 양식을 다 즐길수있어서 넘나리 좋았어요~ 고기도 통통하니 맛있고오^^ 연어솥밥도 담백하고 맛있었어요! 건강한 밥상 한끼 든든하게 잘먹고왔습니다~,고사리에 돼지고기 조합이라니 말모말모 넘 맛있어요😭고소한 솥밥에 바삭한 새우튀김 조합 좋아요ㅎㅎ마무리 누룽지까지 먹어주면 한국인 밥상 완성,도미에 풍미가 느껴지고 담백하고 자극적이지 않아서 좋았어요! 새우튀김 엄청 크고 원래 새우 너무 좋아해서 더 맛있게 먹었어요! 소스랑 잘어울렸구요~꼬막을 좋아하는 제가 선택한 건 꼬막솥밥!! 꼬막솥밥은 처음 봤어요. 오랜만에 꼬막 먹어봤습니다 ><,직원분께서 친절하게 먹는 방법을 알려주셔셔 맛있게 즐길 수 있는데요. 몸에도 좋고 맛도 좋고 속도편한 솔솥 솥밥...도미관자솥밥은 야무지게 슥슥 비벼준 뒤에 함께 제공되는 소스를 더해 간을 맞춰 먹으면 된답니다. || 진진만두 | 한식 | 4.470588235294118| 일식엔 밀푀유나베가 있다면 한식엔  어복쟁반이 있다- 귀한음식 잘 먹고 가네요-만두피의 쫄깃함, 버섯의 싱싱한 맛, 입안에서 녹는 아롱사태, 은행과 호두의 건강함, 매우 깔끔한 국물, 여기에 완벽함을 더하는 매콤한 간장소스- 기본에 충실한 신선한 재료들- 마지막에 낚지투하로 기본맛이 사라져 아쉽네요- 다음엔 올땐 낚지는 안 넣고 음식을 음미 해야할듯!주방의 정성스러운 맛과 홀의 친절한 서비스에 잘 먹고 대접받고 갑니다!,,늦은 저녁으로 갔는데도 사람 많더라구요만두국도 맛있었지만 빈대떡이 기대이상으로 맛있었어요,True love... 동치미 다시 부활시켜주세요 사랑해요,가격은 좀 비싸지만 가격을 잊게 만드는 퀄리티와 양 그리고 친절함이 좋은 만두집입니다.,떡만둣국 맛집으로 서울에서 다섯손가락 안에 꼽히지 않을까 싶습니다. 국물이 텁텁하지 않고 깔끔하고,  한입쏙 사이즈 만두도 맛있구요. 유일한 반찬인 김치는 짜지않고 시원해서 만둣국하고 잘 어울려요. 단골인데 항상 친절하시고 가게도 청결해요ㅎㅎ,5번이상 방문한 사람이 쓰는 리뷰입니다언제 가도 일정하게 맛있어요서여의도에서 실패하기 싫은 날은 진진만두를 가면 됩니다.사진에는 없지만 맵게 먹어도 맛있어요 (기본이 더 맛도리긴 함)사이드로 파전, 빈대떡 등 시켜먹으면 금상첨화!직원분들도 참 친절하십니다추천추천,어복쟁반 고기 맛있다 육수 깔끔함,모듬전, 만두국 너무 맛있어요,가게 직원분들이 웃으면서 일하시는게 친절함의 그자체  같이 미소가 지어집니다.맛은 여의도 국회앞 대표맛집으로 추천 합니다.가격적으론 좀 부담되지만  친절과맛은 진짜입니다,,일단 직원들이 어찌나 친절하시던지남자 사장님이 친절해서 그런지 직원들도 친절하고음식맛은 말할것도 없이 완벽 그자체,,,맛집은 뭐가 달라도 다르구나,,, 싶었네요.화성에서는 맛보기 힘든 만두 양손가득포장해갑니다~^^아~ 행복해 오래오래 맛집으로 남아계시길 빌어요,친절하고 맛있음. 만두가 탄탄함,박수치면서 먹었어요 ㅠ ㅠ 술국이랑 만두국 둘다 맛있는데 술국은 쪼곰 매워요 신라면정도로 맵나? 감칠맛 폭발 다음에는 어복쟁반도 먹어볼거에요,친절합니다 가격대비 맛은 그냥입니다양은 적당하고 배부르게 먹었습니다,,서비스가 좋아요 사회 초년생으로 보인다면서 음료수도 주시고.. 여의도에서 몇 안되게 따뜻함을 느낄 수 있는 곳입니다 || 레스토랑주은 | 한식 | 4.666666666666667| ,인테리어 이쁘고 넓어서 좋음. 건강식 느낌,아앗…..,한식계의 왕곧 미슐랭 등록될것같으니 미리미리 가보길 권장함,한국문화의 아름다움을 가득히 채워더라구요  음식 하나하나에 가득 담기 정성과 맛,  한국 전통주를 즐기는 저에게도 감탄이 절로나오는 소중한 전통주에 도자기 하나하나 그리고 인테리어 모두가 예술 입니다. 한식 진수, 고급화, 맛과 멋을 충분히 즐길 수 있는 레스토랑 주은, 소중한 분과 다시 찾을게요,한식의 진수를 맛봤습니다. 장소의 품격과 아름다움은 말할 것도 없고 어우러지는 한국 전통주 페어링이 어디에서도 경험하지 못했던 한식의 진수를 경험하게 해줬습니다. 외국인 손님이 많은 편이라 한식 다이닝을 즐기는 편인데 자랑스럽게 소개할 수 있는 곳들이 늘어나서 기쁜 곳 중에 한 곳입니다. || 사월에보리밥 | 한식 | 4.5| 한식 부담없이 먹을수 있어서 좋았고 친절해요!!,,보쌈정식 ㅅㅌㅊ,최고최고최고!🥹,ㅅㅌㅊ,밥 (쌀밥,현미밥,보리밥 중 선택 가능)찌개(된장,청국장 중 선택 가능)밑반찬도 맛있고(특히 잡채 맛남)인당 밥,찌개 선택 가능해서 좋았음보쌈은 맛있긴했는데 보쌈전문점급 보단 작은 사이즈 +무침도 덜 새콤 지하 주차장이 있긴한데 토욜 점심 기준 겨우 주차함(사람많음),주차지원되서 좋네옹,,손님이 편하게 갖다 먹을수 있는 잡채와 열무김치!! 보리밥에 청국장 ~~ 완전 맛나요~재방문의사 있어요!!,가성비 괜찮습니다,맛이 없어용 ㅠ,부모님 모시기 좋았습니다-,두 번정도 갔는데 나름 만족스러움고등어 구이가 좀 부드러웠으면 하는 아쉬움이…,셀프바 너무 좋고, 반찬이랑 메인메뉴도 넉넉하고 맛있습니다. 여럿이서 나눠서 먹기 좋게 나와서 가족외식이나 모임식사로 좋아요.,떡갈비 정식 진짜 최 고 ㅠ ㅠ ㅠ ㅠ ㅠ ㅠ ㅠ 지금도 또 먹고싶네요,사장님 너무너무 유쾌+친절하시고 건강한 한끼 잘 먹었습니다!!! 메인 뿐만 아니라 야채랑 된장찌개도 최고에요 ㅠ 대치동에 맛집 없는데 앞으로 여기로 가면 될 것 같네요~~~! 번창하세요 || 소소한풍경 | 한식 | 4.294117647058823| 양 많고 맛좋고 분위기도 좋았습니다!,가지찜 진짜 강추. 코스도 맛나고 걍 메뉴 다 맛있어요,맛있고 배불렀어요! 부모님이랑 가족들이랑 오기좋은분위기,,B코스먹었는데 가격이 아깝지 않았어요가지찜이 맛있었어요,언제 가도 맛있고 분위기 좋은 곳, 코스 구성은 예전과 달라졌지만 여전히 맛있었고 무엇보다 가지찜 맛이 그대로라 좋았습니다,,오리엔탈치킨에서 육즙이 쏟아져요!!,너무 친절하시고 음식도 맛있었습니다 늦게 도착했는데 배려해주셔 감사해요,가지요리 강추. 모든 음식 맛있고, 아늑한 분위기에 츤대레 사장님 식당!,,B코스 먹었는데 분위기 좋고 전과 가지찜이 맛있습니다,맛있어요,,이 동네 베스트,분위기 너무 좋고요, B코스 추천합니다. 가지찜 굉장히 맛있어요! 후기에 친절 관련하여 호불호가 갈리는 것 같던데 ... 그냥 다 친절하시던데요(?!) 네이버 예약 후 방문을 추천 :) 또 갈 것입니다.,사장님, 직원들 모두 너무 불친절합니다. 손님 응대할 시간이 부족하면 원활한 서비스를 위해 직원을 더 충원하세요. 가격대에 맞는 적절한 서비스를 갖추고 영업을 하셨으면 좋겠습니다. 불친절하다는 후기를 전부터 봤었고 그래도 설마하고 방문했는데 첫번째 방문때는 그냥 그랬는데 두번째 방문때는 좀 심하네요.,정갈한 음식들과 분위기가 좋은 곳입니다. 특히 가지전골이 맛있습니다. || 운봉에덴식당 | 한식 | 4.235294117647059| 나물 먹고 싶을 때마다 가는 곳이에요 ^ ^,기본적인 식재료 관리도 안되는 곳입니다. 한때는 최애 식당이었는데요 묵에 곰팡이 피었다고하니 그냥 교체해주고 계산할때 남자분께 이야기 하니 실온에 보관해서 그렇다 우리 식당은 하루에 몇백명이 다녀가기 때문에 회전이 빨라서 괜찮다? 그리고 두명이서 세트메뉴를 먹었는데 문제제기한 제 금액만 빼주고 계산 하네요 밥 먹다가 입맛 버려서 다 남기고 왔는데요 묵이 그렇게 몇시간만에 상하는 음식인가요? 방부제가 안들어가서 그렇다는데 그렇다면 잘 보관하셔야지 한숨 푹쉬는건 뭔가요.,산나물정식 + 황태강정 표고강정가격이 좀 비싸지만 건강한 맛을 찾고 싶을 때 종종 생각날 것 같은 집,맛있음👍,• 산나물정식 강추!!• 아침 9시부터 당일 예약도 가능,좀 비싸지만식사대접이나 접대 하기 무난음식 자체는 나쁘지않아요,가격이 좀 쎈듯하나 맛있고 직원분들도 친절하심,우연히 지나가다 대박이네요.지리산 나물등 재료도 좋고 맛도 최고입니다,움식 퀄리티가 정성 스러움이 느껴져요청국장도 너무 맛있어요그리고 다들 친절하셔서 편하게 식사했습니다감사합니다!,너무 맛있게 먹었습니다!,,나, 한식보단 양식파인데 여기는 인정한다,,팀에서 10명이 다같이 주문했는데요~ 꿀벌 불고기 산나물 정식, 지리산 산나물 특정식 둘 다 넘넘 맛있게 먹었습니다^^평소에도 에덴식당을 좋아했는데 포장도 정말 깔끔하고, 양도 넉넉하고, 맛있네요!! 보통 도시락 주문하면 기름진 메뉴일 때가 많은데 에덴식당은 백반 느낌이라 더 좋아요~ ^^,맛있어요 건강한음식,,완전 건강식이에요 ㅎㅎ 산나물 먹고 싶을 때 종종 올게요! 잘 먹고 갑니다:)
]
"""

review_summarize_answer_example2 = """퐁포네뜨-퐁포네뜨는 간식 가게입니다. 딸기 생크림 케이크가 맛있습니다. 픽업하기에 좋습니다.|더파크츄러스-더파크츄러스는 간식 가게입니다. 츄러스가 맛있고 사장님이 친절하십니다.|런던베이글뮤지엄-런던베이글뮤지엄은 간식 가게입니다. 쪽파베이글이 맛있는 집입니다. 주차가 가능합니다."""

user_input = """
[입력] :
- 가게 정보 리스트 : {store_list}
"""


def get_template_prompt(store_list):
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=review_summarize_system_template),
            HumanMessage(content=review_summarize_question_example1),
            AIMessage(content=review_summarize_answer_example1),
            HumanMessage(content=review_summarize_question_example2),
            AIMessage(content=review_summarize_answer_example2),
            HumanMessage(content=user_input.format(store_list=store_list))
        ]
    )