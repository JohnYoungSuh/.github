#!/bin/bash
#
# Quick fixes for eMASS OpenAPI YAML - removes invalid control families
# Run this FIRST before applying the Python script
#
# Usage: ./quick-fixes.sh your-file.yaml
#

if [ $# -eq 0 ]; then
    echo "Usage: $0 <yaml-file>"
    echo ""
    echo "This script removes invalid control families from your OpenAPI YAML file."
    echo "Run this first, then use fix_openapi_yaml.py for complete fixes."
    exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
    echo "Error: File '$FILE' not found!"
    exit 1
fi

echo "Creating backup: ${FILE}.backup"
cp "$FILE" "${FILE}.backup"

echo "Removing invalid control families..."

# Remove invalid control families
sed -i.tmp '/^\s*-\s*S-1$/d' "$FILE"
sed -i.tmp '/^\s*-\s*S-23$/d' "$FILE"
sed -i.tmp '/^\s*-\s*SI-56$/d' "$FILE"
sed -i.tmp '/^\s*-\s*UA-16$/d' "$FILE"

# Remove the temp files
rm -f "${FILE}.tmp"

echo "✓ Removed invalid control families (S-1, S-23, SI-56, UA-16)"
echo ""
echo "Next steps:"
echo "  1. Review the changes: diff ${FILE}.backup ${FILE}"
echo "  2. Run the Python fix script: python3 fix_openapi_yaml.py ${FILE}"
echo ""
echo "Backup saved as: ${FILE}.backup"
