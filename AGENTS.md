# Working on PETS

Before changing teaching content, read [TEACHING_GUIDE.md](TEACHING_GUIDE.md) and the relevant entries in [SOURCE_NOTES.md](SOURCE_NOTES.md). The guide records the learner's preferences and the framework for sequencing, explanations, visuals and feedback. Current user instructions take precedence.

- Edit the authoring sources described in README, then run `npm run build`; do not maintain separate copies of HW3/HW4 solutions in generated HTML.
- Preserve deck URLs. When removing or merging cards, retain old IDs as tested bookmark aliases. Keep public branding PETS and use only the two shared typography sizes.
- Check prerequisites and mathematical reasoning before layout. Use `npm run test:content` and the relevant browser checks; report their actual scope.
- When feedback identifies a teaching failure, use the guide's Q4 process to decide whether guidance was missing, ignored or too weak. Fix the material and update the guide when needed.

- Use the undergraduate prerequisite boundary in S1. For every formal definition, check E8; for every message exchange, check V8. Review the full prose, not just the coverage checklist.
