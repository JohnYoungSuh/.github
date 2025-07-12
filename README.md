# .github
4. CI/CD with GitHub Actions
4.1. Shared Reusable Workflow (`ci-template.yml` in `.github` repo)

```yaml
name: Shared CI

on:
  workflow_call:
    inputs:
      pdf-name:
        required: true
        type: string

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: sudo apt update && sudo apt install -y pandoc texlive-xetex shellcheck markdownlint

      - name: Lint shell scripts
        run: shellcheck scripts/*.sh

      - name: Lint markdown
        run: markdownlint PROJECT.md README.md

      - name: Build PDF
        run: |
          pandoc PROJECT.md --pdf-engine=xelatex \
            -V geometry:margin=1in -o "${{ inputs.pdf-name }}.pdf"

      - name: Commit artifacts
        run: |
          git config user.name "CI Bot"
          git config user.email "ci@github.com"
          git add "${{ inputs.pdf-name }}.pdf" || echo "No changes"
          git commit -m "Auto-update PDF" || echo "Nothing to commit"
          git push
```
4.2. Stub Workflow (`.github/workflows/ci.yml` in project repo)

```yaml
name: Build & Test
on:
  push:
    branches: [main]
jobs:
  call-shared-ci:
    uses: JohnYoungSuh/.github/.github/workflows/ci-template.yml@main
    with:
      pdf-name: gpu-dock-auto-switch
  # You can add more jobs here: e.g., deploy, notify, etc.
```

---
5. Automation Script for Stubs

Place this on your workstation (e.g. `~/scripts/add-ci-stub.sh`):

```bash
#!/usr/bin/env bash
set -e
export GH_TOKEN=ghp_your_fine_grained_token

for repo in $(gh repo list JohnYoungSuh --json name --jq '.[].name'); do
  echo "Adding stub to $repo"
  gh api repos/JohnYoungSuh/$repo/contents/.github/workflows/ci.yml \
    -f message="chore: add reusable CI stub" \
    -f content="$(base64 <<<'name: Build & Test

on:
  push:
    branches: [main]

jobs:
  call-shared-ci:
    uses: JohnYoungSuh/.github/.github/workflows/ci-template.yml@main
    with:
      pdf-name: gpu-dock-auto-switch
') \
    -f branch=main \
    || echo "Failed for $repo"
done
```

Make it executable and run:
```bash
chmod +x ~/scripts/add-ci-stub.sh
~/scripts/add-ci-stub.sh
```

---

6. Manual Testing Checklist

1. **Script & Rule**  
   - Plug/unplug dock → verify `/var/log/gpu-switch.log` updates.  
   - Check `prime-select query` matches expected GPU.

2. **Git & Remote**  
   - `git remote -v` shows SSH URL.  
   - `git push`/`git pull` works without password.

3. **CI Workflow**  
   - On push, GitHub Actions → **Build & Test** runs successfully.  
   - Artifacts: generated PDF appears in repo root.

4. **Stub Automation**  
   - New repos under your account receive `.github/workflows/ci.yml`.

---

7. Automating Tests Based on Documentation

You can extend your CI to **automatically test** every instruction:

- **Shell Tests**:  
  - Use [Bats](https://github.com/bats-core/bats-core) to write tests for `gpu-switch.sh` logic.  
  - Simulate `online` values by mocking `/sys/class/power_supply/$PSY/online`.

- **Markdown Tests**:  
  - Run `markdownlint` to catch formatting errors.  
  - Use a link checker (e.g., `markdown-link-check`) to ensure internal references exist.

- **PDF Build Test**:  
  - Fail the job if `pandoc` exits non-zero or if the PDF file is missing.

- **udev Rule Simulation**:  
  - In a privileged Docker container, use `udevadm test $(udevadm info --path=...)` to verify rule parsing.

Sample “test.yml” Workflow

```yaml
name: Smoke Tests
on:
  workflow_call:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install test tools
        run: sudo apt update && sudo apt install -y bats markdownlint pandoc texlive-xetex
      - name: Run shell tests
        run: bats tests/gpu-switch.bats
      - name: Lint markdown
        run: markdownlint .
      - name: Build and verify PDF
        run: |
          pandoc PROJECT.md -o test.pdf
          [ -s test.pdf ]
```
You can call this `test.yml` from your stub or chain it with `ci-template.yml` for a full validation suite.
