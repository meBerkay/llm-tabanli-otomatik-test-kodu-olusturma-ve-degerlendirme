"""
ADIM 2: Toplanan fonksiyonlar için Gemini ile unit test üret.
Çalıştır: python3 2_generate_tests.py
"""
import json
import os
import time
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, PROMPT_TEMPLATE, OUTPUT_DIR

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)


def clean_code(text: str) -> str:
    """Gemini'nin markdown bloklarını temizle."""
    text = text.strip()
    if text.startswith("```python"):
        text = text[9:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()


def generate_test(func: dict) -> dict:
    """Bir fonksiyon için Gemini'ye test üret."""
    prompt = PROMPT_TEMPLATE.format(source_code=func["source"])
    try:
        response = model.generate_content(prompt)
        test_code = clean_code(response.text)
        return {
            **func,
            "test_code": test_code,
            "status": "generated",
            "error": None,
        }
    except Exception as e:
        return {
            **func,
            "test_code": None,
            "status": "api_error",
            "error": str(e),
        }


if __name__ == "__main__":
    in_path = os.path.join(OUTPUT_DIR, "functions.json")
    out_path = os.path.join(OUTPUT_DIR, "tests_generated.json")

    with open(in_path, encoding="utf-8") as f:
        functions = json.load(f)

    # Daha önce üretilenleri atla (kaldığı yerden devam)
    already_done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding="utf-8") as f:
            done = json.load(f)
        already_done = {(d["repo"], d["name"], d["lineno"]) for d in done}
        results = done
        print(f"DEVAM  {len(already_done)} önceden üretilmiş, devam ediliyor...")
    else:
        results = []

    total = len(functions)
    for i, func in enumerate(functions):
        key = (func["repo"], func["name"], func["lineno"])
        if key in already_done:
            continue

        print(f"[{i+1}/{total}] {func['repo']} → {func['name']}... ", end="", flush=True)
        result = generate_test(func)
        results.append(result)

        if result["status"] == "generated":
            print("OK")
        else:
            print(f"HATA {result['error'][:60]}")

        # Her 5'te bir kaydet
        if len(results) % 5 == 0:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        time.sleep(1.2)  # Gemini free tier: 15 RPM → ~4s güvenli

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    total_ok = sum(1 for r in results if r["status"] == "generated")
    print(f"\nTAMAMLANDI {total_ok}/{total} test başarıyla üretildi → {out_path}")
