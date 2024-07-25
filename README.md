# FamTrust Backend API - Core

## Project Overview

This is the microservice for the FamTrust project that focuses and handles the core functionalities
of the project. The core functionalities include:

- Family Groups and Membership Management
- Family Accounts Management
- Family Transactions Management
- Fund Requests Management


Live link is at https://core.famtrust.biz/api/v1

Doc link at https://documenter.getpostman.com/view/14404907/2sA3kXCzfa

## Installation Instructions

### Prerequisites

Before setting up the project locally, ensure you have the following prerequisites installed:

- [Python](https://www.python.org/downloads/) (>=3.11.4)
- [Django](https://www.djangoproject.com/download/)
- [Django Rest Framework](https://www.django-rest-framework.org/#installation)
- A Database System (e.g., Postgres, MySQL, SQLite) - [Django Database Installation](https://www.djangoproject.com/download/#database-installation)

Ensure you follow the `env_file_template` to set the required variables

```
ENV=
FAMTRUST_SECRET_KEY=
DB_NAME=
DB_ENGINE=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
EXTERNAL_AUTH_URL=
API_VERSION=
PRODUCTION_URL=
PAGE_SIZE=
MAX_PAGE_SIZE=

```

### Installation Steps

1. Clone the repository:

        git clone https://github.com/InternPulse/famtrust-backend.git

2. Change into the parent directory:

        cd famtrust-backend

3. Set up a virtual environment:

        python3 -m venv venv

4. Activate your virtual environment:

        source venv/bin/activate

5. Install the Python dependencies:

        pip install -r requirements.txt

6. Create a .env file and set necessary secret keys below:

7. Apply migrations to create the database schema:

        python3 manage.py migrate

8. Start the development server:
    ```
    python3 manage.py runserver
    ```

The API should now be running locally at [http://localhost:8000/api/v1](http://localhost:8000/api/v1).


# Commit Standards

## Branches

- **dev** -> pr this branch for everything `backend` related
- **main** -> **don't touch** this branch, this is what is running in production!

## Contributions

famtrust-backend is open to contributions, but I recommend creating an issue or replying in a comment to let us know what you are working on first that way we don't overwrite each other.

## Contribution Guidelines

1. Clone the repo `git clone https://github.com/InternPulse/famtrust-backend.git`.
2. Open your terminal & set the origin branch: `git remote add origin https://github.com/InternPulse/famtrust-backend.git`
3. Pull origin `git pull origin dev`
4. Create a new branch for the task you were assigned to, eg `TicketNumber/(Feat/Bug/Fix/Chore)/Ticket-title` : `git checkout -b BA-001/Feat/Sign-Up-from`
5. After making changes, do `git add .`
6. Commit your changes with a descriptive commit message : `git commit -m "your commit message"`.
7. To make sure there are no conflicts, run `git pull origin dev`.
8. Push changes to your new branch, run `git push -u origin feat-csv-parser`.
9. Create a pull request to the `dev` branch not `main`.
10. Ensure to describe your pull request.
11. If you've added code that should be tested, add some test examples.


# Merging
Under any circumstances should you merge a pull request on a specific branch to the `dev` or `main` branch

### _Commit CheatSheet_

| Type     |                          | Description                                                                                                 |
|----------|--------------------------|-------------------------------------------------------------------------------------------------------------|
| feat     | Features                 | A new feature                                                                                               |
| fix      | Bug Fixes                | A bug fix                                                                                                   |
| docs     | Documentation            | Documentation only changes                                                                                  |
| style    | Styles                   | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)     |
| refactor | Code Refactoring         | A code change that neither fixes a bug nor adds a feature                                                   |
| perf     | Performance Improvements | A code change that improves performance                                                                     |
| test     | Tests                    | Adding missing tests or correcting existing tests                                                           |
| build    | Builds                   | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
| ci       | Continuous Integrations  | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
| chore    | Chores                   | Other changes that don't modify, backend or test files                                                      |
| revert   | Reverts                  | Reverts a previous commit                                                                                   |

> _Sample Commit Messages_

- `chore: Updated README file`:= `chore` is used because the commit didn't make any changes to the backend or test folders in any way.
- `feat: Added plugin info endpoints`:= `feat` is used here because the feature was non-existent before the commit.
