# OpenAPI YAML Fixing Tools

Comprehensive toolkit for fixing and validating OpenAPI YAML files, particularly for eMASS REST API specifications with NIST 800-53 controls and CCI identifiers.

## Tools Overview

### 1. `fix_openapi_with_llm.py` ⭐ **RECOMMENDED**

**All-in-one solution** that combines all fixes and validates using `openapi-llm`.

```bash
python3 fix_openapi_with_llm.py <input.yaml> [output.yaml]
```

**Features:**
- ✅ Fixes the "multiple YAML documents" error (Prism issue)
- ✅ Replaces x-faker patterns with NIST 800-53 Rev 4 control enums
- ✅ Replaces x-faker CCIs with valid 6-digit identifiers
- ✅ Removes invalid control families (S-, UA-, SI-56, etc.)
- ✅ Cleans up formatting and orphaned references
- ✅ Validates with `openapi-llm`
- ✅ Validates YAML syntax

**Example:**
```bash
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml
# Creates: eMASSRestOpenApi.yaml.fixed

# Then test with Prism:
prism mock eMASSRestOpenApi.yaml.fixed
```

---

### 2. `fix_openapi_yaml.py`

Fixes NIST 800-53 control acronyms and CCI identifiers.

```bash
python3 fix_openapi_yaml.py <input.yaml> [output.yaml]
```

**Features:**
- Replaces x-faker control acronyms with proper NIST 800-53 enums
- Replaces x-faker CCI patterns with valid 6-digit CCIs
- Removes invalid control identifiers

---

### 3. `clean_yaml.py`

Removes multiple YAML document separators and cleans formatting.

```bash
python3 clean_yaml.py <input.yaml> [output.yaml]
```

**Features:**
- Removes multiple `---` separators (fixes Prism parsing)
- Removes orphaned x-faker blocks
- Fixes indentation
- Removes trailing whitespace
- Ensures proper file ending

---

### 4. `validate_yaml.py`

Diagnostic tool to identify issues in OpenAPI YAML files.

```bash
python3 validate_yaml.py <input.yaml>
```

**Features:**
- Checks for multiple YAML documents
- Validates YAML syntax
- Checks for pattern/regex issues
- Validates OpenAPI structure
- Identifies x-faker references

---

## Common Issues and Solutions

### Issue: Prism error "expected a single document in the stream, but found more"

**Cause:** Multiple YAML document separators (`---`) in the file.

**Solution:**
```bash
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml
# Or use clean_yaml.py specifically for this issue
python3 clean_yaml.py eMASSRestOpenApi.yaml
```

### Issue: x-faker patterns causing validation errors

**Cause:** x-faker is a mock data extension not supported by standard OpenAPI validators.

**Solution:**
```bash
python3 fix_openapi_yaml.py eMASSRestOpenApi.yaml
```

### Issue: Invalid NIST control identifiers

**Cause:** Invalid control families like S-1, UA-16, SI-56.

**Solution:**
```bash
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml
```

---

## Complete Workflow

### For first-time fixes:

```bash
# 1. Diagnose issues
python3 validate_yaml.py eMASSRestOpenApi.yaml

# 2. Apply comprehensive fixes
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml

# 3. Test with Prism
prism mock eMASSRestOpenApi.yaml.fixed

# 4. If successful, replace original
mv eMASSRestOpenApi.yaml.fixed eMASSRestOpenApi.yaml
```

### For iterative development:

```bash
# Fix in place
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml eMASSRestOpenApi.yaml

# Validate
python3 validate_yaml.py eMASSRestOpenApi.yaml

# Test
prism mock eMASSRestOpenApi.yaml
```

---

## Installation

### Prerequisites

```bash
# Install Python dependencies
pip3 install openapi-llm pyyaml

# Install Prism (for testing)
npm install -g @stoplight/prism-cli
```

### Verify Installation

```bash
# Check openapi-llm
pip3 show openapi-llm

# Check Prism
prism --version

# Check scripts are executable
ls -la *.py
```

---

## Understanding NIST 800-53 Controls

The scripts handle NIST 800-53 Rev 4 security control families:

- **AC** - Access Control
- **AU** - Audit and Accountability
- **CA** - Security Assessment
- **CM** - Configuration Management
- **CP** - Contingency Planning
- **IA** - Identification and Authentication
- **IR** - Incident Response
- **MA** - Maintenance
- **MP** - Media Protection
- **PE** - Physical Protection
- **PL** - Planning
- **PS** - Personnel Security
- **RA** - Risk Assessment
- **SA** - System Acquisition
- **SC** - System Protection
- **SI** - System Integrity
- **PM** - Program Management

Invalid families (S-, UA-) are automatically removed.

---

## Understanding CCI (Control Correlation Identifier)

CCIs are 6-digit identifiers that map to NIST controls:
- Format: `NNNNNN` (e.g., `000001`, `001234`, `003450`)
- Valid range: 000001-999999
- The scripts include a validated subset of common CCIs

---

## Troubleshooting

### Script fails with "Module not found"

```bash
pip3 install openapi-llm pyyaml
```

### "Permission denied" when running scripts

```bash
chmod +x *.py
```

### Prism still fails after fixing

```bash
# Validate the fixed file
python3 validate_yaml.py eMASSRestOpenApi.yaml.fixed

# Check for remaining issues
grep -n "x-faker" eMASSRestOpenApi.yaml.fixed
grep -n "^---$" eMASSRestOpenApi.yaml.fixed
```

### openapi-llm validation warnings

These are often informational. The file may still work with Prism even with minor warnings.

---

## Advanced Usage

### Process multiple files

```bash
for file in *.yaml; do
    python3 fix_openapi_with_llm.py "$file" "${file%.yaml}.fixed.yaml"
done
```

### Diff before/after

```bash
python3 fix_openapi_with_llm.py input.yaml output.yaml
diff -u input.yaml output.yaml | less
```

### Chain tools

```bash
# Clean first, then fix controls, then validate
python3 clean_yaml.py input.yaml temp.yaml
python3 fix_openapi_yaml.py temp.yaml output.yaml
python3 validate_yaml.py output.yaml
```

---

## Contributing

When reporting issues, please include:
1. Input YAML file (or sample)
2. Error message
3. Output of `validate_yaml.py`
4. Python and tool versions

---

## References

- [openapi-llm GitHub](https://github.com/vblagoje/openapi-llm)
- [Prism Documentation](https://stoplight.io/open-source/prism)
- [NIST 800-53](https://nvd.nist.gov/800-53)
- [OpenAPI Specification](https://swagger.io/specification/)
