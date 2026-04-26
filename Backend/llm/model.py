from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1",
    task="text-generation",
    max_new_tokens=1024,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
)


model = ChatHuggingFace(llm=llm)
