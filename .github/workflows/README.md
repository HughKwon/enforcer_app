# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD automation.

## Available Workflows

### 1. `ci.yml` - Comprehensive CI Pipeline (Recommended)
**Triggers:** Push and PR to main/master/develop branches

**Features:**
- ✅ Runs tests on Python 3.10 and 3.11
- ✅ Generates coverage reports
- ✅ Uploads coverage to Codecov
- ✅ Code quality checks (Black, isort, Flake8)
- ✅ Test result summaries in PR comments

**Use this for:** Production-ready CI with full quality checks

---

### 2. `tests.yml` - PostgreSQL Integration Tests
**Triggers:** Push and PR to main/master/develop branches

**Features:**
- ✅ Runs tests against PostgreSQL database
- ✅ Generates coverage reports
- ✅ Comments coverage on PRs
- ✅ Archives HTML coverage reports

**Use this for:** Testing with production-like database setup

---

### 3. `tests-simple.yml` - Fast SQLite Tests
**Triggers:** Push and PR to main/master/develop branches

**Features:**
- ✅ Quick test execution with SQLite
- ✅ Basic linting checks
- ✅ Test summaries

**Use this for:** Quick feedback on every commit

---

## How to Use

### Choose Your Workflow

Pick one workflow to enable (delete the others or rename with `.disabled` extension):

**For most projects, use `ci.yml`** - it provides the best balance of speed and coverage.

### Add Status Badge to README

Add one of these badges to your main `README.md`:

```markdown
![Tests](https://github.com/YOUR_USERNAME/Enforcer_app/actions/workflows/ci.yml/badge.svg)
```

Replace `YOUR_USERNAME` with your GitHub username.

### Codecov Integration (Optional)

To enable Codecov coverage tracking:

1. Sign up at https://codecov.io with your GitHub account
2. Add your repository
3. No secrets needed - the GitHub token is automatically provided

### Viewing Results

- **In Pull Requests**: Check the "Checks" tab to see test results
- **In Actions Tab**: View detailed logs and download coverage reports
- **Coverage Reports**: Download HTML reports from workflow artifacts

## Workflow Configuration

### Customizing Triggers

Edit the `on:` section to customize when workflows run:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
```

### Python Versions

Modify the matrix strategy to test different Python versions:

```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']
```

### Environment Variables

Add secrets in GitHub repository settings (Settings → Secrets and variables → Actions):

```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}
```

## Troubleshooting

### Tests fail in CI but pass locally
- Check Python version matches
- Verify all dependencies in `requirements.txt`
- Check environment variables are set

### Workflow doesn't trigger
- Ensure workflow file is in `.github/workflows/`
- Check branch names match trigger configuration
- Verify YAML syntax is correct

### Coverage report missing
- Ensure `pytest-cov` is installed
- Check coverage files are generated before upload
- Verify artifact upload path is correct

## Best Practices

1. **Keep workflows fast** - Use caching for dependencies
2. **Run critical tests first** - Fail fast on important checks
3. **Use matrix builds sparingly** - Only test necessary Python versions
4. **Archive artifacts** - Save test reports for debugging
5. **Set appropriate retention** - Don't keep artifacts forever

## Example PR Workflow

When you create a PR:

1. ✅ All workflow checks run automatically
2. ✅ Status badges appear in the PR
3. ✅ Coverage changes are commented
4. ✅ Code quality issues are highlighted
5. ✅ Merge is blocked if tests fail (optional)

## Required Status Checks

To require passing tests before merge:

1. Go to repository Settings → Branches
2. Add branch protection rule for `main`
3. Enable "Require status checks to pass before merging"
4. Select the workflows you want to require
