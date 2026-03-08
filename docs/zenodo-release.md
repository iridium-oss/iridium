# Zenodo Release and DOI

This document describes how to archive IRIDIUM on Zenodo and obtain a DOI for formal citation.

## GitHub-Zenodo Integration

1. Log in to [Zenodo](https://zenodo.org) and link your GitHub account.
2. In Zenodo, go to GitHub and enable the repository `iridium-oss/iridium`.
3. Zenodo will create a new archive (and assign a DOI) on each **GitHub release**. Draft releases are not archived.

## Reserving a DOI Before Publication

- Zenodo assigns the DOI when the first release is published. To reserve a DOI earlier, create a Zenodo deposit manually, upload a snapshot or tag, and use "Reserve DOI" before publishing the deposit.
- For automatic archiving on each release, the GitHub integration is sufficient; the DOI is assigned at first release.

## One-Step DOI Badge Activation

When a Zenodo DOI has been assigned (e.g. after the first GitHub release or after a manual deposit):

1. Note the DOI (e.g. `10.5281/zenodo.1234567`).
2. Add a Zenodo badge to the README badge block:
   `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)`
3. Replace XXXXXXX with your Zenodo record number.
4. Update docs/badges.md inventory and run `make verify-badges`.

Do not add a DOI badge with a placeholder or fabricated DOI. If no DOI exists yet, leave the badge out and document the activation step here.

## Metadata

The repository includes `.zenodo.json` at the root. Zenodo can use it to pre-fill metadata when creating a new version. Ensure `.zenodo.json` is consistent with CITATION.cff and README (title, description, authors, license, version). Update version in both when cutting a release.

## Release Checklist

See docs/release-checklist.md. Zenodo archival is one of the steps: create a GitHub release, wait for Zenodo to ingest it, then add the DOI badge if not already present.
