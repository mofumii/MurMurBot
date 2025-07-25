# Change Log
All notable changes to this project will be documented in this file.

## [1.1.3] - 2025-07-25

### Added
- Captcha for new users in group chats. Passed by clicking inline button

### Changed
- handlers/stats.py Sends default profile picture if user does not have one

### Fixed
- utils/user.py get_user_pfp Error handling

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