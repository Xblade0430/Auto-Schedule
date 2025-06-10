diff --git a/README.md b/README.md
index e7a157c9cc9074cef7cd8cb87f248e29709c4493..7aa8ef255d136a480b551385349fb9dc0ce77f95 100644
--- a/README.md
+++ b/README.md
@@ -1 +1,60 @@
-# Auto-Schedule
+# Auto-Schedule
+
+A simple web application that automatically generates employee schedules for a week.
+The interface is styled with [Bootstrap](https://getbootstrap.com/) for a clean, professional look.
+
+## Features
+
+- Add employees and specify their maximum hours per week.
+- Record employee availability for each day and shift.
+- Process time-off requests.
+- Generate weekly schedules that balance hours and avoid overtime using an AI solver (Google OR-Tools).
+- Import employees, availability, and time-off information from Excel or PDF files.
+
+## Quick Start
+
+1. Install dependencies:
+   ```sh
+   pip install -r requirements.txt
+   ```
+2. Run the application:
+   ```sh
+   python app.py
+   ```
+3. Open your browser and navigate to `http://localhost:5000`.
+
+The scheduler uses [Google OR-Tools](https://developers.google.com/optimization)
+to intelligently assign shifts while balancing employee hours.
+
+Data is stored in memory for simplicity and will reset each time the app restarts.
+
+## Importing Data
+
+You can upload an Excel (`.xlsx`) or PDF file containing employee details. The
+file should contain the following columns/fields:
+
+- **Name** – employee name
+- **MaxHours** – optional maximum hours per week
+- **Days** – comma separated available days (e.g. `Mon, Tue`)
+- **Shifts** – comma separated available shifts (`morning`, `evening`, `night`)
+- **TimeOff** – comma separated days off
+
+Each row (or line in a PDF) creates/updates an employee with the provided
+information. Use the import form on the main page to upload your file.
+
+## Discord Bot
+
+You can also control the scheduler from Discord. First set the `DISCORD_TOKEN`
+environment variable to your bot token and run:
+
+```sh
+python bot.py
+```
+
+Commands use the `!` prefix:
+
+- `!add_employee <name> [max_hours]`
+- `!availability <emp_id> <day1,day2,...> <shift1,shift2,...>`
+- `!time_off <emp_id> <day>`
+- `!employees` list all employees
+- `!schedule` display the generated schedule
