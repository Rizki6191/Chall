#!/usr/bin/env python3
"""
Create new challenge folder with template.
Usage: python new.py <day> "<challenge_name>" <category_number>
Category: 1=Pwn, 2=Web, 3=Crypto, 4=Other
Example: python new.py 7 "Ret2Libc via Format String" 1
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Category mapping
CATEGORIES = {
    "1": {"name": "Pwn (Binary Exploitation)", "emoji": "🛡️", "folder": "pwn"},
    "2": {"name": "Web Exploitation", "emoji": "🌐", "folder": "web"},
    "3": {"name": "Cryptography", "emoji": "🔐", "folder": "crypto"},
    "4": {"name": "Other", "emoji": "📁", "folder": "other"}
}

def create_challenge(day: str, name: str, category_code: str):
    """Create folder and template for new challenge"""
    
    if category_code not in CATEGORIES:
        print(f"❌ Invalid category. Use: 1=Pwn, 2=Web, 3=Crypto, 4=Other")
        return False
    
    category = CATEGORIES[category_code]
    
    # Create folders
    day_folder = Path(day)
    assets_folder = Path("assets") / day
    
    if day_folder.exists():
        print(f"⚠️  Folder {day}/ already exists!")
        response = input("Overwrite? (y/N): ")
        if response.lower() != 'y':
            return False
    
    day_folder.mkdir(exist_ok=True)
    assets_folder.mkdir(parents=True, exist_ok=True)
    
    # Create README.md template
    template = f"""# Writeup

### {category['emoji']} {category['name']}

## {name}

disini gw bakal ngerjain ulang soal {name} tanpa adanya ai

![Gambar](../assets/{day}/1.png)

## Lesson Learned
- 
"""
    
    readme_path = day_folder / "README.md"
    readme_path.write_text(template)
    
    print(f"✅ Created day {day}: {name}")
    print(f"   Category: {category['emoji']} {category['name']}")
    print(f"   📁 {day}/README.md")
    print(f"   📁 assets/{day}/ (put screenshots here)")
    print()
    print("📝 Next steps:")
    print(f"   1. Edit {day}/README.md with your writeup")
    print(f"   2. Put screenshots in assets/{day}/ (rename to 1.png, 2.png, ...)")
    print(f"   3. Run: python generate.py")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    
    day = sys.argv[1]
    name = sys.argv[2]
    category = sys.argv[3]
    
    create_challenge(day, name, category)