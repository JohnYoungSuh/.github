#!/usr/bin/env python3
"""
Script to clean OpenAPI YAML files by removing multiple document separators
and fixing common formatting issues.
"""

import sys
import re

def clean_yaml(filepath, output_filepath=None):
    """Clean YAML file by fixing common issues."""

    print(f"Reading: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Track changes
    changes = []

    # 1. Remove multiple document separators (keep only first one if at start)
    lines = content.split('\n')
    cleaned_lines = []
    separator_count = 0
    first_separator_line = -1

    for i, line in enumerate(lines):
        if line.strip() == '---':
            if separator_count == 0 and i < 5:  # First separator near the top is OK
                cleaned_lines.append(line)
                first_separator_line = i
            else:
                changes.append(f"Removed document separator at line {i+1}")
                continue  # Skip this line
            separator_count += 1
        else:
            cleaned_lines.append(line)

    content = '\n'.join(cleaned_lines)

    if separator_count > 1:
        changes.append(f"Removed {separator_count - 1} extra document separator(s)")

    # 2. Remove any orphaned x-faker blocks that weren't caught
    original_faker_count = content.count('x-faker')
    content = re.sub(
        r'\s*x-faker:\s*\n\s+random\.arrayElement:[\s\S]*?(?=\n\s{0,10}\w+:|$)',
        '',
        content
    )
    new_faker_count = content.count('x-faker')
    if original_faker_count > new_faker_count:
        changes.append(f"Removed {original_faker_count - new_faker_count} x-faker block(s)")

    # 3. Fix common indentation issues with enum blocks
    # Make sure enum blocks are properly indented
    content = re.sub(r'\n(\s+)enum:\n(\s+)#', r'\n\1enum:\n\1  #', content)

    # 4. Remove trailing whitespace
    lines = content.split('\n')
    original_line_count = len([l for l in lines if l != l.rstrip()])
    content = '\n'.join(line.rstrip() for line in lines)
    if original_line_count > 0:
        changes.append(f"Removed trailing whitespace from {original_line_count} line(s)")

    # 5. Ensure file ends with newline
    if content and not content.endswith('\n'):
        content += '\n'
        changes.append("Added newline at end of file")

    # Write output
    if output_filepath is None:
        output_filepath = filepath

    if content != original_content:
        print(f"\nApplying {len(changes)} change(s):")
        for change in changes:
            print(f"  - {change}")

        print(f"\nWriting to: {output_filepath}")
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print("✓ Done!")
        return True
    else:
        print("\n✓ No changes needed - file is already clean")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python clean_yaml.py <input_file> [output_file]")
        print("\nThis script will:")
        print("  1. Remove multiple YAML document separators (---)")
        print("  2. Remove any remaining x-faker blocks")
        print("  3. Fix indentation issues")
        print("  4. Remove trailing whitespace")
        print("  5. Ensure proper file ending")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        clean_yaml(input_file, output_file)
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
