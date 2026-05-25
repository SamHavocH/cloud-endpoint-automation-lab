# Branch Protection Policy

This repository uses a simple promotion model:

```text
feature branches -> develop -> main
```

## Policy

- `develop` represents the development environment.
- `main` represents production.
- Direct commits to `main` should be blocked.
- Pull requests into `main` must come from `develop`.
- The GitHub Actions job `Main merge policy` fails any pull request into `main` from another branch.

## Recommended GitHub Settings

Configure a branch protection rule for `main`:

- Require a pull request before merging.
- Require status checks to pass before merging.
- Require branches to be up to date before merging.
- Require the `Main merge policy` status check.
- Require the CI validation checks.
- Do not allow bypassing the above settings.
- Restrict who can push to matching branches, if available for the repository plan.

## GitHub CLI Example

After logging in with `gh auth login`, run:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/SamHavocH/cloud-endpoint-automation-lab/branches/main/protection \
  -f required_status_checks.strict=true \
  -f enforce_admins=true \
  -F required_pull_request_reviews='{"required_approving_review_count":1}' \
  -F restrictions='null' \
  -F required_status_checks.contexts[]="Main merge policy" \
  -F required_status_checks.contexts[]="Backend tests and lint" \
  -F required_status_checks.contexts[]="Dashboard syntax check" \
  -F required_status_checks.contexts[]="Docker Compose validation" \
  -F required_status_checks.contexts[]="Terraform format and validate"
```

GitHub branch protection blocks direct pushes. The source-branch rule is enforced by the `Main merge policy` GitHub Actions job.

## Branch Creation

Create and publish the development branch:

```bash
git checkout -b develop
git push -u origin develop
```
