import win32com.client

def schedule_command(command, task_name, start_time):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    start_time = datetime.datetime.strptime(start_time, "%H:%M")
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M')
    TIME_TRIGGER_DAILY = 2
    trigger = task_def.Triggers.Create(TIME_TRIGGER_DAILY)
    trigger.StartBoundary = start_time_str
    trigger.DaysInterval = 1

    ACTION_EXEC = 0
    action = task_def.Actions.Create(ACTION_EXEC)
    action.Path = 'cmd'
    action.Arguments = '/c ' + command

    task_def.RegistrationInfo.Description = 'Scheduled task'
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False

    root_folder.RegisterTaskDefinition(task_name, task_def, 6, '', '', 3)

schedule_command('echo Hello, World!', 'My Task', '12:00')
