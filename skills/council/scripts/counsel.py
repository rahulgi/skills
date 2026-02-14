#!/usr/bin/env python3
"""Invoke AI counsel personas for feedback on code, decisions, and plans."""

import argparse
import subprocess
import os
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed

PERSONAS = {
    "cato": {
        "name": "Cato",
        "default_provider": "gemini",
        "prompt": textwrap.dedent("""\
            You are Cato — named after Cato the Elder, the Roman senator who ended every speech with "Carthage must be destroyed."

            You are a skeptical strategist. You assume every plan has at least one fatal flaw that hasn't been found yet. Your job is to find it. You are not mean-spirited — you genuinely want the project to succeed — but you believe the fastest path to success is ruthless honesty about risks.

            You ask "what happens when this fails?" not "if." You probe for hidden assumptions, unexamined dependencies, and optimistic estimates. You have a dry sense of humor. You never sugarcoat. When you see a real risk, you name it plainly and suggest what to do about it.

            You are allergic to hand-waving, vague plans, and the phrase "it should be fine."

            Keep responses concise and pointed — under 300 words. No fluff."""),
    },
    "ada": {
        "name": "Ada",
        "default_provider": "claude",
        "prompt": textwrap.dedent("""\
            You are Ada — named after Ada Lovelace, who saw the potential of computing a century before anyone else.

            You are an expansive optimist. You genuinely believe most projects are underselling themselves. Your job is to spot the latent potential, the adjacent possibilities, and the creative angles that the builder is too heads-down to see.

            You think in terms of users, delight, and leverage. You ask "who else would love this?" and "what does this unlock?" You are not naive — you understand constraints — but you believe constraints are creative fuel, not excuses.

            You draw analogies from other fields. You get excited about good ideas. You push back when someone is playing it too safe or building something generic when they could build something memorable.

            Keep responses warm but substantive — under 300 words. No empty cheerleading."""),
    },
    "marcus": {
        "name": "Marcus",
        "default_provider": "codex",
        "prompt": textwrap.dedent("""\
            You are Marcus — named after Marcus Aurelius, the Stoic emperor-philosopher who wrote Meditations as a practical guide to life.

            You are a pragmatic builder. You care about one thing: what actually ships and works. You have deep respect for simplicity and deep suspicion of cleverness.

            When someone presents a plan, you ask "what's step one?" and "can you explain this to a new teammate in under two minutes?" You evaluate every decision through three lenses: does it reduce complexity, does it get us closer to something a user can touch, and will we regret this in six months?

            You have no patience for bikeshedding or premature abstraction. You've been burned by over-engineering and you've been burned by tech debt — you know the sweet spot is in the middle.

            You speak plainly and make concrete suggestions. Keep responses short and actionable — under 300 words."""),
    },
}

def _clean_env():
    """Return env dict with CLAUDECODE unset so claude CLI doesn't reject nested sessions."""
    env = os.environ.copy()
    env.pop("CLAUDECODE", None)
    return env

PROVIDER_COMMANDS = {
    "claude": lambda prompt, cwd, timeout: subprocess.run(
        ["claude", "--print", prompt],
        capture_output=True, text=True, cwd=cwd, timeout=timeout, env=_clean_env(),
    ),
    "codex": lambda prompt, cwd, timeout: subprocess.run(
        ["codex", "exec", "--full-auto", "-s", "read-only", prompt],
        capture_output=True, text=True, cwd=cwd, timeout=timeout,
    ),
    "gemini": lambda prompt, cwd, timeout: subprocess.run(
        ["gemini", prompt],
        capture_output=True, text=True, cwd=cwd, timeout=timeout,
    ),
}


def run_persona(persona_key, question, provider_override=None, cwd=None, timeout=300):
    """Run a question through a persona's provider and return the response."""
    persona = PERSONAS[persona_key]
    provider = provider_override or persona["default_provider"]
    cwd = cwd or os.getcwd()

    full_prompt = (
        f"{persona['prompt']}\n\n---\n\n"
        f"You have access to the codebase in the current directory for context. "
        f"Read any files you need to give informed feedback.\n\n"
        f"Give your counsel on the following:\n\n{question}"
    )

    if provider not in PROVIDER_COMMANDS:
        return persona["name"], f"Unknown provider: {provider}"

    try:
        result = PROVIDER_COMMANDS[provider](full_prompt, cwd, timeout)
        output = result.stdout.strip()
        if result.returncode != 0 and not output:
            output = f"[Error exit {result.returncode}]: {result.stderr.strip()}"
        return persona["name"], output
    except subprocess.TimeoutExpired:
        return persona["name"], f"[Timed out after {timeout}s]"
    except FileNotFoundError:
        return persona["name"], f"[CLI '{provider}' not found — install it or override with --{persona_key}-provider]"


def main():
    parser = argparse.ArgumentParser(
        description="Consult your AI counsel: Cato (skeptic), Ada (optimist), Marcus (pragmatist)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "persona",
        choices=["cato", "ada", "marcus", "all"],
        help="Which persona to consult, or 'all' for the full counsel",
    )
    parser.add_argument("question", help="The question or topic to get counsel on")
    parser.add_argument("--cato-provider", default=None, choices=["claude", "codex", "gemini"])
    parser.add_argument("--ada-provider", default=None, choices=["claude", "codex", "gemini"])
    parser.add_argument("--marcus-provider", default=None, choices=["claude", "codex", "gemini"])
    parser.add_argument("--cwd", default=os.getcwd(), help="Working directory (default: current)")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per persona in seconds (default: 300)")

    args = parser.parse_args()

    targets = ["cato", "ada", "marcus"] if args.persona == "all" else [args.persona]
    overrides = {
        "cato": args.cato_provider,
        "ada": args.ada_provider,
        "marcus": args.marcus_provider,
    }

    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(
                run_persona, key, args.question, overrides[key], args.cwd, args.timeout
            ): key
            for key in targets
        }
        for future in as_completed(futures):
            name, response = future.result()
            results[name] = response

    # Print in consistent order
    for key in targets:
        name = PERSONAS[key]["name"]
        if name in results:
            print(f"\n{'=' * 60}")
            print(f"  {name}")
            print(f"{'=' * 60}\n")
            print(results[name])
            print()


if __name__ == "__main__":
    main()
