"""
ADIM 3: Üretilen testleri çalıştır, pass rate ve coverage ölç.
Çalıştır: python3 3_run_tests.py
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
from config import OUTPUT_DIR

PYTHON = sys.executable  # Aynı Python ortamını kullan


def run_test(func_source, test_code):
    """
    Geçici bir dizinde fonksiyon + test dosyasını çalıştır.
    Döner: {passed, failed, errors, line_coverage, branch_coverage, compile_ok}
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Fonksiyon kaynağını test dosyasının içine göm (import sorunu olmaz)
        test_file = os.path.join(tmpdir, "test_generated.py")
        full_test = (
            "import sys, os\n"
            + func_source + "\n\n"
            + test_code + "\n"
        )
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(full_test)

        # Söz dizimi kontrolü
        result = subprocess.run(
            [PYTHON, "-m", "py_compile", test_file],
            capture_output=True, text=True, cwd=tmpdir
        )
        if result.returncode != 0:
            return {
                "compile_ok": False,
                "passed": 0, "failed": 0, "errors": 1,
                "line_coverage": 0.0, "branch_coverage": 0.0,
                "compile_error": result.stderr[:300],
            }


        # pytest + coverage çalıştır
        cov_cmd = [
            PYTHON, "-m", "pytest",
            "test_generated.py",
            "--cov=test_generated",
            "--cov-branch",
            "--cov-report=json:cov.json",
            "-q", "--tb=no", "--timeout=10",
        ]
        r = subprocess.run(
            cov_cmd, capture_output=True, text=True, cwd=tmpdir, timeout=30
        )
        output = r.stdout + r.stderr

        # Sonuç analizi
        passed = failed = errors_count = 0
        for line in output.splitlines():
            if " passed" in line:
                for part in line.split():
                    if part.isdigit():
                        passed = int(part)
                        break
            if " failed" in line:
                for part in line.split():
                    if part.isdigit():
                        failed = int(part)
                        break
            if " error" in line.lower():
                errors_count += 1

        # Coverage JSON oku
        line_cov = branch_cov = 0.0
        cov_json = os.path.join(tmpdir, "cov.json")
        if os.path.exists(cov_json):
            with open(cov_json, encoding="utf-8") as f:
                cov_data = json.load(f)
            summary = cov_data.get("totals", {})
            line_cov   = round(summary.get("percent_covered", 0), 1)
            b_total    = summary.get("num_branches", 0) or 0
            b_covered  = summary.get("covered_branches", 0) or 0
            branch_cov = round(100 * b_covered / b_total, 1) if b_total else 0.0


        return {
            "compile_ok": True,
            "passed": passed,
            "failed": failed,
            "errors": errors_count,
            "line_coverage": line_cov,
            "branch_coverage": branch_cov,
        }


if __name__ == "__main__":
    # pytest-timeout yükle
    subprocess.run([PYTHON, "-m", "pip", "install", "pytest-timeout", "-q"],
                   capture_output=True)

    in_path = os.path.join(OUTPUT_DIR, "tests_generated.json")
    out_path = os.path.join(OUTPUT_DIR, "results.json")

    with open(in_path, encoding="utf-8") as f:
        tests = json.load(f)

    results = []
    for i, t in enumerate(tests):
        name = f"{t['repo'].split('/')[-1]}/{t['name']}"
        if t["status"] != "generated" or not t["test_code"]:
            results.append({**t, "run": {"compile_ok": False, "passed": 0,
                "failed": 0, "errors": 1, "line_coverage": 0, "branch_coverage": 0}})
            print(f"[{i+1}/{len(tests)}] {name}: ATLA API hatası, atlandı")
            continue

        print(f"[{i+1}/{len(tests)}] {name}... ", end="", flush=True)
        try:
            run = run_test(t["source"], t["test_code"])
        except subprocess.TimeoutExpired:
            run = {"compile_ok": True, "passed": 0, "failed": 0,
                   "errors": 1, "line_coverage": 0, "branch_coverage": 0, "timeout": True}

        results.append({**t, "run": run})

        if not run["compile_ok"]:
            print("HATA Derleme hatası")
        elif run["passed"] > 0:
            print(f"OK {run['passed']}p/{run['failed']}f  "
                  f"line={run['line_coverage']}%  branch={run['branch_coverage']}%")
        else:
            print(f"UYARI  0 test geçti  line={run['line_coverage']}%")

        # Her 5'te bir kaydet
        if len(results) % 5 == 0:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Özet istatistikler
    compiled = [r for r in results if r["run"]["compile_ok"]]
    passed_any = [r for r in compiled if r["run"]["passed"] > 0]
    line_covs = [r["run"]["line_coverage"] for r in compiled]
    branch_covs = [r["run"]["branch_coverage"] for r in compiled]

    print(f"\n{'='*50}")
    print(f"TOPLAM FONKSİYON      : {len(results)}")
    print(f"DERLEME BAŞARISI      : {len(compiled)}/{len(results)}  "
          f"(%{100*len(compiled)//len(results) if results else 0})")
    print(f"EN AZ 1 TEST GEÇTİ   : {len(passed_any)}/{len(compiled)}")
    if line_covs:
        print(f"ORT. SATIR KAPSAMA    : %{sum(line_covs)/len(line_covs):.1f}")
        print(f"ORT. DAL KAPSAMA      : %{sum(branch_covs)/len(branch_covs):.1f}")
    print(f"Sonuçlar kaydedildi   → {out_path}")
