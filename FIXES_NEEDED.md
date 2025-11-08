# eMASS OpenAPI Data Generation Fixes

## 1. Control Acronyms - CRITICAL FIX

**Problem:** Using `x-faker: random.arrayElement` generates unrealistic control acronyms

**Solution:** Use `enum` with actual NIST 800-53 Rev 4 controls

### Valid NIST 800-53 Control Families:
- AC (Access Control)
- AT (Awareness and Training)
- AU (Audit and Accountability)
- CA (Assessment, Authorization, and Monitoring)
- CM (Configuration Management)
- CP (Contingency Planning)
- IA (Identification and Authentication)
- IR (Incident Response)
- MA (Maintenance)
- MP (Media Protection)
- PE (Physical and Environmental Protection)
- PL (Planning)
- PS (Personnel Security)
- PT (PII Processing and Transparency) - Rev 5
- RA (Risk Assessment)
- SA (System and Services Acquisition)
- SC (System and Communications Protection)
- SI (System and Information Integrity)
- SR (Supply Chain Risk Management) - Rev 5
- PM (Program Management)

### Replacement Pattern:

**BEFORE (WRONG):**
```yaml
acronym:
  type: string
  example: AC-3
  x-faker:
    random.arrayElement:
      - - AC-1
        - AC-2
        - S-1         # INVALID - "S" is not a valid family
        - S-23        # INVALID
        - SI-16
        - SI-56       # INVALID - SI doesn't go to 56
        - UA-16       # INVALID - "UA" is not a valid family
        - SI-4(11)
```

**AFTER (CORRECT):**
```yaml
acronym:
  type: string
  description: 'NIST SP 800-53 Revision 4 Security Control Identifier'
  example: AC-3
  enum:
    # Access Control (AC)
    - AC-1
    - AC-2
    - AC-2(1)
    - AC-2(2)
    - AC-2(3)
    - AC-2(4)
    - AC-3
    - AC-3(1)
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
    # Certification, Accreditation, and Security Assessments (CA)
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
    # Physical and Environmental Protection (PE)
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
    # System and Services Acquisition (SA)
    - SA-1
    - SA-2
    - SA-3
    - SA-4
    - SA-5
    - SA-8
    - SA-9
    - SA-10
    - SA-11
    # System and Communications Protection (SC)
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
    # System and Information Integrity (SI)
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
    - PM-11
```

## 2. CCI Identifiers - Format Fix

**Problem:** CCIs are shown as 6-digit but examples use varying formats

**Solution:** Always use 6-digit format with leading zeros

**BEFORE:**
```yaml
cci:
  type: string
  example: '000002'
  x-faker:
    random.arrayElement:
      - - '000012'
        - '000045'
        - '000005'
```

**AFTER:**
```yaml
cci:
  type: string
  description: 'Control Correlation Identifier (6-digit format)'
  pattern: '^\d{6}$'
  example: '000002'
  enum:
    - '000001'
    - '000002'
    - '000003'
    - '000004'
    - '000005'
    - '000012'
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
    # ... add more valid CCIs
```

## 3. Assessment Procedures - Pattern Fix

**Problem:** Assessment procedures don't align with controls

**Solution:** Use format CONTROL.PROCEDURE (e.g., AC-1.1, SI-4.5)

**BEFORE:**
```yaml
assessmentProcedure:
  type: string
  example: AC-1.1
```

**AFTER:**
```yaml
assessmentProcedure:
  type: string
  description: 'Assessment Procedure identifier (Control.Procedure format)'
  pattern: '^[A-Z]{2,3}-\d{1,2}(\(\d{1,2}\))?\.\d{1,2}$'
  example: AC-1.1
  enum:
    - AC-1.1
    - AC-1.2
    - AC-2.1
    - AC-2.2
    - AC-3.1
    - AU-2.1
    - SI-4.1
    - SI-4.2
    # Match the control enums above
```

## 4. Other Fields Needing Attention

### Security Checks
Should use actual STIG IDs:
```yaml
securityChecks:
  type: string
  description: 'STIG vulnerability IDs'
  example: 'SV-230221r743913_rule'
  pattern: '^(SV-\d+r\d+_rule|V-\d+)(,\s*(SV-\d+r\d+_rule|V-\d+))*$'
```

### POA&M External UID
Should be actual UUID format:
```yaml
externalUid:
  type: string
  format: uuid
  description: 'UUID format identifier'
  example: 'd6d98b88-c866-4496-9bd4-de7ba48d0f52'
```

## Files Requiring Changes

Search and replace all instances of:

1. `x-faker: random.arrayElement` with control acronyms → Replace with `enum`
2. Invalid control families (S-, UA-) → Remove
3. CCI format inconsistencies → Standardize to 6-digit
4. Assessment procedure examples → Align with controls

## Locations in File:

- Line ~2840: `roleCategory` (keep as-is, this is valid)
- Line ~4350: Control acronym examples
- Line ~4850: CCI examples
- Line ~5200: Assessment procedure examples
- Multiple locations in schemas section

## Testing Recommendations

1. Validate all enum values against NIST 800-53 Rev 4 official list
2. Ensure CCIs map to actual NIST CCI database
3. Cross-reference assessment procedures with control implementations
4. Test mock server generates only valid combinations
