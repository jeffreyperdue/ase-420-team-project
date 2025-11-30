# GitHub Pages Deployment Guide

This Hugo site is automatically deployed to GitHub Pages using GitHub Actions.

## Automatic Deployment

The site is automatically built and deployed when:
- Changes are pushed to the `main` branch
- Files in the `hugo-site/` directory are modified
- The workflow is manually triggered via GitHub Actions

## GitHub Pages Setup

1. **Enable GitHub Pages**:
   - Go to your repository settings
   - Navigate to "Pages" in the left sidebar
   - Under "Source", select "GitHub Actions"

2. **Verify Deployment**:
   - After pushing changes, check the "Actions" tab in your repository
   - The workflow should run automatically
   - Once complete, your site will be available at: `https://jeffreyperdue.github.io/ase-420-team-project/`

## Manual Deployment (if needed)

If you need to deploy manually:

1. Build the site:
   ```bash
   cd hugo-site
   hugo --minify
   ```

2. The `public/` directory contains the built site

3. You can manually push the contents of `public/` to a `gh-pages` branch, but the GitHub Actions workflow handles this automatically.

## Troubleshooting

### Site not updating

- Check the GitHub Actions workflow status
- Ensure files were modified in the `hugo-site/` directory
- Verify the baseURL in `hugo.toml` matches your GitHub Pages URL

### PDFs not loading

- Ensure PDFs are in `static/pdfs/` directory
- Verify all PDF links use `absURL` for absolute URLs
- Check that PDF filenames match exactly (case-sensitive)

### Build errors

- Ensure Hugo Extended version is 0.128.0 or later
- Check that all required files are present
- Verify `hugo.toml` syntax is correct

## Workflow Details

The GitHub Actions workflow (`.github/workflows/hugo.yml`) performs the following:

1. Installs Hugo Extended
2. Checks out the repository
3. Builds the Hugo site with minification
4. Uploads the built site as an artifact
5. Deploys to GitHub Pages

The workflow runs in the `hugo-site/` directory to ensure proper context.

