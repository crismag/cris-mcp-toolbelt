# Release Checklist

Steps to cut a tagged release of `cris-mcp-toolbelt`. See
[MAINTAINER_GUIDANCE.md](MAINTAINER_GUIDANCE.md) for versioning guidance.

## 1. Validation

- [ ] `python3 scripts/validate_catalog.py` passes.
- [ ] `python3 scripts/validate_profiles.py` passes.
- [ ] `python3 scripts/policy_lint.py` passes.
- [ ] `bash scripts/doctor.sh` passes.
- [ ] `bash scripts/test_mcp_servers.sh` passes.
- [ ] `python3 -m pytest tests/ -q` passes.
- [ ] CI is green on the release commit.

## 2. Catalog and profiles

- [ ] Every published catalog entry describes a complete, deployable server.
- [ ] Catalog entries carry honest `trust_level` and `review_status` values;
      nothing is `trusted` or `approved` without maintainer review.
- [ ] All seven profiles are present and keep conservative defaults.

## 3. Public-safety

- [ ] No private project names, private paths, or internal system references.
- [ ] No secrets, credentials, or realistic-looking fake secrets.
- [ ] Generic placeholders are used throughout.
- [ ] `dev_plans/` and other internal-only material is not committed.

## 4. Documentation

- [ ] `README.md` is accurate and free of overclaiming.
- [ ] The seven core context documents are current.
- [ ] No unbuilt feature is described as if it were complete.
- [ ] Cross-document links resolve.

## 5. Version and history

- [ ] The version number follows the versioning guidance in
      MAINTAINER_GUIDANCE.md.
- [ ] `ROADMAP.md` reflects what is shipping and what is deferred.
- [ ] A changelog entry summarizes the release.

## 6. Tag

- [ ] Create the release tag on the validated commit.
- [ ] Confirm the tag points at a commit where CI is green.

## Notes

- An MCP server is published in the catalog only when it is complete and
  functional for deployment.
- Profiles, activation policy, and scope controls are declarative intent, not
  runtime enforcement — release notes must not claim otherwise.
