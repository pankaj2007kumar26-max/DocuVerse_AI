"""
DocuVerse AI / PDF Assistant - Groq API Handler (api_handler.py)
-----------------------------------------------------------------
Active Groq Models verified on this account:
- Primary: qwen/qwen3.8-27b (Fast, multilingual, SOTA quality)
- Fallbacks: openai/gpt-oss-20b, openai/gpt-oss-120b, allam-2-7b

Features:
- RAG Q&A (Strict Anti-Hallucination)
- Executive Document Summaries
- Practice MCQs with Answers & Explanations
- Key Points & Highlights Extraction
- Multi-Language Support (English, Hindi, Hinglish)
"""

import time
from typing import List, Dict, Any, Optional
import requests
import config

GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

# Active Verified Models on user's Groq account
GROQ_MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "allam-2-7b"
]


def call_groq(
    prompt: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.3,
    max_tokens: int = 2048
) -> Dict[str, Any]:
    """
    Groq Cloud API ko direct request bhejta hai using active verified models.
    """
    api_key = getattr(config, "GROQ_API_KEY", "").strip()
    if not api_key:
        return {
            "text": "",
            "model_used": None,
            "success": False,
            "error": "GROQ_API_KEY `.env` file mein nahi mili. Kripya check karein."
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    model_errors = []

    for model_name in GROQ_MODELS:
        try:
            print(f"[Groq AI] Calling verified model '{model_name}'...")
            payload = {
                "model": model_name,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            response = requests.post(
                GROQ_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=45
            )

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                print(f"[Groq AI] Success with {model_name}!")
                return {
                    "text": content,
                    "model_used": f"Groq ({model_name})",
                    "success": True,
                    "error": None
                }
            else:
                err_msg = f"{model_name} (HTTP {response.status_code}): {response.text}"
                print(f"[Groq AI] Warning: {err_msg[:120]}")
                model_errors.append(err_msg[:100])
                time.sleep(0.5)
                continue

        except Exception as e:
            err_msg = f"{model_name}: {str(e)}"
            print(f"[Groq AI] Request error: {err_msg[:120]}")
            model_errors.append(err_msg[:100])
            time.sleep(0.5)
            continue

    return {
        "text": "",
        "model_used": None,
        "success": False,
        "error": " | ".join(model_errors) if model_errors else "All Groq models failed to respond"
    }


def generate_rag_answer(
    query: str,
    context_chunks: List[Dict[str, Any]],
    language: str = "English",
    chat_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    User ke question ka answer strictly PDF context ke basis par deta hai.
    """
    if not context_chunks:
        return {
            "answer": "❌ **Document mein is question se related koi relevant information nahi mili.** (No matching context found in uploaded PDFs)",
            "sources": [],
            "success": False
        }

    # 1. Format Context Blocks with exact Source and Page References
    context_blocks = []
    sources = []
    
    for i, c in enumerate(context_chunks):
        meta = c.get("metadata", {})
        source_name = meta.get("source", "Document")
        page_num = meta.get("page", 1)
        score = c.get("score", 0.0)
        text = c.get("chunk_text", "").strip()
        
        context_blocks.append(f"--- [Context Chunk #{i+1} | Source: {source_name} | Page: {page_num}] ---\n{text}")
        sources.append({
            "source": source_name,
            "page": page_num,
            "score": round(score, 4),
            "snippet": text[:200] + "..." if len(text) > 200 else text
        })

    combined_context = "\n\n".join(context_blocks)

    # 2. Language Directive
    lang_instruction = "Respond in clear, professional English."
    if "Hindi" in language and "Hinglish" not in language:
        lang_instruction = "Respond strictly in clear, natural Hindi (हिंदी भाषा में उत्तर दें)."
    elif "Hinglish" in language:
        lang_instruction = "Respond in conversational Hinglish (Hindi written using English/Roman script, jaise WhatsApp par chat karte hain, e.g. 'Is document ke mutabiq...')."

    # 3. Strict System Prompt (Anti-Hallucination)
    system_instruction = (
        "You are PDF Assistant, an intelligent, strictly factual document assistant powered by Groq LPU.\n"
        "Your task is to answer the user's question using ONLY the provided document context below.\n\n"
        "STRICT RULES:\n"
        "1. Answer ONLY using the facts mentioned in the context. DO NOT assume or make up information.\n"
        "2. If the answer cannot be found in the context, explicitly state: "
        "'I could not find information about this in the uploaded document(s).' Do not guess.\n"
        "3. Keep your explanation structured, clear, and easy to read using markdown formatting.\n"
        "4. When stating facts, cite the source and page number wherever relevant.\n"
        f"5. Language Requirement: {lang_instruction}"
    )

    prompt = f"""DOCUMENT CONTEXT:
{combined_context}

USER QUESTION:
{query}

Please provide a factual and well-structured answer based strictly on the context above:"""

    call_result = call_groq(
        prompt=prompt,
        system_instruction=system_instruction,
        temperature=0.3,
        max_tokens=2048
    )

    if call_result["success"]:
        return {
            "answer": call_result["text"],
            "sources": sources,
            "model_used": call_result["model_used"],
            "success": True
        }
    else:
        return {
            "answer": f"⚠️ **Groq API Error:** {call_result.get('error', 'Unable to fetch response')}",
            "sources": sources,
            "success": False
        }


def generate_document_summary(
    full_text_sample: str,
    language: str = "English"
) -> Dict[str, Any]:
    """Uploaded documents ka executive summary aur key insights generate karta hai."""
    lang_instruction = "Respond in clear English."
    if "Hindi" in language and "Hinglish" not in language:
        lang_instruction = "Respond in Hindi (हिंदी)."
    elif "Hinglish" in language:
        lang_instruction = "Respond in Hinglish (Roman script)."

    prompt = f"""Analyze the following document text and generate a structured summary:
1. **Executive Overview**: High-level summary of the document (3-4 sentences).
2. **Key Highlights & Main Points**: 4-6 bullet points covering core concepts.
3. **Important Entities & Topics**: Major themes, tools, or conclusions mentioned.

Language: {lang_instruction}

DOCUMENT TEXT:
{full_text_sample[:15000]}
"""

    call_result = call_groq(
        prompt=prompt,
        temperature=0.2,
        max_tokens=1500
    )

    if call_result["success"]:
        return {
            "summary": call_result["text"],
            "model_used": call_result["model_used"],
            "success": True
        }
    else:
        return {
            "summary": f"⚠️ Groq summary generation error: {call_result.get('error')}",
            "success": False
        }


def generate_document_mcqs(
    full_text_sample: str,
    num_questions: int = 4
) -> Dict[str, Any]:
    """Document content ke basis par interactive Multiple Choice Questions generate karta hai."""
    prompt = f"""Generate {num_questions} Multiple Choice Questions (MCQs) strictly based on the following document text.
Format each question clearly as:

### Question X: [Question text]
- **A)** [Option A]
- **B)** [Option B]
- **C)** [Option C]
- **D)** [Option D]

