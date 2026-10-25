# PETS undergraduate teaching rebuild

The earlier material confused first exposure to cryptography with first exposure to mathematics. It also repeated definitions and sometimes hid the connected explanation behind an interactive view. This rebuild applies the learner’s corrected starting point throughout the eight decks.

## Learner model and writing decisions

- Assume ordinary undergraduate mathematics, including fractions, exponentials, bits, Boolean values, sets and functions.
- Teach unfamiliar course concepts precisely: what the object is, why the protocol needs it, the formal definition, and how to read its quantifiers and probability experiment.
- Use connected prose to establish the goal and justify each consequential step. Keep derivation difficulty in the concept rather than in compressed wording.
- Keep the written explanation visible. Diagrams supplement it and identify participants, their knowledge, actual messages and local checks.
- Put homework preparation where the solution uses it. Keep solutions closed until the learner chooses to inspect them.

These decisions strengthen S1, E1/E8 and V6/V8 in [TEACHING_GUIDE.md](TEACHING_GUIDE.md). Its feedback record distinguishes missing guidance from guidance that was not enforced.

## Consolidation and retained syllabus

| Deck | Before | Now | Disposition |
| --- | ---: | ---: | --- |
| Chapter 1 | 95 | 58 | Rewrite the cryptographic foundations; merge duplicate definitions and proof fragments. |
| Chapter 2 | 73 | 46 | Connect the formal guarantees, graph protocol, simulation, extraction and Fiat–Shamir. |
| Chapter 3 | 48 | 48 | Restore precise succinctness, PCP and PCS statements; explain the formal-polynomial distinction; add protocol diagrams. |
| Chapter 4 | 45 | 44 | Merge selector preparation into secret sharing; state server-view privacy and clarify specialised notation. |
| HW1 | 33 | 15 | Keep every assigned exercise; put necessary preparation in its worked solution. |
| HW2 | 31 | 13 | Keep every assigned exercise; remove standalone repeated primers. |
| HW3 | 12 | 12 | Review every solution; add message-flow diagrams to the construction exercises. |
| HW4 | 15 | 15 | Review every solution; remove elementary notation/gate explanations and add oracle, opening and PIR diagrams. |

There are 251 current cards. Removed legacy IDs remain as bookmark aliases to retained lessons, including without JavaScript. Chapter/homework copies continue to use shared solutions. [SOURCE_NOTES.md](SOURCE_NOTES.md) identifies available source documents and mathematical clarifications; it also states the limits of source comparison for Chapters 1/2.

## What the new diagrams explain

- A distinguisher receives a sample, not the name of its source distribution.
- A commitment opening is checked against the value sent earlier.
- A random oracle remembers previous inputs; a PRF adversary chooses later queries from earlier answers.
- The Hamiltonian protocol reveals one challenge branch per run. The extractor uses two branches from the same saved state.
- Schnorr’s random challenge arrives after its first message. Fiat–Shamir transmits a proof from which that challenge is recomputed.
- Merkle authentication verifies positions and values; the PCP predicate still has to verify the claim.
- Polynomial commitments precede the random evaluation point. Authentic openings and the polynomial identity are separate checks.
- PIR queries conceal a selector; replies let the client reconstruct or decrypt the requested item.

Every protocol figure has a complete static reading order. Step controls highlight the current action without hiding the rest. Existing numerical experiments remain where they support a course concept.

## Review and verification

The generated [card review audit](scripts/teaching-audit.json) covers every current card and distinguishes rewritten explanations, reviewed retained derivations and canonical homework copies. It records editorial scope, not a machine-certified teaching score.

Content checks enforce exercise retention, dependency order, canonical solutions, legacy bookmark coverage and the presence of the key formal definitions. Browser checks cover mathematical rendering, two text sizes, all card navigation, initially closed solutions, visible prose, static protocol diagrams, interaction arithmetic and phone/tablet layouts. Editorial review checks the explanations and representative rendered pages; passing tests alone cannot establish that a learner will find every explanation sufficient.
