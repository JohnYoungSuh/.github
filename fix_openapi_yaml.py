#!/usr/bin/env python3
"""
Script to fix eMASS OpenAPI YAML file by replacing x-faker patterns with proper enums
for NIST 800-53 control acronyms, CCIs, and assessment procedures.
"""

import re
import sys

def get_control_acronym_enum():
    """Returns the proper enum for control acronyms."""
    return """enum:
            # Access Control (AC)
            - AC-1
            - AC-2
            - AC-2(1)
            - AC-2(2)
            - AC-2(3)
            - AC-2(4)
            - AC-3
            - AC-3(2)
            - AC-4
            - AC-5
            - AC-6
            - AC-6(1)
            - AC-6(2)
            - AC-7
            - AC-8
            - AC-10
            - AC-11
            - AC-12
            - AC-14
            - AC-17
            - AC-17(1)
            - AC-17(2)
            - AC-18
            - AC-19
            - AC-20
            - AC-21
            - AC-22
            # Audit and Accountability (AU)
            - AU-1
            - AU-2
            - AU-3
            - AU-4
            - AU-5
            - AU-6
            - AU-6(1)
            - AU-6(3)
            - AU-7
            - AU-8
            - AU-9
            - AU-11
            - AU-12
            # Security Assessment (CA)
            - CA-1
            - CA-2
            - CA-3
            - CA-5
            - CA-6
            - CA-7
            - CA-8
            - CA-9
            # Configuration Management (CM)
            - CM-1
            - CM-2
            - CM-3
            - CM-4
            - CM-5
            - CM-6
            - CM-7
            - CM-8
            - CM-9
            - CM-10
            - CM-11
            # Contingency Planning (CP)
            - CP-1
            - CP-2
            - CP-3
            - CP-4
            - CP-6
            - CP-7
            - CP-8
            - CP-9
            - CP-10
            # Identification and Authentication (IA)
            - IA-1
            - IA-2
            - IA-2(1)
            - IA-2(2)
            - IA-2(3)
            - IA-2(8)
            - IA-2(11)
            - IA-3
            - IA-4
            - IA-5
            - IA-5(1)
            - IA-5(2)
            - IA-6
            - IA-7
            - IA-8
            # Incident Response (IR)
            - IR-1
            - IR-2
            - IR-3
            - IR-4
            - IR-5
            - IR-6
            - IR-7
            - IR-8
            # Maintenance (MA)
            - MA-1
            - MA-2
            - MA-3
            - MA-4
            - MA-5
            - MA-6
            # Media Protection (MP)
            - MP-1
            - MP-2
            - MP-3
            - MP-4
            - MP-5
            - MP-6
            - MP-7
            # Physical Protection (PE)
            - PE-1
            - PE-2
            - PE-3
            - PE-4
            - PE-5
            - PE-6
            - PE-8
            - PE-9
            - PE-10
            - PE-12
            - PE-13
            - PE-14
            - PE-15
            - PE-16
            # Planning (PL)
            - PL-1
            - PL-2
            - PL-4
            - PL-8
            # Personnel Security (PS)
            - PS-1
            - PS-2
            - PS-3
            - PS-4
            - PS-5
            - PS-6
            - PS-7
            - PS-8
            # Risk Assessment (RA)
            - RA-1
            - RA-2
            - RA-3
            - RA-5
            # System Acquisition (SA)
            - SA-1
            - SA-2
            - SA-3
            - SA-4
            - SA-5
            - SA-8
            - SA-9
            - SA-10
            - SA-11
            # System Protection (SC)
            - SC-1
            - SC-2
            - SC-3
            - SC-4
            - SC-5
            - SC-7
            - SC-8
            - SC-10
            - SC-12
            - SC-13
            - SC-15
            - SC-17
            - SC-18
            - SC-19
            - SC-20
            - SC-21
            - SC-22
            - SC-23
            - SC-28
            - SC-39
            # System Integrity (SI)
            - SI-1
            - SI-2
            - SI-3
            - SI-4
            - SI-4(1)
            - SI-4(2)
            - SI-4(4)
            - SI-4(5)
            - SI-4(11)
            - SI-5
            - SI-6
            - SI-7
            - SI-8
            - SI-10
            - SI-11
            - SI-12
            - SI-16
            # Program Management (PM)
            - PM-1
            - PM-2
            - PM-3
            - PM-4
            - PM-5
            - PM-6
            - PM-7
            - PM-9
            - PM-10
            - PM-11"""

