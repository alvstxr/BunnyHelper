# ouughh im importing iut , uim improtting it so good, itys everywher
import os
import json
import datetime
import time
import pytz
import tzlocal
import difflib
import threading
import signal
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt, Confirm
from rich import box
# from win10toast_click import ToastNotifier
from plyer import notification

console = Console()
# toaster = ToastNotifier()

DATA_DIR = "data"
CONFIG_FILE = os.path.join(DATA_DIR, "config.json") # watch antivirsus flag this shi now
BORDER_CHAR = "━"
BORDER_ICON = "🐇"
BORDER_STAR = "★"

os.makedirs(DATA_DIR, exist_ok=True) # imma assume this always works (it doesnt :pensive:) NVM IT DOES kinda?

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def transition(message="Loading", dots=3, delay=0.3):
    console.clear()
    for i in range(dots + 1):
        console.print(f"[bold cyan]{message}{'.' * i}[/bold cyan]", end="\r")
        time.sleep(delay)
    clear_screen()


def load_config():
    default_config = {
        "last_profile": None,
        "color": "purple",
        "font_style": "bold italic",
        "menu_color": "blue"
    }
    if not os.path.exists(CONFIG_FILE):
        save_config(default_config)
        return default_config
    else:
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
            if not isinstance(config, dict):
                raise ValueError("Invalid config")
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
        except:
            save_config(default_config) 
            return default_config
        
# why  isnt it saving? oh thats why
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_local_timezone():
    return tzlocal.get_localzone_name()

def validate_timezone(tz):
    if tz in pytz.all_timezones:
        return tz
    matches = difflib.get_close_matches(tz.capitalize(), pytz.all_timezones, n=1, cutoff=0.5)
    if matches:
        return matches[0]
    console.print(f"[red]Invalid timezone:[/red] '{tz}' is not recognized.") # now it doesnt crash anymore :huggyball: (it was this moment al knew that it did crash 5 times in a row bcs she wrote {z} instead of tz)
    return None

def get_profile_path(name):
    return os.path.join(DATA_DIR, f"profile_{name}.json")

def load_profile(name): # will it still load even if profi le is "1"? update: yes it did
    path = get_profile_path(name)
    if not os.path.exists(path):
        profile = {"groups": {}, "active_group": None, "name": name, "reminders": []}
        save_profile(profile)
    else:
        with open(path, "r") as f:
            profile = json.load(f)
    return profile

def get_next_task_id(profile):
    max_id = 0
    for group in profile["groups"].values():
        for task in group:
            try:
                task_id = int(task["id"])
                if task_id > max_id:
                    max_id = task_id
            except:
                continue
    return str(max_id + 1)

def save_profile(profile):
    path = get_profile_path(profile["name"])
    with open(path, "w") as f:
        json.dump(profile, f, indent=4)

def list_profiles():
    return [f[8:-5] for f in os.listdir(DATA_DIR) if f.startswith("profile_") and f.endswith(".json")]

def export_profile(profile): # hello Lee, i heard you like saving stuff :3 
    export_path = Prompt.ask("Enter export filename", default=f"{profile['name']}_export.json")
    with open(export_path, "w") as f:
        json.dump(profile, f, indent=4)
    console.print(f"Exported to [green]{export_path}[/green]") # for some whatever reason this print crashed the entire thing twice :sob: :sob:

def import_profile():
    try:
        path = Prompt.ask("Enter path to profile JSON")
        if not path:
            console.print("[red]No path provided.[/red]")
            return None
        with open(path, "r") as f:
            profile = json.load(f)
        save_profile(profile)
        console.print(f"Imported profile [cyan]{profile['name']}[/cyan]")
        return profile['name']
    except Exception as e:
        console.print(f"[red]Failed to import profile:[/red] {e}")
        return None

# this will flag so hard every antivirus known to man :sob: 
# update: I WAS FUCKING RIGHT, IT FLAGGED :sob:
def reminder_thread(title, description, seconds):
    def notify():
        time.sleep(seconds)
        try:
            notification.notify(
                title=f"Reminder: {title}",
                message=description,
                timeout=10
            )
        except Exception as e:
            console.print(f"[red]Notification error:[/red] {e}")
    threading.Thread(target=notify).start()


