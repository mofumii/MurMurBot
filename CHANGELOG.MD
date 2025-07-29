# Change Log
All notable changes to this project will be documented in this file.

## [1.2.1] - 2025-07-29
### Added
- handlers/captcha.py Adds new users to the databaser after completing captcha.

### Changed
- requirements.txt updated.

### Removed
- db/db.py get_user_points dublicate removed.

## [1.2] - 2025-07-26
### Added
- handlers/chatbot.py Chatbot with a friendly persona who talks to chat members.
- utils/gpt.py Chatbot API handler to send prompts to OpenAI.

## [HOTFIX 1.1.5] - 2025-07-26
### Changed
- utils/user.py fetch_user_avatar removed because it caused errors

### Fixed
- handlers/stats.py stats_handler loads user avatar properly and notifies user if error occured

## [1.1.4] - 2025-07-26
### Fixed
- utils/user.py fetch_user_avatar Error handling if user avatar not found and blank pfp not found


## [1.1.3] - 2025-07-25

### Added
- Captcha for new users in group chats. Passed by clicking inline button

### Changed
- handlers/stats.py Sends default profile picture if user does not have one

### Fixed
- utils/user.py get_user_pfp Error handling: Returns exception if cannot get user avatar.

## [1.1.2] - 2025-07-25

### Added
- /ban command to ban users in chat.
- /stats can now show profiles of other users
- handlers/__init__.py added.

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