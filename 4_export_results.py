"""
ADIM 4: Sonuçları analiz et ve konsol raporu oluştur.
Çalıştır: python3 4_export_results.py
"""
import json
import os
import statistics
from config import OUTPUT_DIR

# ── Sonuçları oku ──────────────────────────────────────────────────────────────
in_path = os.path.join(OUTPUT_DIR, "results.json")
with open(in_path, encoding="utf-8") as f:
    results = json.load(f)

# ── Temel metrikler ────────────────────────────────────────────────────────────
total        = len(results)
compiled     = [r for r in results if r["run"]["compile_ok"]]
failed_comp  = [r for r in results if not r["run"]["compile_ok"]]
passed_any   = [r for r in compiled if r["run"]["passed"] > 0]

line_covs    = [r["run"]["line_coverage"]   for r in compiled]
branch_covs  = [r["run"]["branch_coverage"] for r in compiled]

compile_rate = 100 * len(compiled) / total if total else 0
pass_rate    = 100 * len(passed_any) / len(compiled) if compiled else 0
avg_line     = statistics.mean(line_covs)   if line_covs   else 0
med_line     = statistics.median(line_covs) if line_covs   else 0
avg_branch   = statistics.mean(branch_covs) if branch_covs else 0
med_branch   = statistics.median(branch_covs) if branch_covs else 0

# ── Repo bazlı özet ────────────────────────────────────────────────────────────
repos = {}
for r in results:
    repo = r["repo"].split("/")[-1]
    repos.setdefault(repo, {"total": 0, "compiled": 0, "passed": 0,
                             "line_covs": [], "branch_covs": []})
    repos[repo]["total"] += 1
    if r["run"]["compile_ok"]:
        repos[repo]["compiled"] += 1
        repos[repo]["line_covs"].append(r["run"]["line_coverage"])
        repos[repo]["branch_covs"].append(r["run"]["branch_coverage"])
        if r["run"]["passed"] > 0:
            repos[repo]["passed"] += 1

# ── Hata kategorileri ──────────────────────────────────────────────────────────
syntax_err = import_err = semantic_err = 0
for r in results:
    err = r["run"].get("compile_error", "") or ""
    if not r["run"]["compile_ok"]:
        if "SyntaxError" in err or "IndentationError" in err:
            syntax_err += 1
        elif "ImportError" in err or "ModuleNotFoundError" in err:
            import_err += 1
        else:
            semantic_err += 1
    elif r["run"]["failed"] > 0:
        semantic_err += 1

# ── Konsol raporu ──────────────────────────────────────────────────────────────
print("=" * 60)
print("DENEY SONUÇLARI ÖZETİ")
print("=" * 60)
print(f"Toplam fonksiyon           : {total}")
print(f"Derleme başarısı (Pass@1)  : {len(compiled)}/{total}  (%{compile_rate:.1f})")
print(f"En az 1 test geçti         : {len(passed_any)}/{len(compiled)}  (%{pass_rate:.1f})")
print(f"Ort. satır kapsama         : %{avg_line:.1f}  (medyan: %{med_line:.1f})")
print(f"Ort. dal kapsama           : %{avg_branch:.1f}  (medyan: %{med_branch:.1f})")
print()
print("REPO BAZLI:")
for rname, d in repos.items():
    lc = statistics.mean(d["line_covs"]) if d["line_covs"] else 0
    bc = statistics.mean(d["branch_covs"]) if d["branch_covs"] else 0
    print(f"  {rname:12s}  derleme={d['compiled']}/{d['total']}  "
          f"geçti={d['passed']}  line=%{lc:.1f}  branch=%{bc:.1f}")
print()
print("HATA KATEGORİLERİ:")
total_err = syntax_err + import_err + semantic_err
if total_err:
    print(f"  Söz dizimi (syntax)    : {syntax_err}  (%{100*syntax_err/total_err:.0f})")
    print(f"  İthalat (import)       : {import_err}  (%{100*import_err/total_err:.0f})")
    print(f"  Anlamsal (semantic)    : {semantic_err}  (%{100*semantic_err/total_err:.0f})")
print("=" * 60)

