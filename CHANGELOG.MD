# Change Log
All notable changes to this project will be documented in this file.

## [1.1.2] - 2025-07-25

### Added
- /ban command to ban users in chat.
- /stats can now show profiles of other users
- handlers/__init__.py added.

### Changed

### Fixed

## [1.1] - 2025-07-24

### Added
- db/db.py User Profiles. User profiles store OS, langauges, specs.
- /stats, /register. Register and show user statistics.
- utils/motivation.py Motivation quotes. Used in /stats to motivate and cheer up users

### Changed
- DatabaseManager added to work with new database structure to the following files:
 - handlers/balance
 - main.py

- Bot parsemode set to HTML
- requirements.txt updated

### Fixed