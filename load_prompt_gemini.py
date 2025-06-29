import json
import glob
import google.generativeai as genai
from google.generativeai import GenerativeModel
knowledge = []
for file_path in glob.glob("converted/*.json"):
    with open(file_path) as f:
        content = f.read()
    knowledge.append(content)

genai.configure(api_key="AIzaSyB5N7rOFmxE_MeW4v_FZIzrpeRBSYAMabg")

model = genai.GenerativeModel("models/gemini-1.5-flash")
def ask_gemini(query, knowledge_base):
    context = "\n\n".join(knowledge_base)
    prompt = f"""You are a data analyst assistant. Using only the exoplanet knowledge base below, answer the following question in a clear, complete sentence. If the answer is numerical, provide context (e.g., highest, lowest, average). If unsure, say "I don’t know about this question.I haven't explore this are myself :)".

### Knowledge base:
{context}

### Question:
{query}

Only answer if the information is present in the knowledge base. Otherwise, say 'I don’t know.'"""

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    test_question = "What is the name of an actress?"
    answer = ask_gemini(test_question, knowledge)
    print("Gemini’s Answer:\n", answer)
