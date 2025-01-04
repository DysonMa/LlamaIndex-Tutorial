from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.evaluation import RetrieverEvaluator, FaithfulnessEvaluator
import json

llm = Ollama(model="llama3.2:3b", request_timeout=600.0)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-m3")
documents = SimpleDirectoryReader(input_dir="../data/docx/").load_data()

"""
小兔子與烏龜的奇幻冒險
很久很久以前，在一片魔法森林裡，住著一隻非常驕傲的小兔子。牠有一雙強壯有力的後腿，每次一跳就能跨出好幾米遠。小兔子每天都會在森林裡奔跑，展示自己的速度，森林裡的其他動物們都知道小兔子跑得飛快。每當牠跑過時，樹上的鳥兒們都會拍著翅膀叫好，而地上的松鼠們則會用崇拜的眼神看著牠。
但是，小兔子卻常常取笑森林裡的慢性子動物，特別是那隻走路慢得像在散步的烏龜。烏龜是森林裡最年長的居民，牠總是慢慢地爬行，從來不著急。每當小兔子遇到烏龜，牠總會說些譏諷的話："烏龜啊，你這麼慢，恐怕太陽下山了你也走不到家吧！"
有一天，小兔子覺得取笑烏龜已經不夠有趣，牠決定要來點更大的挑戰。"嘿，烏龜，要不要來場比賽？"小兔子雙手叉腰，滿臉得意地問道。
烏龜抬起頭，慢悠悠地看了看小兔子，然後平靜地回答："好啊，為什麼不呢？"
小兔子瞪大了眼睛，牠沒想到烏龜竟然會答應。旁邊圍觀的動物們也感到驚訝，牠們紛紛議論："烏龜真的要和小兔子比賽嗎？這根本沒有勝算啊！"
比賽當天，魔法森林裡的動物們都來到了比賽現場。這是一條從森林的入口到山頂的路徑，中間要經過溪流、山洞和一片神秘的迷霧森林。大家都知道，這條路可不是那麼容易走的，但小兔子對自己充滿信心，牠認為自己可以輕鬆取勝。
"比賽開始！"森林裡的老貓頭鷹宣布後，小兔子像離弦的箭一樣衝了出去，留下一片塵土飛揚。烏龜則慢悠悠地開始爬，完全不受小兔子的速度影響，牠依然保持著穩定的步伐，一步一步地向前進。
跑了一會兒，小兔子已經跑出了很遠。牠轉身看了看，烏龜連影子都看不到。小兔子笑了笑，自言自語道："我這麼快，烏龜肯定追不上我。既然這樣，何不休息一下呢？"於是，小兔子在一棵大樹下找了個陰涼的地方，躺了下來，閉上眼睛睡了一會兒。
當小兔子正在做著美夢時，烏龜繼續穩定地向前爬。雖然牠的速度很慢，但牠不曾停下，心中只有一個信念：一步一步，不要放棄。途中，牠遇到了河流，但憑藉著多年累積的智慧，牠找到了繞過河流的安全路線。當牠進入神秘的迷霧森林時，牠毫不慌亂，用爪子觸摸地面，找到正確的路徑，繼續前行。
過了一會兒，太陽漸漸西下，天色開始變暗，小兔子終於醒了過來。牠伸了個懶腰，抖了抖身上的灰塵，準備繼續比賽。"烏龜一定還在後面呢，"牠想道。於是，小兔子開始重新奔跑，信心滿滿地向終點衝去。
但當牠快到終點時，卻看到一個熟悉的身影慢慢爬過終點線——是烏龜！小兔子簡直不敢相信自己的眼睛。烏龜真的贏了這場比賽，牠那慢而穩的步伐最終幫助牠取得了勝利。
動物們都歡呼起來，牠們為烏龜的堅持和智慧感到驚嘆。小兔子則低下了頭，感到既驚訝又羞愧。牠走到烏龜面前，誠懇地說道："我錯了，烏龜。我以為自己一定會贏，但沒想到你用堅持和智慧贏得了比賽。"
烏龜微笑著回答："勝利並不是最快的人才能得到的，有時候，穩定和不放棄的態度才是最重要的。"
從那天起，小兔子再也不取笑其他動物了，牠學會了尊重每個人的優點。而烏龜則成為了森林裡的英雄，牠的故事被動物們口耳相傳，成為了森林裡一個經典的傳說。
"""

# Build the index
index = VectorStoreIndex.from_documents(
    documents=documents,
    embed_model=embed_model,
)

# Get the nodes from the index
nodes = list(index.docstore.docs.values())
print("Node count: ", len(nodes))
node_dict = {}
for node in nodes:
    node_dict[node.node_id] = node.get_content()
print(json.dumps(node_dict, indent=4, ensure_ascii=False))

# Retrive
query = "小兔子和烏龜參與一場比賽，當牠們跑了一會兒，小兔子看不到烏龜了，但後者繼續穩定地向前爬。請問：小兔子為什麼會在此時感到休息的需要？"
retriever = index.as_retriever(similarity_top_k=2)
retrieved_nodes = retriever.retrieve(query)
print("Retrieved nodes are: ")
for node in retrieved_nodes:
    print(node)

# Retrieval Evaluate
retriever_evaluator = RetrieverEvaluator.from_metric_names(
    metric_names=["hit_rate", "mrr", "precision", "recall"],
    retriever=retriever
)
expected_ids = [
    nodes[1].node_id
]
result = retriever_evaluator.evaluate(query=query, expected_ids=expected_ids)
print(result)
print(result.metric_vals_dict)  # {'hit_rate': 1.0, 'mrr': 1.0, 'precision': 0.5, 'recall': 1.0}

# Query
query_engine = index.as_query_engine(llm=llm)
response = query_engine.query(query)
print(response.response)  # 因為牠已經跑出了很遠，覺得自己一定會贏得這場比賽。所以，就決定在路上休息一下，不覺得有必要繼續追趕烏龜。
print([node.score for node in response.source_nodes])  # Retrieval score: [0.763, 0.737]

# Faithful Evaluate
faith_evaluator = FaithfulnessEvaluator(llm=llm)
result2 = faith_evaluator.evaluate_response(
    query=query,
    response=response
)
print(result2.query)
print(response.source_nodes[0].node.text)
print(result2.passing) # Pass or Fail
print(result2.feedback)  # Evaluate Reason