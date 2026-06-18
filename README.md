# Alejandro Mahillo's Academic Webpage

This is my personal academic website, built with [Jekyll](https://jekyllrb.com/) using the [Academic Pages](https://github.com/academicpages/academicpages.github.io) template (a fork of [Minimal Mistakes](https://mademistakes.com/work/minimal-mistakes-jekyll-theme/)).

If you want to create your own academic webpage, I highly recommend forking the [Academic Pages repository](https://github.com/academicpages/academicpages.github.io) — it's well-documented and easy to customize.

If you have any questions about my website, feel free to reach out at alejandro.mahillo@unican.es.

---

## Running locally with Docker

The easiest way to preview changes locally is using Docker.

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Step-by-step

1. **Clone the repository:**

   ```bash
   git clone https://github.com/alejandro-mahillo/alejandro-mahillo.github.io.git
   cd alejandro-mahillo.github.io
   ```

2. **Build and start the container:**

   ```bash
   docker compose up --build
   ```

   The first build will take a few minutes to download the Ruby image and install dependencies. Subsequent runs will be faster.

3. **View the site:**

   Open [http://localhost:4000](http://localhost:4000) in your browser.

4. **Stop the server:**

   Press `Ctrl+C` in the terminal, or run:

   ```bash
   docker compose down
   ```

The site auto-reloads when you make changes to any file (may take a few seconds).

---

## Forking my site (or the template)

If you want to use this site as a starting point for your own academic webpage:

1. Fork this repository (or the [Academic Pages template](https://github.com/academicpages/academicpages.github.io))
2. Clone your fork
3. Replace the content in `_pages/`, `_publications/`, `_talks/`, `_teaching/` with your own
4. Update `_config.yml` with your name, bio, social links, etc.
5. Replace the profile photo in `images/`
6. Test locally with Docker: `docker compose up --build`
7. Push to your GitHub repository

For GitHub Pages deployment, enable GitHub Pages in your repository settings (Settings → Pages → source: GitHub Actions). The included workflow file (`.github/workflows/jekyll.yml`) will build and deploy automatically.
