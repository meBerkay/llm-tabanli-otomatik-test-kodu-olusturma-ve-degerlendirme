# ──────────────────────────────────────────────────────────
# Deney Konfigürasyonu
# ──────────────────────────────────────────────────────────

# Gemini API Key — https://aistudio.google.com/app/apikey adresinden alınabilir
GEMINI_API_KEY = ""

# Kullanılacak model
GEMINI_MODEL = "gemini-2.5-flash"

# Analiz edilecek GitHub repoları (popüler, test içeren Python projeleri)
REPOS = [
    "psf/requests",       # HTTP kütüphanesi ~30K★
    "pallets/click",      # CLI kütüphanesi ~14K★
    "pytoolz/toolz",      # Fonksiyonel araçlar ~4K★
]

# Her repo'dan kaç fonksiyon seçilecek
FUNCTIONS_PER_REPO = 10  # Toplam 30 fonksiyon

# Çıktı dizini
OUTPUT_DIR = "results"

# Gemini'ye gönderilecek prompt şablonu
PROMPT_TEMPLATE = """You are an expert Python software engineer specializing in test-driven development.
Given the following Python function, write comprehensive unit tests using pytest.

Requirements:
- Use pytest framework
- Test normal cases, edge cases, and error cases
- Use meaningful test function names
- Do NOT use any mocks unless absolutely necessary
- Import only what is needed
- The tests must be self-contained and runnable

Function to test:
```python
{source_code}
```

Return ONLY the Python test code, no explanations, no markdown blocks."""
