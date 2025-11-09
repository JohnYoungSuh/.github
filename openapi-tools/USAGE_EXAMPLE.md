# Quick Start Guide

## Step 1: Copy your OpenAPI file to this directory

If your file is in a Docker container:

```bash
# From your host machine
docker cp <container_id>:/local/eMASSRestOpenApi.yaml ./openapi-tools/

# Example with container ID 4c566f706870:
docker cp 4c566f706870:/local/eMASSRestOpenApi.yaml ./openapi-tools/
```

Or if you have it locally, just copy it:

```bash
cp /path/to/eMASSRestOpenApi.yaml ./openapi-tools/
```

## Step 2: Run the comprehensive fixer

```bash
cd openapi-tools

# Fix the file (creates eMASSRestOpenApi.yaml.fixed)
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml
```

## Step 3: Test with Prism

```bash
# Test the fixed file
prism mock eMASSRestOpenApi.yaml.fixed
```

If successful, you should see:
```
[CLI] ✔  success   Prism is listening on http://127.0.0.1:4010
```

Instead of the error:
```
Error parsing: expected a single document in the stream, but found more
```

## Step 4: Use the fixed file

```bash
# Copy back to container if needed
docker cp eMASSRestOpenApi.yaml.fixed <container_id>:/local/

# Or replace the original
mv eMASSRestOpenApi.yaml.fixed eMASSRestOpenApi.yaml
```

---

## Troubleshooting

### If you get errors, validate first:

```bash
python3 validate_yaml.py eMASSRestOpenApi.yaml
```

This will show you:
- Multiple YAML document separators
- YAML syntax errors
- x-faker references
- OpenAPI structure issues

### Run individual fixes:

```bash
# Just fix multiple documents
python3 clean_yaml.py eMASSRestOpenApi.yaml

# Just fix NIST controls
python3 fix_openapi_yaml.py eMASSRestOpenApi.yaml
```

---

## Complete Example Workflow

```bash
# 1. Copy file from Docker
docker cp 4c566f706870:/local/eMASSRestOpenApi.yaml ./

# 2. Validate and see issues
python3 validate_yaml.py eMASSRestOpenApi.yaml

# 3. Fix everything
python3 fix_openapi_with_llm.py eMASSRestOpenApi.yaml

# 4. Validate the fixed file
python3 validate_yaml.py eMASSRestOpenApi.yaml.fixed

# 5. Test with Prism
prism mock eMASSRestOpenApi.yaml.fixed

# 6. If successful, copy back
docker cp eMASSRestOpenApi.yaml.fixed 4c566f706870:/local/
```

---

## Files in this directory

- `fix_openapi_with_llm.py` - **Main tool** - fixes all issues + validates
- `fix_openapi_yaml.py` - Fixes NIST 800-53 controls and CCIs
- `clean_yaml.py` - Fixes YAML formatting and multiple documents
- `validate_yaml.py` - Diagnostic tool to identify issues
- `README.md` - Complete documentation
- `USAGE_EXAMPLE.md` - This file (quick start guide)
