# Auto-Schedule

A simple web application that automatically generates employee schedules for a week.
The interface is styled with [Bootstrap](https://getbootstrap.com/) for a clean, professional look.

## Features

- Add employees and specify their maximum hours per week.
- Record employee availability for each day and shift.
- Process time-off requests.
- Generate weekly schedules that balance hours and avoid overtime using an AI solver (Google OR-Tools).

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

The scheduler uses [Google OR-Tools](https://developers.google.com/optimization)
to intelligently assign shifts while balancing employee hours.

Data is stored in memory for simplicity and will reset each time the app restarts.

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