def get_cci_enum():
    """Returns the proper enum for CCI identifiers."""
    return """pattern: '^\\\\d{6}$'
          enum:
            - '000001'
            - '000002'
            - '000003'
            - '000004'
            - '000005'
            - '000009'
            - '000012'
            - '000013'
            - '000015'
            - '000016'
            - '000017'
            - '000018'
            - '000019'
            - '000022'
            - '000024'
            - '000026'
            - '000044'
            - '000045'
            - '000046'
            - '000052'
            - '000053'
            - '000056'
            - '000058'
            - '000061'
            - '000063'
            - '000067'
            - '000068'
            - '000070'
            - '000073'
            - '000076'
            - '000125'
            - '000145'
            - '000155'
            - '000158'
            - '000159'
            - '000160'
            - '000162'
            - '000163'
            - '000164'
            - '000167'
            - '000169'
            - '000171'
            - '000172'
            - '000174'
            - '000254'
            - '000451'
            - '000852'
            - '001234'
            - '001453'
            - '001494'
            - '001495'
            - '001499'
            - '001503'
            - '001504'
            - '001581'
            - '001643'
            - '001744'
            - '001858'
            - '001941'
            - '002041'
            - '002115'
            - '002235'
            - '002301'
            - '002450'
            - '002617'
            - '002752'
            - '002899'
            - '003123'
            - '003305'
            - '003447'
            - '003449'
            - '003450'"""

def fix_control_acronyms(content):
    """Replace x-faker control acronym patterns with proper enum."""
    # Pattern to match control acronym x-faker blocks
    pattern = r"(acronym:.*?)\n\s+x-faker:\s*\n\s+random\.arrayElement:\s*\n\s+-\s+-\s+AC-1[\s\S]*?-\s+SI-4\(11\)"

    replacement = r"\1\n          " + get_control_acronym_enum()

    content = re.sub(pattern, replacement, content)

    # Also fix the simple faker references
    content = re.sub(
        r"x-faker:\s*\n\s+random\.arrayElement:\s*\n\s+-\s+-\s+AC-1\n.*?-\s+SI-4\(11\)",
        get_control_acronym_enum(),
        content,
        flags=re.DOTALL
    )

    return content

def fix_cci_identifiers(content):
    """Replace x-faker CCI patterns with proper enum."""
    # Pattern to match CCI x-faker blocks
    pattern = r"(example:\s*['\"]?\d{6}['\"]?)\s*\n\s+x-faker:\s*\n\s+random\.arrayElement:[\s\S]*?-\s+['\"]?\d{6}['\"]?"

    replacement = r"\1\n          " + get_cci_enum()

    content = re.sub(pattern, replacement, content)

    return content

def remove_invalid_controls(content):
    """Remove invalid control acronyms like S-1, S-23, UA-16, SI-56."""
    invalid_patterns = [
        r"-\s+S-1\n",
        r"-\s+S-23\n",
        r"-\s+UA-16\n",
        r"-\s+SI-56\n",
    ]

    for pattern in invalid_patterns:
        content = re.sub(pattern, "", content)

    return content

def main():
    """Main function to process the YAML file."""
    if len(sys.argv) < 2:
        print("Usage: python fix_openapi_yaml.py <input_file> [output_file]")
        print("\nThis script will:")
        print("  1. Replace x-faker control acronyms with proper NIST 800-53 enums")
        print("  2. Replace x-faker CCI patterns with valid 6-digit CCIs")
        print("  3. Remove invalid control identifiers (S-1, UA-16, etc.)")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file + ".fixed"

    print(f"Reading {input_file}...")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        sys.exit(1)

    print("Applying fixes...")
    print("  - Fixing control acronyms...")
    content = fix_control_acronyms(content)

    print("  - Fixing CCI identifiers...")
    content = fix_cci_identifiers(content)

    print("  - Removing invalid controls...")
    content = remove_invalid_controls(content)

    print(f"Writing to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\nDone! Fixed file saved as: {output_file}")
    print("\nChanges made:")
    print("  ✓ Replaced random control acronyms with NIST 800-53 Rev 4 enum")
    print("  ✓ Replaced CCI patterns with valid 6-digit identifiers")
    print("  ✓ Removed invalid control families (S-, UA-)")

if __name__ == "__main__":
    main()
