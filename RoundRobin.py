from tkinter import *
from PIL import ImageTk, Image
import copy


def update_queue(queue, n, max_processindex):
    beg_process = 0
    for i in range(n):
        # print("update")
        if queue[i] == 0:
            beg_process = i
            break

    queue[beg_process] = max_processindex + 1


def organize_queue(queue, n):
    i = 0

    while i < n-1 and queue[i+1] != 0:
        # print("organize")
        temp = queue[i]
        queue[i] = queue[i+1]
        queue[i+1] = temp

        i += 1


def process_arrival_check(queue, curr_time, arrival_time, n, max_processindex):
    if curr_time <= max(arrival_time):
        isArrived = False

        for j in range(n):
            # print("check")
            if arrival_time[j] <= curr_time:
                if j+1 not in queue:
                    max_processindex = j
                    isArrived = True

        if isArrived:
            update_queue(queue, n, max_processindex)


def Display_gantt(gant_timeline, gantt_process):
    print()
    print("GANTT Chart :: ")
    print(" ", *gantt_process, sep="   |   ", end="   |")
    print()
    print("GANTT Timeline :: ")
    print(*gant_timeline, sep="       ")


def display(n, arrival_time, burst_time, waiting_time, turn_around_time, exit_time):
    avg_wait_time = 0
    avg_turn_around_time = 0
    print()
    print("Process ID \t Arrival Time \t Burst Time \t Waiting Time \t Turn-Around Time")
    for i in range(n):
        print(
            f"\tP{i+1}\t\t{arrival_time[i]}\t\t{burst_time[i]}\t\t{waiting_time[i]}\t\t{turn_around_time[i]}")

        avg_wait_time += waiting_time[i]
        avg_turn_around_time += turn_around_time[i]

    print()
    print("Average Waiting Time :: ", avg_wait_time/n)
    print("Average Turn-Around Time :: ", avg_turn_around_time/n)


def solve(no_p, q, arrival_times, burst_times):
    curr_time = 0
    max_processindex = 0

    # quantum = int(input("Enter the Quantum value :: "))
    # n = int(input("Enter the number of processes :: "))
    quantum = int(q)
    n = int(no_p)

    waiting_time = [0 for _ in range(n)]
    turn_around_time = [0 for _ in range(n)]

    burst_time = copy.deepcopy(burst_times)
    arrival_time = copy.deepcopy(arrival_times)

    isComplete = [False for _ in range(n)]
    gant_process = []
    gant_timeline = [0]

    # for i in range(n):
    #     arrival_time.append(
    #         int(input(f"Enter the arrival time for process P{i+1} :: ")))
    #     burst_time.append(
    #         int(input(f"Enter the burst time for process P{i+1} :: ")))

    # arrival_time = [0, 0, 0, 0]
    # burst_time = [4, 1, 8, 1]

    temp_burst_time = copy.deepcopy(burst_time)

    queue = [0 for _ in range(n)]

    while curr_time < min(arrival_time):
        curr_time += 1

    if curr_time != 0:
        gant_timeline.append(curr_time)
        gant_process.append("Idle")

    temp = arrival_time[0]
    if arrival_time.count(temp) == len(arrival_time):
        for i in range(n):
            queue[i] = i+1
    else:
        queue[0] = arrival_time.index(min(arrival_time))+1

    while True:
        flag = True

        for i in range(n):
            if temp_burst_time[i] != 0:
                flag = False
                break

        if flag:
            break

        i = 0
        while i < n and queue[i] != 0:
            ctr = 0

            isExecuted = False
            while ctr < quantum and temp_burst_time[queue[0]-1] > 0:
                # print("hello")
                temp_burst_time[queue[0]-1] -= 1
                curr_time += 1
                ctr += 1

                process_arrival_check(
                    queue, curr_time, arrival_time, n, max_processindex)
                isExecuted = True

            if isExecuted:
                gant_process.append("P"+str(queue[0]))
                gant_timeline.append(curr_time)

            if temp_burst_time[queue[0]-1] == 0 and isComplete[queue[0]-1] == False:
                turn_around_time[queue[0]-1] = curr_time
                isComplete[queue[0]-1] = True

            idle = True
            if queue[n-1] == 0:
                j = 0
                while j < n and queue[j] != 0:
                    if isComplete[queue[j]-1] == False:
                        idle = False
                    j += 1
            else:
                idle = False

            if idle:
                curr_time += 1
                process_arrival_check(
                    queue, curr_time, arrival_time, n, max_processindex)

            if idle:
                gant_process.append("Idle")
                gant_timeline.append(curr_time)

            organize_queue(queue, n)

            i += 1

    exit_time = copy.deepcopy(turn_around_time)
    for i in range(n):
        turn_around_time[i] = turn_around_time[i] - arrival_time[i]
        waiting_time[i] = turn_around_time[i] - burst_time[i]

    Display_gantt(gant_timeline, gant_process)
    display(n, arrival_time, burst_time,
            waiting_time, turn_around_time, exit_time)

    display_gui(n, arrival_time, burst_time,
                waiting_time, turn_around_time, exit_time, gant_timeline, gant_process)


