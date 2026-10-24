import os
import re

base_dir = r"C:\Users\Samer Alhalib\.gemini\antigravity\scratch\wedding-invitation"
index_file = os.path.join(base_dir, "index.html")

with open(index_file, "r", encoding="utf-8") as f:
    html_content = f.read()

# 1. Check all CSS files referenced in index.html
css_pattern = re.compile(r'href=["\']([^"\']+\.css)["\']')
css_files = css_pattern.findall(html_content)
print("CSS Files found in HTML:", css_files)
for css in css_files:
    css_path = os.path.join(base_dir, css.replace("/", os.sep))
    assert os.path.exists(css_path), f"Missing CSS file: {css_path}"
    print(f"  [OK] {css} exists ({os.path.getsize(css_path)} bytes)")

# 2. Check all JS files referenced in index.html
js_pattern = re.compile(r'src=["\']([^"\']+\.js)["\']')
js_files = js_pattern.findall(html_content)
print("JS Files found in HTML:", js_files)
for js in js_files:
    js_path = os.path.join(base_dir, js.replace("/", os.sep))
    assert os.path.exists(js_path), f"Missing JS file: {js_path}"
    print(f"  [OK] {js} exists ({os.path.getsize(js_path)} bytes)")

# 3. Check JS module imports in app.js
app_js_path = os.path.join(base_dir, "js", "app.js")
with open(app_js_path, "r", encoding="utf-8") as f:
    app_js = f.read()

import_pattern = re.compile(r"from\s+['\"](\./[^'\"]+)['\"]")
imports = import_pattern.findall(app_js)
print("Module imports in app.js:", imports)
for imp in imports:
    imp_path = os.path.normpath(os.path.join(base_dir, "js", imp.replace("/", os.sep)))
    assert os.path.exists(imp_path), f"Missing imported module: {imp_path}"
    print(f"  [OK] Module {imp} verified ({os.path.getsize(imp_path)} bytes)")

# 4. Strict data verification per requirements
required_texts = [
    "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
    "وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً ۚ إِنَّ فِي ذَٰلِكَ لَآيَاتٍ لِّقَوْمٍ يَتَفَكَّرُونَ",
    "عائلة المرحوم حسين المرعي",
    "محمد قناطري",
    "صدام حسين المرعي",
    "كريمة السيد محمد قناطري",
    "الجمعة 30 أكتوبر 2026",
    "الساعة 5:00 عصرًا",
    "الانطلاق من منزل العريس",
    "صالة ليالي النجوم",
    "غربي كفر عويد، شمال طريق الرام",
    "صالة مخصصة للرجال",
    "صالة مخصصة للنساء",
    "عدم التصوير داخل صالة النساء",
    "بحضوركم نزداد سرورًا، وتكتمل فرحتنا",
    "شكرًا لمشاركتنا فرحتنا",
    "نسأل الله أن يديم عليكم الأفراح والمسرات، وأن يجمعنا وإياكم دائمًا على الخير والمحبة"
]

print("\nVerifying mandatory texts:")
for txt in required_texts:
    found_in_html = txt in html_content
    found_in_config = False
    with open(os.path.join(base_dir, "js", "config.js"), "r", encoding="utf-8") as f:
        found_in_config = txt in f.read()
    
    assert found_in_html or found_in_config, f"Text not found in project: {txt}"
    print(f"  [MATCH] '{txt[:30]}...' -> HTML: {found_in_html}, Config: {found_in_config}")

# 5. Verify that 'علي وكريمته' is NOT in the project
assert "علي وكريمته" not in html_content, "Forbidden phrase found!"

print("\nALL VERIFICATIONS PASSED 100% PERFECTLY!")
