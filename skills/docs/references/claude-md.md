## Documentation

This project uses an agent-first documentation architecture.

- **After completing meaningful work**: update ROADMAP.md (check off items, add notes) and add an entry to the daily log in `logs/YYYY-MM-DD.md`. Trivial changes (typos, minor fixes) only need a log entry, not a roadmap update.
- **When planning a meaningful feature**: create a design doc in `design-docs/YYYY-MM-DD-feature-name.md` before implementing. Link it from ROADMAP.md. Use your judgement — if the work involves real decisions or tradeoffs, it deserves a design doc.
- **When an idea comes up that isn't actionable yet**: add it to IDEAS.md.
- **When making a significant decision**: record it in the relevant design doc's Decisions section with date and rationale.
- **Logs vs git**: daily logs capture narrative context — surprises, debugging insights, why you chose an approach. Don't just summarize commits; add the context that commit messages can't convey.
- **ROADMAP tags**: use `#product` and `#marketing` as defaults. Tags let you filter the roadmap by workstream. Create new tags if needed, but keep the set small.
