# Auto-Schedule

A simple web application that automatically generates employee schedules for a week.

## Features

- Add employees and specify their maximum hours per week.
- Record employee availability for each day and shift.
- Process time-off requests.
- Generate weekly schedules that balance hours and avoid overtime.

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

Data is stored in memory for simplicity and will reset each time the app restarts.
