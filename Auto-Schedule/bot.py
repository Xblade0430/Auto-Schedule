import os
import discord
from discord.ext import commands

from scheduler import Scheduler, Employee

bot = commands.Bot(command_prefix='!')

scheduler = Scheduler()

@bot.command(name='add_employee')
async def add_employee(ctx, name: str, max_hours: int = 40):
    scheduler.add_employee(Employee(name=name, max_hours=max_hours))
    await ctx.send(f"Added employee {name} with max {max_hours}h/week.")

@bot.command(name='availability')
async def availability(ctx, emp_id: int, days: str, shifts: str):
    day_list = [d.strip() for d in days.split(',') if d.strip()]
    shift_list = [s.strip() for s in shifts.split(',') if s.strip()]
    try:
        scheduler.update_availability(emp_id, day_list, shift_list)
        await ctx.send("Availability updated.")
    except ValueError as e:
        await ctx.send(str(e))

@bot.command(name='time_off')
async def time_off(ctx, emp_id: int, day: str):
    try:
        scheduler.request_time_off(emp_id, day)
        await ctx.send("Time off recorded.")
    except ValueError as e:
        await ctx.send(str(e))

@bot.command(name='schedule')
async def show_schedule(ctx):
    schedule = scheduler.generate_schedule()
    lines = []
    for day, shifts in schedule.items():
        shift_str = ', '.join(f"{s}: {shifts[s] or '-'}" for s in ['morning','evening','night'])
        lines.append(f"{day}: {shift_str}")
    await ctx.send('```\n' + '\n'.join(lines) + '\n```')

@bot.command(name='employees')
async def list_employees(ctx):
    if not scheduler.employees:
        await ctx.send("No employees.")
        return
    lines = [f"{e.id}: {e.name} ({e.max_hours}h)" for e in scheduler.employees]
    await ctx.send('```\n' + '\n'.join(lines) + '\n```')

if __name__ == '__main__':
    token = os.environ.get('DISCORD_TOKEN')
    if not token:
        raise SystemExit('DISCORD_TOKEN environment variable not set.')
    bot.run(token)