#        (\_/)
#        ( •_•)
#        / >🍪   this bunny is here to remind me 
#                  that no, i still haven't handled the borders

#                                                                               IM WORKING ON IT OKAY

#                                                                                                                                               i just forgot how to use border()

#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       yeah no i asked chatgpt bcs not even stack overflow was telling me

def draw_border(color):
    width = console.size.width
    side = (width - len(BORDER_ICON) - 2) // 2
    border = f"{BORDER_STAR}{BORDER_CHAR * side}{BORDER_ICON}{BORDER_CHAR * side}{BORDER_STAR}"
    console.print(f"[bold {color}]{border}[/bold {color}]")

def splash():
    from itertools import cycle

    rainbow_colors = ["red", "orange1", "yellow", "green", "blue", "magenta", "cyan"] # im gay :pensive_wobble_slow:
    color_cycle = cycle(rainbow_colors)

    logo = [
        r" ______ _   _ _   _  _   ___   __     _   _  _____ _     ______ ___________  ",
        r" | ___ \ | | | \ | || \ | \ \ / /    | | | ||  ___| |    | ___ \  ___| ___ \ ",
        r" | |_/ / | | |  \| ||  \| |\ V /     | |_| || |__ | |    | |_/ / |__ | |_/ / ",
        r" | ___ \ | | | . ` || . ` | \ /      |  _  ||  __|| |    |  __/|  __||    /  ",
        r" | |_/ / |_| | |\  || |\  | | |      | | | || |___| |____| |   | |___| |\ \  ",
        r" \____/ \___/\_| \_/\_| \_/ \_/      \_| |_/\____/\_____/\_|   \____/\_| \_| ",
    ]

    for line in logo:
        color = next(color_cycle)
        console.print(f"[bold {color}]{line}[/bold {color}]")

    console.print(f" ")
    console.print(f"[bold cyan]A TO-DO LIST BY THE BUN AL 🐇[/bold cyan]")
    console.print(f" ")
    console.print(f"[italic yellow]Your current timezone is:[/] [bold]{get_local_timezone()}[/bold]\n") # so people dont forget
    time.sleep(3)

def menu_box(title, options, config):
    try:
        draw_border(config["color"])
        content = "\n".join([f"[{i+1}] {opt}" for i, opt in enumerate(options)])
        panel = Panel(content, title=title, border_style=config.get("menu_color", "blue"), box=box.ROUNDED)
        console.print(panel)
        draw_border(config["color"])
        return Prompt.ask("Select option")
    except Exception as e:
        console.print(f"[red]Menu display error:[/red] {e}")
        return ""

def add_task(profile):
    console.print(f"[yellow]Current groups:[/yellow] {', '.join(profile['groups'].keys()) or 'None'}")
    group = Prompt.ask("Enter group")
    if group not in profile['groups']:
        profile['groups'][group] = []
    title = Prompt.ask("Title")
    description = Prompt.ask("Description")
    note = Prompt.ask("Note")
    deadline = Prompt.ask("Deadline (YYYY-MM-DD HH:MM)", default="")
    timezone = Prompt.ask(f"Timezone (Your current timezone is: {get_local_timezone()})", default=str(get_local_timezone()))
    timezone = validate_timezone(timezone)
    if not timezone:
        return
    priority = Prompt.ask("Priority (low, medium, high)", choices=["low", "medium", "high"], default="medium")
    emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(priority, "")
    task_id = get_next_task_id(profile)
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "note": note,
        "deadline": deadline,
        "timezone": timezone,
        "status": "Incomplete",
        "priority": priority,
        "emoji": emoji
    }
    profile['groups'][group].append(task)
    save_profile(profile)
    console.print(f"[green]Added task:[/] {emoji} {title}")