#--------------------------------------------------GUI STARTS HERE----------------------------------------------------#
root = Tk()
root.title("Round Robin Calculator")
frame = LabelFrame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)
frame.configure(bg='#569D04') #BG color     
      

# Quantum time
qtime = Entry(frame, width=5, borderwidth=3)
qtime.grid(row=0, column=1, padx=5, pady=10)
qtime_label = Label(frame, text="Enter the Quantum time value")
qtime_label.grid(row=0, column=0, padx=5, pady=10)
qtime_label.configure(bg='#B0FF55') #BG color

# Number of processes
no_p = Entry(frame, width=5, borderwidth=3)
no_p.grid(row=1, column=1, padx=5, pady=10)
no_p_label = Label(frame, text="Enter Total Number of Processes")
no_p_label.grid(row=1, column=0, padx=5, pady=10)
no_p_label.configure(bg='#B0FF55') #BG color

# read button
btn1 = Button(frame, text="Continue",
              padx=5, pady=5,bg='#B0FF55' ,command=lambda: read(int(no_p.get())))
btn1.grid(row=2, column=0, columnspan=1)

btn2 = Button(frame, text="Close",
              padx=5, pady=5,bg='#B0FF55', command=root.destroy)
btn2.grid(row=2, column=1, columnspan=1)


def calc(arr_var, burst_var):
    # print(*arr_var)
    # print(*burst_var)
    arrival_times = []
    burst_times = []

    for arrival in arr_var:
        if (arrival.get()).isnumeric():
            arrival_times.append(int(arrival.get()))
        else:
            arrival_times.append(0)

    for burst in burst_var:
        if (burst.get()).isnumeric():
            burst_times.append(int(burst.get()))
        else:
            burst_times.append(0)

    # print(*arrival_times)
    # print(*burst_times)

    q = qtime.get()
    n = no_p.get()

    solve(n, q, arrival_times, burst_times)


def read(n):
    arr_var = []
    burst_var = []

    readframe = Toplevel(frame, padx=10, pady=10)
    readframe.title("Reading values")
    readframe.configure(bg='#569D04') #BG colour

    for i in range(n):
        label1 = Label(
            readframe, text=f"Enter The arrival time of process {i+1}", padx=5, pady=5,bg='#B0FF55').grid(row=i, column=0)
        arrival = Entry(readframe, width=7, border=3)
        arrival.grid(row=i, column=1)
        
        
        label2 = Label(
            readframe, text=f"Enter The Burst time of process {i+1}", padx=10, pady=5,bg='#B0FF55').grid(row=i, column=3)
        burst = Entry(readframe, width=7, border=3)
        burst.grid(row=i, column=4)
        
        # print(arrival)
        # print(burst)

        arr_var.append(arrival)
        burst_var.append(burst)

    cnf = Button(readframe, text="Calculate",
                 command=lambda: calc(arr_var, burst_var))
    cnf.grid(row=n, column=3, sticky=W+E, columnspan=1, padx=5, pady=20)
    cnf.configure(bg='#B0FF55') #BG color

    diff = Button(readframe, text="Change num of process",
                  command=readframe.destroy)
    diff.grid(row=n, column=0, sticky=W+E, columnspan=1, padx=5, pady=20)
    diff.configure(bg='#B0FF55') #BG color

    clo = Button(readframe, text="Close", command=root.destroy)
    clo.grid(row=n, column=1, sticky=W+E, columnspan=1, padx=5, pady=20)
    clo.configure(bg='#B0FF55') #BG color


