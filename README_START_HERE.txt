PLAYSTATION UNIVERSE - READY WEB CATALOG

WHAT IS INCLUDED
- index.html: searchable web storefront
- catalog.json: 22,008 existing metadata listings (no package URLs)
- installer_games.json: initially empty installer package map
- authorized_packages.json: add legitimate homebrew package HTTPS links here
- tools/build_installer.py and .github/workflows/build-installer.yml: GitHub Actions generator

ANDROID SETUP
1. Extract this ZIP on your phone. Do NOT upload the ZIP as a file to the repository.
2. Upload index.html, catalog.json, authorized_packages.json, installer_games.json and README_START_HERE.txt to the repository root. Use desktop site if GitHub mobile upload fails.
3. Create tools/build_installer.py and .github/workflows/build-installer.yml using GitHub Add file > Create new file, then paste their contents.
4. In GitHub repo Settings > Pages choose Deploy from a branch, main / (root), Save.
5. Visit https://zezooth738-collab.github.io/PS4-Games-Installer-Catalog/ after deployment.
6. Add only authorized direct HTTPS homebrew PKG URLs to authorized_packages.json, commit, then run Actions > Build PS4 homebrew installer catalog.

IMPORTANT
This is a WEB catalog, not an installable PS4 PKG app. PS4 browser compatibility is not guaranteed. Game entries without authorized package links display Package not available. No commercial PKG downloads are bundled. Installer_games.json starts empty intentionally.
