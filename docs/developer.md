## Maintainer Documentation

### Running tests on github actions

For security reasons tests on github actions are not run automatically as soon as a new pull request is opened, but need to be labelled by a maintainer as `save_to_test`. Adding this label will retrigger the tests and show a link to the test run in the thread of the pull request.

### Create a new release

To make a new release of DigLabTools on github follow these steps:

- Ensure all tests are passing
- Check that the documentation is built correctly
- Create a commit on github to bump the version number in main to the release version, e.g. `0.3.0`
- Create a github tag pointing to that commit. This should automatically trigger the [github actions release workflow](https://github.com/INT-NIT/DigLabTools/blob/main/.github/workflows/release.yml) building and publishing the new version on PyPI.
- Test the new release by installing it from PyPI
- Create a commit on github to bump the version number to the next alpha version, e.g. `0.4.0-a.1`

