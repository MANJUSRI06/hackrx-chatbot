from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

def generate_answers(questions, retriever):
    print("[INFO] generate_answers() called")

    try:
        llm = ChatOpenAI(
            temperature=0,
            model_name="openai/gpt-3.5-turbo",  # ✅ OpenRouter requires this format
            base_url="https://openrouter.ai/api/v1",  # ✅ Required for OpenRouter
            api_key="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"  # ✅ Your key
        )
        print("[INFO] OpenRouter LLM initialized.")
    except Exception as e:
        print("[ERROR] LLM Init Failed:", e)
        return [f"❌ LLM Init Failed: {e}" for _ in questions]

    try:
        qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
        results = []
        for q in questions:
            print(f"[INFO] Asking question: {q}")
            answer = qa.run(q)
            print(f"[INFO] Answer: {answer}")
            results.append(answer.strip())
        return results

    except Exception as e:
        print("[ERROR] QA Error:", e)
        return [f"❌ QA Failed: {e}" for _ in questions]
