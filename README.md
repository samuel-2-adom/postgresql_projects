# PostgreSQL Projects

This repository contains two small Python command-line applications that use PostgreSQL for data persistence:

- Contact Book: manage personal contacts, favorites, and search/filter operations
- Expense Tracker: log expenses, assign categories, and view summaries by category or date

Both applications are built as interactive terminal interfaces and initialize their required database tables automatically.

## Project structure

```text
postgresql_projects/
├── .gitignore
├── contact_book/
│   ├── main.py
│   └── util/
│       ├── __init__.py
│       ├── contact_book.py
│       ├── database.py
│       └── render_screen.py
├── expense_tracker/
│   ├── main.py
│   └── util/
│       ├── __init__.py
│       ├── database.py
│       ├── expense_categories.py
│       ├── expense_tracker.py
│       └── render_screen.py
└── README.md
```

## Features

### Contact Book
- Add, update, and delete contacts
- Save contact notes
- Mark/unmark favorites
- Search by ID, name, phone number, or email
- View contact statistics

### Expense Tracker
- Add, update, and delete expenses
- Categorize transactions automatically from description text
- View all expenses or a single expense record
- Generate summaries by category and date

## Requirements

- Python 3.10+
- PostgreSQL server running locally or on a remote host
- The following Python packages:

```bash
pip install python-dotenv psycopg2 rich
```

## Database setup

Create a `.env` file in the repository root with your PostgreSQL connection details:

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
```

The applications read these environment variables from `dotenv` at runtime.

## Running the apps

### Contact Book

```bash
cd contact_book
python main.py
```

### Expense Tracker

```bash
cd expense_tracker
python main.py
```

When the app starts, it will initialize the required PostgreSQL tables automatically if they do not already exist.

## Notes

- The project is designed as a learning/demo project for working with PostgreSQL from Python.
- The interfaces are terminal-based and rely on the `rich` library for styling and rendering.
- Database schema and logic are stored separately in each app's `util/database.py` file.

## Example workflow

1. Start PostgreSQL and confirm your credentials are valid.
2. Create the `.env` file with your database settings.
3. Run either project from its folder.
4. Use the menu options to add, view, update, and manage records.

## License

This project does not currently include a license file. If you plan to share or distribute it publicly, consider adding an appropriate open-source license.
