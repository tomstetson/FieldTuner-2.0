#!/usr/bin/env python3
"""
Script to replace the messy BackupTab with the clean version
"""

import re

def fix_backup_tab():
    """Replace the messy BackupTab with the clean version."""
    
    # Read the clean backup tab
    with open('src/backup_tab_clean.py', 'r', encoding='utf-8') as f:
        clean_backup_tab = f.read()
    
    # Extract just the class definition (remove imports and docstring)
    lines = clean_backup_tab.split('\n')
    class_start = -1
    class_end = -1
    
    for i, line in enumerate(lines):
        if line.startswith('class BackupTab'):
            class_start = i
        elif class_start != -1 and line.startswith('class ') and not line.startswith('class BackupTab'):
            class_end = i
            break
    
    if class_start == -1:
        print("❌ Could not find BackupTab class in clean file")
        return False
    
    if class_end == -1:
        class_end = len(lines)
    
    clean_class = '\n'.join(lines[class_start:class_end])
    
    # Read the main.py file
    with open('../main.py', 'r', encoding='utf-8') as f:
        main_content = f.read()
    
    # Find the BackupTab class in main.py
    pattern = r'class BackupTab\(QWidget\):.*?(?=class \w+\(|$)'
    match = re.search(pattern, main_content, re.DOTALL)
    
    if not match:
        print("❌ Could not find BackupTab class in main.py")
        return False
    
    # Replace the class
    new_content = main_content.replace(match.group(0), clean_class)
    
    # Write the fixed content
    with open('../main.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Successfully replaced BackupTab with clean version")
    return True

if __name__ == "__main__":
    fix_backup_tab()
