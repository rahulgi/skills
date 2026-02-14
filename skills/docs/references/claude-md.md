## Documentation

This project uses an agent-first documentation architecture.

- **After completing work**: update ROADMAP.md (check off items, add notes) and add an entry to the daily log in `logs/YYYY-MM-DD.md`.
- **When planning a non-trivial feature**: create a design doc in `design-docs/YYYY-MM-DD-feature-name.md` before implementing. Link it from ROADMAP.md. A feature is "non-trivial" if it touches more than 3 files, changes an interface, or involves a decision with multiple valid approaches.
- **When an idea comes up that isn't actionable yet**: add it to IDEAS.md.
- **When making a significant decision**: record it in the relevant design doc's Decisions section with date and rationale.
- **Logs vs git**: daily logs capture narrative context — surprises, debugging insights, why you chose an approach. Don't just summarize commits; add the context that commit messages can't convey.
- **ROADMAP tags**: use `#product` and `#marketing` as defaults. Create new tags if needed, but keep the set small.