**Correct Answer:** [A/B/C/D]
**Explanation:** [1 sentence explanation citing the document]

---

DOCUMENT TEXT:
{full_text_sample[:15000]}
"""

    call_result = call_groq(
        prompt=prompt,
        temperature=0.2,
        max_tokens=2048
    )

    if call_result["success"]:
        return {
            "mcqs": call_result["text"],
            "model_used": call_result["model_used"],
            "success": True
        }
    else:
        return {
            "mcqs": f"⚠️ Groq MCQ generation error: {call_result.get('error')}",
            "success": False
        }


def generate_document_key_points(
    full_text_sample: str,
    language: str = "English"
) -> Dict[str, Any]:
    """Extracts top key points, core takeaways, and important conclusions."""
    lang_instruction = "Respond in clear English."
    if "Hindi" in language and "Hinglish" not in language:
        lang_instruction = "Respond in Hindi (हिंदी)."
    elif "Hinglish" in language:
        lang_instruction = "Respond in Hinglish (Roman script)."

    prompt = f"""Extract and list the 6 to 8 most important Key Points from the document text below.
Format them as crisp, clear bullet points with short bold titles.

Language: {lang_instruction}

DOCUMENT TEXT:
{full_text_sample[:15000]}
"""

    call_result = call_groq(
        prompt=prompt,
        temperature=0.2,
        max_tokens=1500
    )

    if call_result["success"]:
        return {
            "key_points": call_result["text"],
            "model_used": call_result["model_used"],
            "success": True
        }
    else:
        return {
            "key_points": f"⚠️ Groq Key Points extraction error: {call_result.get('error')}",
            "success": False
        }
