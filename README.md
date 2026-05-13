<div align="center">

# 🧪 TEST CASE ÜRETİMİ: LLM TABANLI OTOMATİK TEST KODU OLUŞTURMA VE DEĞERLENDİRME

### LLM-Based Automated Test Code Generation and Evaluation

<br>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![pytest](https://img.shields.io/badge/pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br>

> **Ahmet Yesevi Üniversitesi** — Bilgisayar Mühendisliği Yüksek Lisans Programı  
> Dönem Projesi · 2026

</div>

---

## 📋 Proje Özeti

Bu çalışmada, **Google Gemini 2.5 Flash** büyük dil modeli kullanılarak açık kaynaklı Python kütüphanelerindeki fonksiyonlar için **otomatik birim testi** üretilmiş ve üretilen testler üç temel araştırma sorusu çerçevesinde değerlendirilmiştir:

| # | Araştırma Sorusu | Bulgu |
|---|---|---|
| **AS1** | Derleme başarısı oranı nedir? | **%51.9** hatasız derleme |
| **AS2** | Kod kapsama oranları ne düzeydedir? | Satır: **%89.8** · Dal: **%59.6** |
| **AS3** | Hata türleri nasıl sınıflandırılır? | Anlamsal: **%63** · Sözdizimi: **%37** |

## 🏗️ Mimari

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Kaynak Kod     │────▶│   Gemini 2.5     │────▶│   Test Kodu     │
│   (AST ile       │     │   Flash API      │     │   (otomatik     │
│   fonksiyon      │     │                  │     │   üretilmiş)    │
│   çıkarma)       │     │   İstem Şablonu  │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
                                                 ┌─────────────────┐
                                                 │   Değerlendirme  │
                                                 │   • pytest       │
                                                 │   • coverage.py  │
                                                 │   • Hata analizi │
                                                 └─────────────────┘
```

## 🎯 Hedef Kütüphaneler

| Kütüphane | Açıklama | Fonksiyon Sayısı |
|---|---|---|
| [`requests`](https://github.com/psf/requests) | HTTP istemci kütüphanesi | 10 |
| [`click`](https://github.com/pallets/click) | Komut satırı arayüzü çerçevesi | 9 |
| [`toolz`](https://github.com/pytoolz/toolz) | Fonksiyonel programlama araçları | 8 |
| | **Toplam** | **27** |

## 📁 Dosya Yapısı

```
📦 llm-based-test-generation
├── 📄 config.py                    # API anahtarı ve model ayarları
├── 📄 1_collect_functions.py       # AST ile fonksiyon toplama
├── 📄 2_generate_tests.py          # Gemini API ile test kodu üretimi
├── 📄 3_run_tests.py               # pytest ile test çalıştırma ve kapsam ölçümü
├── 📄 4_export_results.py          # Sonuçların analiz ve raporlanması
└── 📂 results/
    ├── 📊 functions.json           # Toplanan 27 fonksiyonun listesi
    ├── 📊 tests_generated.json     # BDM tarafından üretilen test kodları
    └── 📊 results.json             # Derleme, kapsam ve hata analizi sonuçları
```

## ⚙️ Kurulum ve Çalıştırma

### Gereksinimler

```bash
pip install requests click toolz google-generativeai pytest coverage
```

### Adım Adım Çalıştırma

```bash
# 1️⃣ Hedef kütüphanelerden fonksiyonları topla
python 1_collect_functions.py

# 2️⃣ Gemini API ile her fonksiyon için test kodu üret
python 2_generate_tests.py

# 3️⃣ Üretilen testleri çalıştır ve kapsam ölç
python 3_run_tests.py

# 4️⃣ Sonuçları analiz et ve raporla
python 4_export_results.py
```

> **Not:** `config.py` dosyasına [Google AI Studio](https://aistudio.google.com/app/apikey) üzerinden alacağınız Gemini API anahtarını girmeniz gerekmektedir.

## 📊 Temel Bulgular

<div align="center">

```
Derleme Başarısı        ████████████████████░░░░░░░░░░░░░░░░░░░░  51.9%
Satır Kapsaması         ████████████████████████████████████████░  89.8%
Dal Kapsaması           ████████████████████████░░░░░░░░░░░░░░░░  59.6%
```

</div>

- 📌 27 fonksiyonun **14'ü** hatasız derlendi
- 📌 Başarılı testlerde satır kapsaması ortalaması **%89.8**
- 📌 Hataların **%63'ü** anlamsal, **%37'si** sözdizimsel

## 🔬 Kullanılan Teknolojiler

| Teknoloji | Sürüm | Kullanım Amacı |
|---|---|---|
| Python | 3.9+ | Ana programlama dili |
| Google Gemini | 2.5 Flash | Test kodu üretimi (BDM) |
| pytest | 8.x | Birim test çalıştırma |
| coverage.py | 7.x | Kod kapsama analizi |
| AST (stdlib) | — | Fonksiyon kaynak kodu çıkarma |

## 📖 Kaynak Gösterimi

Bu çalışmayı referans olarak kullanmak isterseniz:

```
Özkaradayı, B. C. (2026). Test Case Üretimi: BDM Tabanlı Otomatik Test Kodu
Oluşturma ve Değerlendirme. Yüksek Lisans Dönem Projesi, Ahmet Yesevi Üniversitesi.
```

## 👤 Yazar

**Berkay Can Özkaradayı**  
Yüksek Lisans Öğrencisi · Bilgisayar Mühendisliği  
Ahmet Yesevi Üniversitesi

**Danışman:** Doç. Dr. Kürşat Mustafa Karaoğlan

---

<div align="center">

Ahmet Yesevi Üniversitesi · Mühendislik Fakültesi · 2026

</div>
