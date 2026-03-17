---
name: worktree-bootstrap
description: Bootstrap a git worktree so local repo commands run correctly. Use when working in a new worktree, when `typecheck` or dev scripts fail because dependencies are missing, or when the user wants a repeatable worktree setup workflow. Prefer shared `node_modules` and `.env.local` symlinks by default, but switch to a real install or separate env file when the worktree needs to diverge.
---

# Worktree Bootstrap

Prepare a git worktree so normal project commands work with minimal duplication.

## When to use

Use this skill when:

- the user asks to work in a separate git worktree
- commands fail because the worktree has no `node_modules`
- `npm run typecheck` or dev scripts fail in a worktree
- the user wants a reusable worktree setup process

## Default policy

Prefer shared root symlinks from the worktree to the main checkout for:

- `node_modules`
- `.env.local`

Do not share `node_modules` if the worktree changes dependency files. If `package.json`, `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock` differ from the main checkout, use a real install in the worktree instead.

Do share `.env.local` by default when the worktree should use the same secrets and local configuration. Only stop sharing it if the user explicitly wants different env values for that worktree.

## Workflow

1. Identify the main checkout and the worktree path.
2. Check whether the worktree already has usable dependencies.
3. If dependency files match the main checkout:
   - create a root `node_modules` symlink to the main checkout if needed
4. If the main checkout has `.env.local` and the worktree should share secrets:
   - create a root `.env.local` symlink to the main checkout if needed
5. If dependency files differ:
   - remove the shared symlink if present
   - run the package manager install inside the worktree
6. If the worktree needs different env values:
   - do not share `.env.local`
   - create or keep a separate `.env.local` in the worktree
7. Verify repo ignores are clean:
   - root `node_modules` should be ignored even when it is a symlink
   - generated directories like `.react-router/` should already be ignored if the repo uses React Router typegen
8. Run the requested command, usually `npm run typecheck` or a dev script.

## Command guidance

- For search and inspection, compare dependency files in the main checkout and worktree before deciding whether to share installs.
- If the sandbox blocks creating symlinks or writing generated files, rerun with escalation.
- `react-router typegen`, `npm run typecheck`, and dev servers may need write access to `.react-router/`.
- Scripts like `npm run dev:agent` may also need escalation for local credential access or long-running server startup.
- If multiple worktrees may run the dev server at once, do not assume Vite will pick a new port automatically. In middleware-mode setups, rerun with an explicit port such as `PORT=3001 npm run dev:agent`.
- If the repo uses dotenvx or shell-loaded env files, a shared `.env.local` symlink is usually the correct default for matching secrets across worktrees.

## Guardrails

- Do not copy `node_modules` by default. It is slower and easier to stale out than a symlink.
- Do not change dependency files just to make the worktree setup easier.
- Do not install dependencies in the main checkout when the task is scoped to the worktree.
- Do not fork `.env.local` unless the worktree truly needs different secrets, ports, or feature flags.
- If you add a shared-worktree convention to a repo, keep it small:
  - a short note in repo instructions
  - a script if the repo wants one
  - ignore rules that prevent `node_modules` symlinks from appearing as untracked

## Expected outcome

After bootstrap:

- `npm run typecheck` should run from the worktree
- repo status should stay clean
- dev commands like `npm run dev` or `npm run dev:agent` should be runnable from the worktree, with escalation if sandbox policy blocks generated files or credential access
- the worktree should use the same local secrets as the main checkout unless the user asked for env divergence
