<p align="center"><img src="assets/hero.svg" alt="TIKAZ Context Economy for Codex" width="100%" /></p>

<h1 align="center">TIKAZ Context Economy for Codex</h1>
<p align="center"><strong>A fidelity-first multimodal context compiler for the smallest useful context that remains checkable.</strong></p>
<p align="center"><a href="https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy/actions/workflows/validate.yml"><img src="https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy/actions/workflows/validate.yml/badge.svg" alt="Validate" /></a> <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-f4c95d.svg" alt="MIT" /></a> <img src="https://img.shields.io/badge/version-0.8.0-A78BFA.svg" alt="0.8.0" /></p>
<p align="center"><a href="https://github.com/TIKAZI/TIKAZ-AI-Skills">← Explore all seven TIKAZ AI Skills for Codex suites</a></p>

---

## One suite, ready to install

This repository is the independently installable **context-economy** distribution from [TIKAZ AI Skills for Codex](https://github.com/TIKAZI/TIKAZ-AI-Skills). The monorepo is the canonical development source; this repository is automatically synchronized and optimized for people who need only this workflow.

Designed, integrated, refactored, and continuously maintained by **TIKAZ**; community contributions are welcome. This is an independent project, not an OpenAI-official repository.

This repository is an automatically synchronized distribution of the canonical [TIKAZ-AI-Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills) monorepo. Cross-suite issues and source changes belong in the canonical repository.

## What makes it different

- **Paste text or attach files and let the workflow choose Text / Hybrid / Source automatically**
- **Document-to-Markdown preparation compacts text while retaining page anchors, protected facts, table checks, and unresolved visual evidence**
- **Documents with images split into compact text, visual relevance filtering, bounded vision work, and source fallback instead of sending every page blindly**

## Install

Clone or download this repository, then copy the repository folder into the Skill directory supported by your Codex environment. The root `SKILL.md` is the suite orchestrator; child folders are focused Skills that can also be installed separately.

```bash
git clone https://github.com/TIKAZI/TIKAZ-Codex-Context-Economy.git
```

## Try it

```text
Process my pasted text or attached files for this task. Automatically choose Text, Hybrid, or Source, prepare reusable Markdown where safe, retain protected facts and anchors, and make every omission visible.
```

```text
This document contains images or tables. Compact the text separately, skip decorative and duplicate visuals, queue only task-relevant visual evidence, and preserve uncertain source pages.
```

```text
Create a recoverable checkpoint from this long conversation. Preserve decisions, constraints, completed evidence, file paths, numbers, commands, and open questions.
```

## How the suite works

Read [SKILL.md](SKILL.md) for the owning workflow, [references/routing.md](references/routing.md) for specialist routing, and [references/output-contract.md](references/output-contract.md) for the verified handoff. Optional tools are detected at runtime; local login state or machine-specific software is never promised as universally available.

## Repository structure

```text
./
├─ SKILL.md                 # suite orchestrator
├─ agents/                  # Codex UI metadata
├─ references/              # routing and output contract
├─ <child-skill>/           # independently installable specialists
├─ DISTRIBUTION.yml         # canonical source and sync metadata
└─ scripts/                 # deterministic validation
```

## Canonical source and contributions

Development, source review, and cross-suite architecture live in [TIKAZ-AI-Skills](https://github.com/TIKAZI/TIKAZ-AI-Skills). This distribution synchronizes from `suites/context-economy` every week and can also be refreshed manually through GitHub Actions.

Source modes, observed licenses, and concrete TIKAZ contributions are recorded in [SOURCES.yml](SOURCES.yml) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). TIKAZ-authored files are released under the [MIT License](LICENSE).
