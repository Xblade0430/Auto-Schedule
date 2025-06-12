# Auto-Schedule
# Auto-Schedule

A simple web application that automatically generates employee schedules for a week.
The interface is styled with [Bootstrap](https://getbootstrap.com/) for a clean, professional look.

## Features

- Add employees and specify their maximum hours per week.
- Record employee availability for each day and shift.
- Process time-off requests.
- Generate weekly schedules that balance hours and avoid overtime using an AI solver (Google OR-Tools).
- Optionally generate a random schedule from available employees.
- Import employees, availability, and time-off information from Excel or PDF files.

## Quick Start

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the application:
   ```sh
   python app.py
   ```
3. Open your browser and navigate to `http://localhost:5000`.

Use the **Random Schedule** button on the home page to assign shifts randomly instead of using the AI solver.

The scheduler uses [Google OR-Tools](https://developers.google.com/optimization)
to intelligently assign shifts while balancing employee hours.

Imported Excel and PDF files are saved to `data/imports/` and automatically
loaded on startup so your employee data persists across restarts.

## Importing Data

You can upload an Excel (`.xlsx`) or PDF file containing employee details. The
file should contain the following columns/fields:

- **Name** – employee name
- **MaxHours** – optional maximum hours per week
- **Days** – comma separated available days (e.g. `Mon, Tue`)
- **Shifts** – comma separated available shifts (`morning`, `evening`, `night`)
- **TimeOff** – comma separated days off

Each row (or line in a PDF) creates/updates an employee with the provided
information. Uploaded files are kept in `data/imports/` so the scheduler can
reuse them when generating future schedules. Use the import form on the main
page to upload your file.

## Discord Bot

You can also control the scheduler from Discord. First set the `DISCORD_TOKEN`
environment variable to your bot token and run:

```sh
python bot.py
```

Commands use the `!` prefix:

- `!add_employee <name> [max_hours]`
- `!availability <emp_id> <day1,day2,...> <shift1,shift2,...>`
- `!time_off <emp_id> <day>`
- `!employees` list all employees
- `!schedule` display the generated schedule

## Chatbot Interface

The `/chat` page provides a simple conversation interface to set up employees and
generate a schedule. The bot stores your answers in `data/chat_state.json` so it
remembers what you entered.

Open `http://localhost:5000/chat` and follow the prompts:

1. Tell the bot what roles are needed each day.
2. List employees and their maximum hours.
3. Provide availability and any time off.
4. The bot will respond with the generated schedule.
5. End your message with a question mark or start with `search ` to let the bot
   look up answers online.

## AI Answers with OpenAI

If you set the `OPENAI_API_KEY` environment variable, the chatbot will use
[OpenAI](https://openai.com/) to answer questions. Without a key it falls back to
DuckDuckGo web search.

## Building a Productive AI Assistant

The project demonstrates a few core building blocks of an autonomous assistant:

1. **Language Model Integration** – handled in `ai_engine.py` which wraps the
   OpenAI API.
2. **Chat Interface** – provided by the Flask route `/chat` and the Discord bot
   in `bot.py`.
3. **Memory System** – conversation state is saved in `data/chat_state.json` so
   previous answers are remembered.
4. **Task Logic** – scheduling logic lives in `scheduler.py`, combining AI
   solvers with heuristics.
5. **Modular Design** – separate modules for the web app, Discord bot, chatbot
   and AI engine keep the codebase organized.

You can extend these pieces to create more advanced automation or connect to
other services (calendars, spreadsheets, etc.).

## AI Code Editor

You can ask the AI to modify files in this project. Run:

```sh
python code_editor.py path/to/file.py "Your instruction here"
```

The editor uses OpenAI to rewrite the file according to your instruction and
saves the updated content. Set the `OPENAI_API_KEY` environment variable before
running the command.