# ZK Learning Lab — permanent tutorial pilot

Canonical tutorial URL (GitHub Pages): https://anujpare.github.io/study_material/zk-workbench/
Linked from: https://anujpare.github.io/study_material/

## Purpose
This is a **two-card pilot** for a persistent, interactive learning resource authored pedagogically in ChatGPT. Its lesson order follows the 2026-10-27 ZK tutorial:
1. card-01.html: Statements, witnesses, efficient verification, NP.
2. card-02.html: Interactive proof structure, completeness, soundness, random challenge.

Grounding: the user's ETH Privacy Enhancing Technologies Lecture 5–8 Zero-Knowledge Proofs, especially pages 1–3. The goal is a first-year undergraduate explanation, beginning from the underlying problem and definitions rather than assuming cryptography or probability.

index.html is the shared UI shell. It renders one card at a time and provides keyboard, dropdown, and arrow navigation. Each card file contains its own lesson text and interaction markup. The shell implements the demos through delegated click handlers.

## Editing contract — non-negotiable
- Treat **this existing URL and these source files** as the single authoritative tutorial. **Do not generate a second tutorial, disconnected chat lesson, or appended replacement page.**
- Read the current card and its neighboring card before editing.
- For a pedagogical correction, update **only that card's existing file**. Do not alter neighboring cards, the navigation shell, or the PETS landing page unless explicitly requested.
- Write fluid, precise, undergraduate teaching: first motivate a question; define unfamiliar terms; explain every symbol; derive a result step by step; connect each sentence to the proof or idea. Avoid summary-only exposition and missed reasoning links.
- Keep interactive examples consistent with the actual theory. Distinguish pedagogical toy games from formally defined security protocols.
- After every update, read back the edited file and confirm that neighboring files are unchanged. Report the canonical URL, not a fresh copy.
- The two-card scope is a comparison pilot; add more cards only when explicitly requested.

## Comparison across platforms
ChatGPT Sites and Space Pages should use the GitHub card content as *source text*, without letting a website-building model regenerate the teaching. Create Site/Page versions only as separate, deliberately named **comparison prototypes**. Do not present an uncreated prototype as published.
