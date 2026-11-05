# Quickstart

## Requirements

- Python 3.9+
- PyYAML (`python3 -c "import yaml"`; if missing: `python3 -m pip install pyyaml`)
- Obsidian (optional, for the vault view)
- DSH / DeepSeek Harness (optional, for skill use)

## 1. Clone

```bash
git clone https://github.com/YanKaFei/Costume-Director-Vault-Starter.git
cd Costume-Director-Vault-Starter
```

## 2. Open the vault (optional)

Open the repository root in Obsidian. Start at `00-系统/MOC/README.md`.

## 3. Install the skill

Copy `skills/costume-director` into the `skills/` directory of your DSH profile:

```bash
# The exact profile path depends on your DSH installation.
cp -R skills/costume-director <your-dsh-profile>/skills/
```

Restart or reload DSH, then ask for `costume-director`.

## 4. Generate a prompt

```bash
python3 scripts/visual_prompt.py --id STR-0028 --kind component_detail --markdown
```

The output is **text only**. `image_generation` is always `false`.

## Scope

This is a public research preview. It includes 15 selected cards and 3 visual plates. It is not the full private research vault, and it does not include source channels, internal identifiers, reports or private projects.