def list_tasks(profile): # FINALLY IT WORKS
    transition("Listing tasks")
    show_archived = Confirm.ask("Show archived tasks?", default=False)
    sort_by = Prompt.ask("Sort by", choices=["deadline", "priority", "status"], default="deadline")
    now = datetime.datetime.now(pytz.timezone(get_local_timezone()))
    def sort_key(task):
        if sort_by == "deadline":
            return (not task["deadline"], task["deadline"])
        elif sort_by == "priority":
            order = {"high": 0, "medium": 1, "low": 2}
            return order.get(task["priority"], 3)
        elif sort_by == "status":
            return task["status"]
        return task["title"]
    for group, tasks in profile["groups"].items():
        table = Table(title=f"[cyan]{group}[/cyan] Tasks")
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Priority")
        table.add_column("Status")
        table.add_column("Deadline")
        table.add_column("Timezone")
        table.add_column("Description")
        if t["status"] == "Archived" and not show_archived:
            continue
        for t in tasks:
            deadline_str = t["deadline"]
            overdue = False
            if deadline_str:
                try:
                    dt = datetime.datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
                    tz = pytz.timezone(t["timezone"])
                    dt = tz.localize(dt).astimezone(pytz.timezone(get_local_timezone()))
                    if dt < now:
                        overdue = True
                        # toaster.show_toast("Overdue Task", f"{t['title']} is overdue!", duration=5) # should i comment this and make a plyer notif?
                        notification.notify(title="Overdue Task", message=f"{t['title']} is overdue!", timeout=5) # the answer is yes

                except:
                    pass
            table.add_row(t["id"], t["emoji"] + " " + t["title"], t["priority"], t["status"], t["deadline"], t.get("timezone", ""), t.get("description", ""))
        console.print(table)
        tasks = sorted(tasks, key=sort_key)


