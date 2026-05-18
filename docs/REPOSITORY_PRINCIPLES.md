# Repository Principles

These principles guide all work in `cris-mcp-toolbelt` — by contributors,
maintainers, and AI coding agents. When a change conflicts with a principle, the
principle wins unless a maintainer documents an explicit exception.

The framing throughout is **configurable control, not crippled tools**.
Capabilities are classified, scoped, configured, activated, and audited — never
permanently excluded.

## 1. Public-Safe by Default

**What it means.** Everything committed to the repository is safe to publish. No
private project names, internal systems, machine-specific paths, or personal
infrastructure.

**Why it matters.** This is a public, community repository. A single leaked path
or internal name reduces trust and can expose information that should stay
private.

**Practical examples.**
- Use `{PROJECT_ROOT}`, `{WORKSPACE_ROOT}`, `{TARGET_REPOSITORY}`,
  `{USER_HOME}`, `{MCP_CONFIG_DIR}`, `{DATABASE_URL}`, `{POSTGRES_URL}`,
  `{MYSQL_URL}`, `{OLLAMA_BASE_URL}`, and `{GITHUB_TOKEN}` instead of real
  values.
- Reference example providers and example source URLs in catalog entries.

**What not to do.**
- Do not commit absolute paths from a contributor's machine.
- Do not name internal tools, employers, or private clients.

## 2. Configurable Control, Not Crippled Tools

**What it means.** MCP servers are powerful capability providers. The repository
makes their capabilities configurable and intentional — it does not frame them
as permanently dangerous, blocked, or crippled.

**Why it matters.** Users adopt the toolbelt to *use* MCP capability safely, not
to lose it. Conservative defaults plus clear activation paths serve them better
than exclusion.

**Practical examples.**
- Use language such as *controlled capabilities*, *high-impact capabilities*,
  *activation policy*, *scope controls*, and *profile-gated access*.
- A write-capable server is `inspect` or `readonly` by default and is activated
  through a profile, not removed.

**What not to do.**
- Do not overuse *dangerous*, *unsafe tool*, *crippled*, or *blocked forever*.
- Do not exclude a capability that can instead be scoped and gated.

## 3. Classify Every Capability

**What it means.** Every capability is assigned a capability class so risk is
described consistently across catalog entries, profiles, and docs.

**Why it matters.** Shared vocabulary makes capability comparable and lintable.

**Capability classes.**

| Class | Meaning |
| --- | --- |
| `passive` | Reads or inspects only |
| `interactive` | Interacts without mutation by default |
| `modifying` | Changes files, databases, repos, or app state |
| `executing` | Runs code, commands, or build tools |
| `administrative` | High-impact admin operations |

**What not to do.**
- Do not add a catalog entry without a `capability_class`.
- Do not record a modifying or executing capability as if it were passive.

## 4. Least Privilege by Default

**What it means.** Read-only and inspect modes are the baseline. Modifying,
executing, and administrative capability is separate, explicit, and documented.

**Why it matters.** Most AI-assisted workflows can be done safely with passive
capability. High-impact capability introduces real risk.

**Practical examples.**
- Filesystem and database access default to read-only or inspect.
- Command execution defaults to `disabled`.

**What not to do.**
- Do not enable modifying, executing, or administrative capability in a default
  or low-tier profile.

## 5. Profiles and Activation Policy Control Exposure

**What it means.** Capability is granted through named profiles paired with an
`activation_policy`, not through scattered configuration flags.

**Why it matters.** A named profile plus an explicit activation policy is
reviewable and auditable. Diffuse settings are not.

**Practical examples.**
- The seven profiles — `readonly-research`, `local-inspect`, `local-dev`,
  `sandbox`, `writer`, `executor`, `admin-controlled` — each describe a coherent
  capability level.
- High-impact entries declare `requires_confirmation`, `requires_allowlist`,
  `requires_scope_limit`, and `audit_required` as appropriate.

**What not to do.**
- Do not let a config template grant capability a profile does not allow.

## 6. Scope Controls for High-Impact Capability

**What it means.** Any capability that touches files, databases, commands,
browsers, or networks declares `scope_controls`.

**Why it matters.** Scope limits convert a broad capability into a bounded,
predictable one.

**Practical examples.**
- Filesystem write declares workspace path restrictions and blocked paths.
- Database access declares an SQL policy; command execution declares an
  allowlist; network access declares a public-URL policy.

**What not to do.**
- Do not catalog a high-impact server without scope controls.

## 7. Unknown Tools Belong in Sandbox

**What it means.** An MCP server that has not been reviewed is treated as
untrusted and is allowed only in the `sandbox` profile.

**Why it matters.** Unknown servers may access the filesystem, network, or shell
in ways that have not been examined. Sandbox isolation contains that risk.

**Practical examples.**
- New catalog entries start at trust level `unknown` or `experimental`.
- `allow_unknown_mcp` is `true` only for the sandbox profile.

**What not to do.**
- Do not add an unreviewed server to a non-sandbox profile.

## 8. No Secrets in Repository

**What it means.** The repository never contains real credentials — and never
contains placeholders crafted to look like real credentials.

**Why it matters.** Public git history is permanent. A committed secret is
compromised, and a realistic-looking fake trains bad habits.

**Practical examples.**
- Use `.env.example` with clearly non-secret placeholder values.
- Document where a real token would go without ever supplying one.

**What not to do.**
- Do not commit `.env`, tokens, keys, or connection strings.

## 9. Generic and Reusable Examples

**What it means.** Examples are written to be reused by anyone, in any
repository, without editing private details out first.

**Why it matters.** A toolbelt is only reusable if its examples are not tied to
one environment.

**What not to do.**
- Do not write an example that only works on the author's machine.
- Do not use destructive commands in examples.

## 10. Validation Before Trust

**What it means.** Catalog entries, profiles, and configuration are validated
against the schema before they are relied upon, and trust is earned through
review.

**Why it matters.** Standardized metadata is only useful if it is correct and
complete.

**Practical examples.**
- `validate_catalog.py` checks schema, enums, required fields, and profile
  references; `policy_lint.py` checks capability and activation consistency.
- Trust level promotion requires maintainer review.

**What not to do.**
- Do not mark an entry `trusted` because it "looks fine".

## 11. Activation Policy Is Intent, Not Runtime Enforcement

**What it means.** `activation_policy`, `scope_controls`, confirmation, and audit
fields describe how a capability *should* be activated. The repository does not
enforce them at runtime.

**Why it matters.** Claiming runtime enforcement the repository cannot deliver
would mislead users about their actual safety.

**Practical examples.**
- Documentation states that these fields are declarative and advisory.
- Configuration rendering translates intent into client config only as far as a
  target client supports it.

**What not to do.**
- Do not describe a profile or policy as if it technically blocks an action.

## 12. Documentation Before Complexity

**What it means.** Behavior is documented before it is automated, and automation
stays as simple as the task allows.

**Why it matters.** Documentation-first work keeps the repository understandable
and contributions reviewable.

**What not to do.**
- Do not introduce a dependency-heavy tool when a simple script is sufficient.

## 13. Community Contributions Require Review

**What it means.** Every contribution — especially catalog entries, profiles,
activation policy, and trust changes — is reviewed by a maintainer before merge.

**Why it matters.** A community catalog is trustworthy only if every entry
passed through review.

**Practical examples.**
- Catalog, profile, and capability changes require explicit security rationale.
- Trust promotion follows the lifecycle in
  [MAINTAINER_GUIDANCE.md](MAINTAINER_GUIDANCE.md).

**What not to do.**
- Do not self-merge a capability or trust change without review.
