#!/usr/bin/env python3
"""
Generate main README.md from existing day folders.
Run: python gen.py
"""

from pathlib import Path
import re

def extract_challenge_info(day_path: Path) -> tuple:
    """Extract challenge name and category from README.md"""
    readme_file = day_path / "README.md"
    
    if not readme_file.exists():
        return None, None, None
    
    content = readme_file.read_text()
    lines = content.split('\n')
    
    # Extract category from "### 🛡️ Pwn (Binary Exploitation)" line
    category = "📁 Other"  # default
    challenge_name = f"Day {day_path.name}"  # default
    
    for i, line in enumerate(lines):
        # Cari baris yang mulai dengan "### " untuk kategori
        if line.strip().startswith('###'):
            # Ambil setelah "### " misal: "🛡️ Pwn (Binary Exploitation)"
            category = line.strip().replace('###', '').strip()
            break
    
    # Cari baris yang mulai dengan "## " untuk nama challenge
    for i, line in enumerate(lines):
        if line.strip().startswith('## '):
            # Ambil setelah "## " misal: "Ret2Libc via Format String"
            challenge_name = line.strip().replace('##', '').strip()
            # Hanya ambil jika tidak terlalu panjang dan bukan kategori
            if len(challenge_name) < 100 and not challenge_name.startswith('🛡️'):
                break
    
    # Fallback jika nama challenge tidak ditemukan
    if challenge_name == f"Day {day_path.name}":
        # Coba ambil dari baris pertama yang bermakna
        for line in lines[:15]:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('![') and len(line) > 5 and len(line) < 80:
                challenge_name = line[:60]
                break
    
    return day_path.name, challenge_name, category

def generate_main_readme():
    """Generate main README.md with all challenges categorized"""
    
    # Find all day folders
    day_folders = []
    for item in Path(".").iterdir():
        if item.is_dir() and item.name.isdigit():
            day_folders.append(item)
    
    if not day_folders:
        print("❌ No day folders found!")
        return
    
    # Extract info from each day
    challenges = []
    for folder in sorted(day_folders, key=lambda x: int(x.name)):
        day_num, name, category = extract_challenge_info(folder)
        if day_num:
            challenges.append({
                "day": day_num,
                "name": name,
                "category": category,
                "folder": folder
            })
            print(f"📖 Day {day_num}: {category} → {name}")
    
    # Group by category
    categories = {}
    for c in challenges:
        cat = c["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(c)
    
    # Generate README.md
    readme_lines = [
        "# 🚩 1 Day 1 Chall",
        "",
        "Cuma Repo yang isinya *writeup* dan catatan.",
        "",
        "---",
        "",
        "## 🗂️ Chall Category",
        ""
    ]
    
    # Generate details for each category
    for category_name, challenge_list in categories.items():
        readme_lines.append("<details>")
        readme_lines.append(f"<summary><b>{category_name}</b></summary>")
        readme_lines.append("<br>")
        readme_lines.append("")
        readme_lines.append("| Day | Challenge Name | Folder |")
        readme_lines.append("| :--- | :--- | :--- |")
        
        for c in sorted(challenge_list, key=lambda x: int(x["day"])):
            readme_lines.append(f"| Day {c['day']} | {c['name']} | [Open Writeup](./{c['day']}) |")
        
        readme_lines.append("")
        readme_lines.append("</details>")
        readme_lines.append("")
    
    # Write file
    output = '\n'.join(readme_lines)
    Path("README.md").write_text(output)
    
    print(f"\n✅ Generated main README.md")
    print(f"📊 Total: {len(challenges)} challenges")
    for cat, lst in categories.items():
        print(f"   {cat}: {len(lst)} days")

if __name__ == "__main__":
    generate_main_readme()