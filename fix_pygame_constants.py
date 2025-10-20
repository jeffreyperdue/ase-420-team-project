#!/usr/bin/env python3
"""
Quick script to fix pygame constants in test files.
"""

import os
import re

def fix_pygame_constants(file_path):
    """Fix hardcoded pygame constants in a test file."""
    
    # Read the file
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace hardcoded constants with actual pygame constants
    replacements = [
        (r'type=1000', 'type=pygame.KEYDOWN'),
        (r'key=1073741906', 'key=pygame.K_UP'),      # UP
        (r'key=1073741904', 'key=pygame.K_LEFT'),    # LEFT  
        (r'key=1073741903', 'key=pygame.K_RIGHT'),   # RIGHT
        (r'key=1073741905', 'key=pygame.K_DOWN'),    # DOWN
        (r'key=32', 'key=pygame.K_SPACE'),           # SPACE
        (r'key=13', 'key=pygame.K_RETURN'),          # RETURN
        (r'key=27', 'key=pygame.K_ESCAPE'),          # ESCAPE
        (r'key=65', 'key=65'),                       # 'A' key (keep as is)
        (r'key=66', 'key=66'),                       # 'B' key (keep as is)
    ]
    
    # Apply replacements
    for old, new in replacements:
        content = content.replace(old, new)
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed pygame constants in {file_path}")

if __name__ == "__main__":
    # Fix the input integration test file
    fix_pygame_constants("tests/integration/test_input_game_integration.py")
