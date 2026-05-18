# Maintainer Guidance

This guide is for maintainers of `cris-mcp-toolbelt`. It defines the review
processes that keep the repository safe, public-friendly, and trustworthy. It
builds on [GOVERNANCE.md](GOVERNANCE.md) and
[REPOSITORY_PRINCIPLES.md](REPOSITORY_PRINCIPLES.md).

## Maintainer Responsibilities

- Keep defaults conservative: read-only and inspect first, no unknown servers
  outside sandbox, no modifying/executing/administrative capability by default.
- Review every catalog, profile, capability, activation policy, and trust change
  before merge.
- Ensure no private references or secrets enter the repository or its history.
- Keep documentation accurate, public-safe, and free of overclaiming.
- Maintain the catalog schema, validation, and policy linting so they stay
  authoritative.
- Ensure controlled-capability language is used consistently.
- Cut releases against a documented checklist.

## Release Policy: Share When Done

An MCP server is shared publicly only when it is **complete and functional for
deployment**. Catalog entries are published when the server they describe is
finished and usable — not while it is still being built.

- Do not merge catalog entries for unfinished or non-deployable servers.
- In-progress MCP work stays out of the public repository until it is done.
- Before publishing an entry, confirm a user can deploy and run the server by
  following its `source_url` and documentation.
- Proposals for not-yet-complete servers belong in issues, not in merged catalog
  entries.

## Catalog Review Process

For each new or changed catalog entry, confirm:

1. All required fields are present and validation passes.
2. The server is complete and deployable (see Release Policy).
3. `source_url` and `homepage` are real and point to the server's source or
   documentation.
4. `license` is stated and consistent with public reuse.
5. `capability_class` is correct and `capabilities` /
   `controlled_capabilities` are complete and honest.
6. `activation_policy` is present for any high-impact capability, and
   `scope_controls` is present for any filesystem, database, command, browser,
   or network capability.
7. `default_access`, `trust_level`, `allowed_profiles`, and `review_status` are
   conservative and consistent — for example, an `unknown` entry is not
   allowlisted into `readonly-research`, and a `modifying` capability is gated
   to `writer` or `admin-controlled`.
8. `security_notes` lists realistic threats and concrete mitigations.

Reject entries with missing provenance, vague capability descriptions,
optimistic trust levels, or incomplete servers.

## Profile Review Process

For each profile change, confirm:

1. The change includes a written security rationale.
2. Defaults stay conservative: passive capability may be enabled where low-risk;
   modifying, executing, and administrative capability is not enabled by
   default.
3. `allow_unknown_mcp` is `true` only for the `sandbox` profile.
4. The profile fits the seven-profile model and its field set is consistent with
   other profiles and validates.
5. The intent and intended use are documented.

## Security Review Process

Treat every capability-affecting change as a security review:

- Identify what capability class the change exposes (`passive`, `interactive`,
  `modifying`, `executing`, `administrative`).
- Confirm high-impact capability is gated by a profile and an activation policy
  and is not on by default.
- Confirm `scope_controls` bound the capability and mitigations are documented.
- Confirm no secret, credential, or private reference is introduced.
- Remember that activation policy and scope controls are declarative intent, not
  runtime enforcement — review what the entry actually allows once configured.
- When in doubt, request a more restrictive default and ask the contributor to
  justify any escalation.

## Trust Level Promotion

Catalog entries move through a trust lifecycle:

```text
unknown -> experimental -> community -> trusted
```

- **unknown** — newly proposed; not reviewed; sandbox only.
- **experimental** — reviewed enough to try; still sandbox-oriented.
- **community** — reviewed, in use, with sound metadata; may be allowlisted into
  non-default profiles where appropriate.
- **trusted** — the highest level; broadly safe to recommend.

`trusted` must be difficult to earn. Promote to `trusted` only when **all** of
the following hold:

- Clear, verifiable source provenance and a stated license.
- The server is complete and deployable.
- Low-risk behavior: passive or tightly scoped, with no surprising filesystem,
  network, or shell access.
- Complete, accurate documentation, capability classification, and security
  notes.
- Review by a maintainer who did not author the entry.

A maintainer may also **demote** an entry if new information increases its risk.

## Review Status Lifecycle

Independently of trust level, a contribution moves through review states:

```text
proposed -> reviewed -> approved -> deprecated
```

- **proposed** — submitted, not yet reviewed.
- **reviewed** — examined; feedback given; not yet accepted.
- **approved** — accepted and merged.
- **deprecated** — superseded or no longer recommended; kept for history with a
  clear note.

## Handling Unsafe Contributions

- If a PR contains a secret or private reference, do not merge it; ask the
  contributor to remove it and, if already pushed anywhere, treat the value as
  compromised.
- If a change weakens defaults without justification, request changes rather
  than merging with a follow-up promise.
- If a catalog entry overclaims trust, safety, or completeness, downgrade it and
  ask for evidence.
- If an entry describes an unfinished server, hold it until the server is done.
- Document the reason for any rejection so the decision is reviewable.

## Release Preparation

Before tagging a release:

1. All catalog entries validate against the schema and pass policy linting.
2. Every published catalog entry describes a complete, deployable server.
3. All profiles validate and keep conservative defaults.
4. CI passes on the release commit.
5. Documentation is current, public-safe, and free of overclaiming.
6. The roadmap and changelog reflect what shipped.
7. The release checklist is completed and recorded.

## Versioning Guidance

The repository uses semantic-style versioning for a documentation-and-tooling
project:

- **Patch** — fixes, formatting, doc corrections, non-behavioral changes.
- **Minor** — new completed catalog entries, new profiles, new templates, new
  scripts that do not change existing conservative defaults.
- **Major** — changes that alter safety defaults, the catalog schema, the
  capability model, or profile semantics in a backward-incompatible way.

Pre-1.0 releases may still change shape, but conservative defaults should remain
across versions.

## Deprecation Policy

- Mark deprecated catalog entries and profiles with `review_status: deprecated`
  rather than deleting them immediately, so existing users are not surprised.
- State what replaces a deprecated item and when removal is expected.
- Remove deprecated items only in a minor or major release, never silently.

## Governance Notes

- Changes to profiles, capability metadata, activation policy, trust levels, or
  write permissions always require maintainer review with explicit security
  rationale.
- Maintainers should avoid self-merging their own capability or trust changes
  without a second reviewer where the project has more than one maintainer.
- Governance decisions and their rationale should be written down so the
  project's safety posture stays consistent over time.