def manage_task_status(task, profile):
    while True:
        transition("Opening Task Manager")
        option = menu_box(f"Task {task['id']}: {task['title']}", [
            "Mark as Incomplete",
            "Mark as Complete",
            "Mark as To Be Finished",
            "Set Reminder",
            "Edit Task",
            "Archive Task",
            "Delete Task",
            "Back"
        ], load_config())

        if option == "1":
            task['status'] = "Incomplete"
        elif option == "2":
            task['status'] = "Complete"
        elif option == "3":
            task['status'] = "To Be Finished"
        elif option == "4":
            console.print("[bold green]Set Reminder[/bold green]\n[italic]Use format like:[/] [cyan]30s[/cyan] (seconds), [cyan]5m[/cyan] (minutes), [cyan]2h[/cyan] (hours), [cyan]1d[/cyan] (days)")
            raw = Prompt.ask("Enter time (e.g., 30s, 5m, 2h, 1d)")
            try:
                unit = raw[-1].lower()
                if unit not in "smhd":
                    raise ValueError("Invalid unit")
                amount = int(raw[:-1])
                seconds = amount * {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
                if seconds <= 0:
                    raise ValueError("Time must be greater than 0")
                reminder_thread(task["title"], task["description"], seconds)
            except Exception as e:
                console.print(f"[red]Invalid format:[/red] {e}")
        elif option == "5": # edit
            console.print("[bold yellow]Edit Task[/bold yellow]")
            task["title"] = Prompt.ask("Title", default=task["title"])
            task["description"] = Prompt.ask("Description", default=task["description"])
            task["note"] = Prompt.ask("Note", default=task["note"])
            task["deadline"] = Prompt.ask("Deadline (YYYY-MM-DD HH:MM)", default=task["deadline"])
            tz = Prompt.ask("Timezone", default=task["timezone"])
            validated = validate_timezone(tz)
            if validated:
                task["timezone"] = validated
            task["priority"] = Prompt.ask("Priority (low, medium, high)", choices=["low", "medium", "high"], default=task["priority"])
            task["emoji"] = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(task["priority"], "")
            console.print("[green]Task updated successfully.[/green]")
        elif option == "6":  # archive
            task['status'] = "Archived"
            console.print("[cyan]Task archived.[/cyan]")
        elif option == "7":  # delete
            confirm = Confirm.ask(f"Delete task [red]{task['title']}[/red]?")
            if confirm:
                for group in profile['groups']:
                    if task in profile['groups'][group]:
                        profile['groups'][group].remove(task)
                        console.print("[red]Task deleted.[/red]")
                        save_profile(profile)
                        return
        elif option == "8":
                break
        save_profile(profile)
        transition("Applying changes")
        console.print(f"[cyan]Status updated to:[/cyan] {task['status']}")

def settings_menu(config):
    new_color = Prompt.ask("Border Color", default=config["color"])
    new_menu_color = Prompt.ask("Menu Color", default=config.get("menu_color", "blue"))
    VALID_COLORS = [
    "red", "purple", "green", "blue", "cyan", "magenta", "yellow", "white",
    "bright_red", "bright_green", "bright_blue", "bright_cyan",
    "bright_magenta", "bright_yellow", "bright_white", "black", "grey0", "navy_blue", 
    "dark_blue", "dark_green", "turquoise", "orange4"
    ]
    config["color"] = new_color if new_color in VALID_COLORS else config["color"]
    config["menu_color"] = new_menu_color if new_menu_color in VALID_COLORS else config["menu_color"]
    save_config(config)
# because of SOMEONE that wanted colored borders, yes im talking about you scarr >:(

def export_tasks_txt(profile):
    filename = Prompt.ask("Enter export filename", default=f"{profile['name']}_tasks.txt")
    lines = []
    for group, tasks in profile["groups"].items():
        lines.append(f"\n=== {group} ===\n")
        for t in tasks:
            lines.append(f"{t['emoji']} {t['title']}")
            lines.append(f"  Description: {t['description']}")
            lines.append(f"  Note: {t['note']}")
            lines.append(f"  Deadline: {t['deadline']} {t['timezone']}")
            lines.append(f"  Priority: {t['priority']}")
            lines.append(f"  Status: {t['status']}\n")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    console.print(f"[green]Tasks exported to[/green] {filename}")

def search_tasks(profile):
    query = Prompt.ask("Search for a task")
    results = []
    for group, tasks in profile["groups"].items():
        for task in tasks:
            if query.lower() in task["title"].lower():
                results.append((group, task))
            elif difflib.get_close_matches(query, [task["title"]], n=1):
                results.append((group, task))
    if not results:
        console.print("[red]No matches found.[/red]")
        return
    for group, task in results:
        console.print(f"[green]{task['id']}[/green] ({group}) - {task['emoji']} {task['title']}")

def task_menu(profile, config):
    while True:
        transition(f"Loading tasks for {profile['name']}")
        console.print(f"[bold]Active Profile:[/] [cyan]{profile['name']}[/cyan]") # "Active Profile" sounds like smth curseforge woudl say when loading a modpack
        option = menu_box("Tasks Menu", [
            "List Tasks",
            "Add Task",
            "Task Manager",
            "Search Tasks",
            "Settings",
            "Export Tasks (txt)",
            "Back to Profiles"
        ], config)
        if option == "1":
            list_tasks(profile)
        elif option == "2":
            add_task(profile)
        elif option == "3":
            task_id = Prompt.ask("Enter Task ID")
            for group in profile['groups']:
                for task in profile['groups'][group]:
                    if task['id'] == task_id:
                        manage_task_status(task, profile)
                        break
        elif option == "4":
            search_tasks(profile)
        elif option == "5":
            settings_menu(config)
        elif option == "6":
            export_tasks_txt(profile)
        elif option == "7":
            break


def profile_menu():
    config = load_config()
    while True:
        transition("Opening profile menu")
        option = menu_box("Profile Menu", [
            "Select Profile", "Create New Profile", "Import Profile", "Settings", "Manage Profiles", "Exit"
        ], config)

        if option == "1":
            names = list_profiles()
            if not names:
                console.print("[yellow]No profiles found[/yellow]")
                continue
            for i, name in enumerate(names):
                console.print(f"[{i+1}] {name}")
            idx = int(Prompt.ask("Pick profile number")) - 1
            if 0 <= idx < len(names):
                name = names[idx]
                config['last_profile'] = name
                save_config(config)
                profile = load_profile(name)
                task_menu(profile, config)
        elif option == "2":
            name = Prompt.ask("Profile name")
            profile = load_profile(name)
            config['last_profile'] = name
            save_config(config)
            task_menu(profile, config)
        elif option == "3":
            name = import_profile() # i may or may not have forgotten that its important to import profiles and not export only :FireTrans: :FireTrans: 
            if name:
                profile = load_profile(name)
                config['last_profile'] = name
                save_config(config)
                task_menu(profile, config)
        elif option == "4":
            settings_menu(config)
        elif option == "5":
            profiles = list_profiles()
            if not profiles:
                console.print("[yellow]No profiles found.[/yellow]")
                continue
            for i, name in enumerate(profiles):
                console.print(f"[{i+1}] {name}")
            idx = int(Prompt.ask("Select profile to manage")) - 1
            if 0 <= idx < len(profiles):
                selected = profiles[idx]
                sub = menu_box(f"Manage Profile: {selected}", ["Rename", "Delete", "Back"], config)
                if sub == "1":
                    new_name = Prompt.ask("New profile name")
                    old_path = get_profile_path(selected)
                    new_path = get_profile_path(new_name)
                    if os.path.exists(new_path):
                        console.print("[red]Profile with that name already exists.[/red]")
                    else:
                        os.rename(old_path, new_path)
                        if config.get("last_profile") == selected:
                            config["last_profile"] = new_name
                            save_config(config)
                        console.print(f"[green]Renamed profile to:[/] {new_name}")
                elif sub == "2":
                    confirm = Confirm.ask(f"Are you sure you want to delete profile [red]{selected}[/red]?")
                    if confirm:
                        os.remove(get_profile_path(selected))
                        if config.get("last_profile") == selected:
                            config["last_profile"] = None
                            save_config(config)
                        console.print(f"[red]Deleted profile:[/] {selected}")
        elif option == "6":
            break

def main():
    splash()
    transition("Opening profile menu")
    config = load_config()
    profile_menu()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda s, f: exit(0))
    main()





