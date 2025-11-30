# Hugo Site for ASE 420 Team Project

This directory contains the Hugo static site for the ASE 420 Team Project GitHub Pages site.

## Local Development

### Prerequisites

- [Hugo Extended](https://gohugo.io/installation/) (version 0.128.0 or later)
- Git

### Running Locally

1. Navigate to the hugo-site directory:
   ```bash
   cd hugo-site
   ```

2. Start the Hugo development server:
   ```bash
   hugo server
   ```

3. Open your browser and navigate to `http://localhost:1313/ase-420-team-project/`

   Note: The site will be available at the baseURL path to match GitHub Pages.

### Building for Production

To build the site for production:

```bash
hugo --minify
```

The generated site will be in the `public/` directory.

## Project Structure

```
hugo-site/
├── content/           # Content files (markdown)
│   ├── documentation/ # Documentation section
│   └── about.md      # About page
├── themes/           # Custom theme
│   └── project-theme/
│       ├── layouts/  # HTML templates
│       └── static/   # CSS and static assets
├── static/           # Static files (PDFs, images)
│   └── pdfs/         # PDF documents
├── hugo.toml         # Hugo configuration
└── README.md         # This file
```

## Adding New PDFs

1. Copy your PDF file to `static/pdfs/`
2. Add a new document item in `themes/project-theme/layouts/documentation/list.html`
3. Follow the existing pattern for iframe and download link

## Configuration

The site is configured in `hugo.toml` with:
- Base URL: `https://jeffreyperdue.github.io/ase-420-team-project/`
- Theme: `project-theme`
- Menu items: Home, Documentation, About

## Deployment

The site is automatically deployed to GitHub Pages via GitHub Actions when changes are pushed to the `main` branch. See `DEPLOYMENT.md` for more details.

