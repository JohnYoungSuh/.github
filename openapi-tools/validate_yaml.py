#!/usr/bin/env python3
"""
Script to validate and diagnose OpenAPI YAML file issues.
"""

import sys
import yaml
import re

def check_multiple_documents(filepath):
    """Check if file contains multiple YAML documents."""
    print("\n=== Checking for Multiple YAML Documents ===")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Count document separators
    separators = content.count('\n---\n') + content.count('\n--- \n')

    if separators > 0:
        print(f"⚠️  Found {separators} YAML document separator(s) (---)")
        print("   This can cause 'expected a single document' errors")

        # Show line numbers of separators
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if line.strip() == '---':
                print(f"   Line {i}: {repr(line)}")
        return True
    else:
        print("✓ No multiple document separators found")
        return False

def check_yaml_syntax(filepath):
    """Validate YAML syntax."""
    print("\n=== Validating YAML Syntax ===")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            docs = list(yaml.safe_load_all(f))

        print(f"✓ YAML syntax is valid")
        print(f"  Found {len(docs)} document(s)")

        if len(docs) > 1:
            print(f"⚠️  Multiple documents found - this may cause issues with Prism")
            print(f"   Prism expects a single OpenAPI document")

        return True, docs
    except yaml.YAMLError as e:
        print(f"✖ YAML syntax error:")
        print(f"  {str(e)}")
        return False, None

def check_pattern_issues(filepath):
    """Check for common regex replacement issues."""
    print("\n=== Checking for Pattern/Regex Issues ===")
    issues = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # Check for unescaped backslashes in patterns
    pattern_lines = []
    for i, line in enumerate(lines, 1):
        if 'pattern:' in line:
            pattern_lines.append((i, line))
            # Check if it has single backslash before 'd', 'w', etc.
            if re.search(r"pattern:.*'[^']*\\d", line) or re.search(r'pattern:.*"[^"]*\\d', line):
                # This is actually correct - single backslash in YAML string
                continue

    if pattern_lines:
        print(f"  Found {len(pattern_lines)} pattern definitions:")
        for line_num, line in pattern_lines[:5]:  # Show first 5
            print(f"    Line {line_num}: {line.strip()}")
    else:
        print("  No pattern definitions found")

    # Check for malformed enum blocks
    enum_count = content.count('enum:')
    print(f"  Found {enum_count} enum definition(s)")

    # Check for orphaned x-faker references
    if 'x-faker' in content:
        print(f"⚠️  Still contains x-faker references")
        faker_lines = [i+1 for i, line in enumerate(lines) if 'x-faker' in line]
        print(f"   Found at lines: {faker_lines[:10]}")
        issues.append("x-faker references still present")
    else:
        print("✓ No x-faker references found")

    return issues

def check_openapi_structure(docs):
    """Validate OpenAPI structure."""
    print("\n=== Checking OpenAPI Structure ===")

    if not docs or len(docs) == 0:
        print("✖ No documents found")
        return False

    doc = docs[0]

    if not isinstance(doc, dict):
        print(f"✖ Document is not a dictionary: {type(doc)}")
        return False

    # Check required OpenAPI fields
    if 'openapi' in doc:
        print(f"✓ OpenAPI version: {doc['openapi']}")
    elif 'swagger' in doc:
        print(f"✓ Swagger version: {doc['swagger']}")
    else:
        print("✖ No openapi or swagger field found")
        return False

    if 'info' in doc:
        print(f"✓ Info section present")
        if 'title' in doc['info']:
            print(f"  Title: {doc['info']['title']}")
    else:
        print("⚠️  No info section")

    if 'paths' in doc:
        print(f"✓ Paths section present ({len(doc['paths'])} paths)")
    else:
        print("⚠️  No paths section")

    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_yaml.py <yaml_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    print(f"Validating: {filepath}")
    print("=" * 60)

    try:
        # Check for multiple documents
        has_multiple = check_multiple_documents(filepath)

        # Check YAML syntax
        valid, docs = check_yaml_syntax(filepath)

        if not valid:
            print("\n" + "=" * 60)
            print("RESULT: YAML file has syntax errors")
            sys.exit(1)

        # Check for pattern issues
        issues = check_pattern_issues(filepath)

        # Check OpenAPI structure
        if docs:
            check_openapi_structure(docs)

        print("\n" + "=" * 60)
        if has_multiple:
            print("RESULT: File contains multiple YAML documents")
            print("ACTION: Remove extra '---' separators, keep only the first one at the top")
        elif issues:
            print(f"RESULT: Found {len(issues)} potential issue(s)")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("RESULT: YAML appears valid")

    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