#%%%%###(#########(#################(##((***,,,,,,****,,,.......,*//////////////(#%&&%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%&&&&%%%&&&&&&&&&%%%%%%%%%%%%%%%%###########################(((((((((((((
###########%%%%%%%##%%%%%%%%%%%%%%%%####((//***,,*/*********,,,,,*////////(%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%&&&%%%%&&&&&&&&&&%%%%%%%%%%%%#######################################(((
#((((((((####%%%%%%%########%%#####%%####(#((///////////*********////((/#%&&&&%%%&&&&&&&&&&&&&&&&&&&&&&&&&%&&&&&&&&&&&&&&&&&&&&&&&&&&%%%&&&&&&%%%%%%%%%%%%###%%%########################################(
#(((((((((########################%%%%%%######(((((///********//(#%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%%&&&&&&&&&&&&&&&&&&&&&&&%&&&&&&%%%%%%%%%%%%%%%%%#######################################((((
###((((((((((((#######################%%###############(/////(#%%&&&&&&%%%%%%%%&&&&&&%&&&&&%%%%%%%%%%%%%%%%%&&&&&&&&&&&&%%%%%&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#######################################((((
#((((((((((#(((##########################################%%%&%%&%%%%%%%%%%%%%%%%%%%&%%%%%%%%%##(****,,,,,,,,*(/##%%&&&&&%%%%%%&%%%%%%%%%%%%%%%%%%%%%####################################################(
#**//######(##%%%%%%#######################%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%#(***/#%&&&&&%%/...//*,. .,//(&%%&%&&&&&&&%%%%%%%%%%%%%%%##########################################((###(######(
#(#/***(##%%###%%%%%%##%%%%###############%%%%%%%%%%%%%%%%%&%%%%%%%%%%%%%%%%&%&&%%%%%%#(**/(#%&&&&&%%%%%%%##%%%%(,.  .*/%%%&&&&&&%%%%%%%%%%%%%%###%%%%########################################(((((((((((
#*/(******(#%%%%#%%%%%%%%%%######(((######%%%%%%%%%%%%%%%%&&&&&%%%%%%%%%%%%%%%%%%%%%/*/(##%%&&&%#((///////////(((#/,.    *(/%%%%%%%%%%%%%%%%%%%###%%########################################(((((((((((((
#/#(//*,,,*(((##((##((/#%%%%%#((((#############%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(//(##%%&&&&%#(((/////((///////(((#/....  ./#%%%%%%%%%%%%%%%%%%%#%%###############################((#####(((((((((((((((
#(#%%%(/(*/#(*,(#((((//**/#%%%#((/(//((###########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#((##%%%&&&%%#((//////////////((///((%(*,... .,(%%%%%%%%%%#######%%%%###############################((((((((((((((((((((((
#(**###//**((/****###(/(#%%%%%#((((#%(*/(#####((###%%%%%%%%%%%%%%%%%%####%%%%%(/(##%#&&&&%%%%%%%%#(((((/////////(((((##(/,. ../(#%%%%%%%#########################################(##(((((((((((((((((((((
##(##(###((#%(**,*(/,*/(####(/(((#%%%%%#///((%#//(##%%%%%%%%%%%%###########(((///##%%&&&%##(((((###((((((((#%%%###%%###%#*,...,/#%%%%%%%%%##%%%############################((((##((((((((((((((((((((((((
#(#%#######%%%%#####/*/(######%%%%%%%#(/#(**/##(##((((#%%%%%%%%%########(#(/(//(((%%&&&%##((#%#%&%##((//(#%%%%####((((#&&%(*,...(##%%%%########################################((((((((((((((((((((((((((
#%%%%%%%########%#(/***/##########%%%#(***/(######((##(((((##############(/(//(((#%%&&&%#(((((((((((((//((###%%%###(((#%&&(*,.    ,/##%%%%%#(#%#########################(((((((((((((((((((((((((((//////
#%%%%%####(*/(###/**(#((((/((((/(/(((((#%%%/*((((########((%%%#////(#(/((///*//##%%%&&&##(((//////(((//((#((((((((///(#%&&(*,,...,**%%%%%%%####(#############(((((((((((((((((((((((((((((((((((/////****
#%%%%%######(#((##############/*(###(#%####%%#(**///(#%%%####%%%%#(/*/#(////**/(%%&&%%#((((((((((((#&#(#&###((///(((((#%%%#(,,,..,.*#%%%%%%%%%%((#######((###########((((((((((((((///((////((((/********
#%%%##########%%%%%%###%%%%%%###(##%%%%%%####%%%####**(##%%%%%%%%%%#*,/#####(((/####((((###((((#(((##%%###((#((((((((((#%%%%(*,....*,%%&%%%%%%%%#(######(((((######((((//(((((((((((((((((((((/((////((((
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###########%%%%%###(/,*/#%#(((###(((((((########%%%%%%%%##((#(#((#((((((/((##/,.....,*%%%%%%%%%%##(#((####((((((((((((((((((((#####((((((((((((///((((///
#%%%%%%%%%%%%%%%%%%%%%%%%%%%####%%%####%%%%%%%%%##(//#%%%%%%%%%%%%/*/*//(###(((##(((((((######%%%#####%&&%%%##((#((((((////((/,....*,(#%%%%%%%%#####((######(((((((((((((#####((((((((//((((((((////(((((
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%####((######%%%%%%#(#%%%%%%%%%%%%###%%%%#(((##%%#/((((####%##((((((#(######%%##((((((///////*,,...,**#%%%%%%########((((####(((((((####((###((((((((///////////(((((((((
#%%###%%%%%%%%%%%%%%%%%%%%%%%%#((((########(((#####%%%%%###(((((####%%%%%%((((###/(((((###%%##(((((((#(######%#((((((///*/*//*.....,,/#####################/**,,,,,,,,,,,,,,,,,,,,,,,,,,,,***///((((((/#&
#%%%%#(####%%%%%%%%%%%%%%%%%%%%%%%%##((//////(#########%######(((((###%%%#(*/((###((((##%%%%%##(/((((((#%###%%%%##(((///**///,......,,,,,,*/((##############%%%%%%%%%%#(*,,,,,,,.,,,....,,,,**,,*,,**//(#
########((((#%%%%%%%%%%%%&&&%#*****,**,**,*******,,,,,,,,,,,,**,,,//***#%%###(/(*%#####%%%####(//(/(#(###%&&&&&&%%#(((//*//*/*,...,,,****/////(((((########%%%%%%%%%&&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%##%%%#((#%%%%%%%%%%%%%#(*****/******,***********,****,,***,,*****/**/#(/(/(%%%%%%%%####((/((((((###%%&&&&&&%%##(/////*,*,*/(///##%%%%%%###%%#(((((((#%%%%%%%%%%%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#((////**(%#%##%%%%%%%%%%%%%%######%###%######%######################((((#(/,,*(%%&&&&&%%##(((((((((((####%%&&&&&&&%%%%##((**,,***(###%%%%%%%%%%%%#########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%((#(*/#####%%%%%%%%%%%%%%######################################/,,**(#####%%%%%%%%%%%%##(((((((########%&&&&&&&&&%%%%%%%%*,...,*(##%%%%%%%%%%%%%######%%%%%%%%%&&%%%%&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%%&
##((((/,,*##%%%%%%%%%%%%%%%%%###################################/##########%%%%%%%%%%%%%%&&&&&%&%#%%%#%%%%%&&&&&&&&&%%%%%%%%%%%##*/*,,,..*##%%%%%%%%%%%%%%%&%%%%%%%%&&%%%&&&%%&&%&&&&&%%%&&%%%%%%%%%%%%%&
#%%%%%(*(%%#(#%%%#%########(################################(*(##########%%%%%%%%%%%%%%%&%%&&&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%###((*/***..*#%%%%%%%%%%#%%&%%%%%%%%%%%%%%%%%&&&&&&&&&%&&&&%%%%&&&&&%%%&
#%%%%%#((((((((#%%%%%####################################################%%%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%#####//**,.*#%%%%####%%%%%%%%%%%%&&%&&&&&&&&&&&&&&&&&&%&&&&&&&&&&&&
#%%%%%%%%%%%%######(#%%###(############################################%%%%%%%%%%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&%%%%%%%%%%%%%%%%%%%%%%%%##%####(*,*%#####%%%%%%%%%%%%&%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
#%%%%%%%%%%%%%####%%%###%%%%%##%###########################%############%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%&&&%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%###(*.**###%%%%%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&%%&&
#%%%%%%%%%%%%%%####%%%%##%%%%%#%##################%%%#####%%%###########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*,##%%%%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%&%%
###%%%%%%%%%%%%#####(((((((####%###############%%%%%%%%##%#%#%%##########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*,(##%%%%%%%%%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&%#%
#%%%%%%%%%%%%%%####%%##########%%###%%###%%%%####%%%%%##%#%%#############%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,,########%%%&&&&&&&&&&&&&&@@@&&&&&&&&&&&&&&&&%##
#%%%%%%%%%%%%%###(###%%%%%%%%%#%%########################%%##%%%%########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.#%%%%%%%%%%%%%&&&&&&&&@@@@&&&&&&&&&&&&&&%%%%&&
#%%##########%%%%#####%%%#%%###%%#####################%%%%%%%%%#######%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,*%%%%%%%&&&&&&&&&@&&&&&&&&&&&&&&&&&&&%%%%%%&&&
#%##############(##(#(####((/(##%#%#####%%%############%%%%%%###########%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(,/&&&&&&&&@@@@@@@@&&&&&&&&&&&&&&&&&&%%%&&%%&&&
#*****,,,,,,,,,,,,,,,,,*/(((####%#%#######%##########%%%%%%%%#########%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(,%&&&&&&&&&@@@@@@@&&&&&&&&&&&&&&&&&&&%%%%%&&&
#,,,,,,,,,,,,,*//((((((((####(#%%###################%%%%%%%%#######%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%%%%%%%%%%%**&&&&&&&&&&&&&&@&&&&&&&&&&&&&&&&&&&&%%%&&&&&
#,,,,,**/(((((((((((((((((((((#%%#################%%%%%%%%%&%%####%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%&&%%%%&%%%%%%%%%%%%%#**&&&&&&&&&&&@@@&&&&&&&&&&&&&&&&&&&&%%%&&&&&
#((((((((((((((((((((((((((((##%%#%%##%%%%%%%%%##%%%%%%%%%%&%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&%%&&%%%%%%%%%%%%%%%(#&&&&&&&&&&&@@&&&&&&&&&&&&&&&&&&&&&%&&&&&&
#(((((((((((((((/((((((#####%%%%########%%%%%%%%%%%%%%%%%%%%##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&&&%&&&%%%%%%%%%%%%%%(,%&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&