def display_gui(n, arrival_time, burst_time,
                waiting_time, turn_around_time, exit_time, gant_timeline, gant_process):

    # ANS Frame
    ansframe = Toplevel(frame, padx=10, pady=10)
    ansframe.title("ANSWER")
    ansframe.configure(bg='#569D04') #BG color

    # Gantt process
    process_label = Label(
        ansframe, text="Gantt Processess : : ", font=('Arial', 10, 'bold'))
    process_label.grid(row=0, column=0, columnspan=1)
    process_label.configure(bg='#B0FF55') #BG color
    
    for i in range(len(gant_process)):
        process = Entry(ansframe, fg="blue", font=(
            'Arial', 10, 'bold'),bg='#B0FF55', width=16)
        # print(process)
        process.grid(row=0, column=i+1, columnspan=1)
        process.insert(1, "            "+str(gant_process[i]))

    # Gantt timeline
    timeline_label = Label(
        ansframe, text="Gantt Timeline : : ", font=('Arial', 10, 'bold'))
    timeline_label.grid(row=1, column=0, columnspan=1)
    timeline_label.configure(bg='#B0FF55')
    for i in range(len(gant_timeline)):
        timeline = Entry(ansframe, fg="blue", font=(
            'Arial', 10, 'bold'),bg='#B0FF55', width=16)
        timeline.grid(row=1, column=i+1)
        timeline.insert(1, gant_timeline[i])

    # Displaying table

    tabulation = Label(ansframe, text="Tabulations",
                       font=('Arial', 10, 'bold', 'underline'))
    tabulation.grid(row=4, column=0, pady=10)
    tabulation.configure(bg='#B0FF55') #BG color
    
    titles = ["Process ID", "Arrival Time", "Burst Time",
              "Exit Time", "Waiting Time", "Turn-Around Time"]
    for i in range(len(titles)):
        table_label = Entry(ansframe, fg="red", font=(
            'Arial', 10, 'bold'),bg='#B0FF55', width=16)
        table_label.grid(row=5, column=i, columnspan=1)
        table_label.insert(1, titles[i])

    list = []
    avg_wt_time = 0
    avg_tat_time = 0
    for i in range(n):
        list.append(["P"+str(f"{i+1}"), arrival_time[i], burst_time[i],
                    exit_time[i], waiting_time[i], turn_around_time[i]])

        avg_wt_time += waiting_time[i]
        avg_tat_time += turn_around_time[i]

    rows = len(list)
    columns = len(list[0])

    for i in range(rows):
        for j in range(columns):
            e = Entry(ansframe, fg="blue", font=(
                'Arial', 10, 'bold'), width=16)
            e.grid(row=i+6, column=j, columnspan=1)
            e.insert(1, list[i][j])
            e.configure(bg='#B0FF55') #BG color

    avg_wt_label = Label(ansframe, text="Average Waiting Time = " +
                         str(avg_wt_time/n), font=('Arial', 10, 'bold', 'underline'))
    avg_wt_label.grid(row=6+n, column=0, pady=5, columnspan=3)
    avg_wt_label.configure(bg='#B0FF55') #BG color
    
    avg_tat_label = Label(ansframe, text="Average Turn Around Time = " +
                          str(avg_tat_time/n), font=('Arial', 10, 'bold', 'underline'))
    avg_tat_label.grid(row=7+n, column=0, pady=5, columnspan=3)
    avg_tat_label.configure(bg='#B0FF55') #BG color

    close = Button(ansframe, text="Close!", command=ansframe.destroy)
    close.grid(row=8+n, column=0, padx=10, pady=10)
    close.configure(bg='#B0FF55') #BG color

root.mainloop()
