def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.
    '''
    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global over90
    global over90_list
    global good_battery_health

    cur_time = 0
    good_battery_health = True
    cur_temp = 20.0
    cur_charge = 50.0
    over90_list = [-360, -360, -360]
    over90 = 0


def simulate_activity(activity, duration):
    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global over90
    global over90_list
    global good_battery_health
    for i in range(duration):
        cur_time += 1
        if activity == 'charge':
            if cur_charge < 80 and cur_temp < 40 and get_cur_battery_health():
                for j in range(3):
                    if cur_charge < 80:
                        cur_charge+= 1
                        cur_temp += 1/6
                    else:
                        cur_charge += 1/3
                        cur_temp += 1/12
            elif not get_cur_battery_health():
                if cur_charge > 80:
                    cur_charge = min(90, cur_charge +1)
                else:
                    cur_charge = min(80, cur_charge + 1)
                cur_temp += 0.25
            else:
                if cur_charge == 90:
                    over90 = 0
                    if cur_time - over90_list[0] < 360 and cur_time - over90_list[1] < 360:
                        over90_list[2] = cur_time
                    elif cur_time - over90_list[0] < 360:
                        over90_list[1] = cur_time
                    else:
                        over90_list[0] = cur_time
                    for k in over90_list:
                        if cur_time - k < 360:
                            over90 += 1
                if over90 >= 3:
                    good_battery_health = False
                    cur_temp += 1/4
                elif cur_charge < 100:
                    cur_charge += 1
                    cur_temp += 1/4
                else:
                    cur_temp += 1/4
                
        elif activity == 'idle':
            cur_charge -= 0.5
            cur_temp -= 1
        else:
            if cur_charge <= 0:
                cur_temp -= 1
            else:
                cur_temp += 1
            cur_charge -= 2

            
        
    cur_charge = max(0, min(100, cur_charge))
    cur_temp = max(0, cur_temp)
        
        


def duration_fast_charge_possible():
    dc = 80 - cur_charge
    dt = 40 - cur_temp
    if get_cur_battery_health():
        return max(0, min(dc/3, dt/0.5))
    return 0

def get_cur_temp():
    return round(cur_temp, 1)

def get_cur_charge():
    return round(cur_charge, 1)

def get_cur_battery_health():
    return good_battery_health

def charge_time_needed(minutes):
    ctot = 2*minutes
    return max(0, duration_fast_charge_possible() + ctot - cur_charge - duration_fast_charge_possible()*3)

if __name__ == '__main__':
    initialize()

    print(duration_fast_charge_possible()) # 10
    print(charge_time_needed(50)) # 30

    simulate_activity("charge",30)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 30

    simulate_activity("use",50)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 80

    simulate_activity("use",10)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 70

    simulate_activity("charge",100)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 95

    simulate_activity("idle",100)
    print(get_cur_charge()) # 50
    print(get_cur_temp()) # 0
    print(get_cur_battery_health()) # True
    print(duration_fast_charge_possible()) # 10

    simulate_activity("charge",80)
    print(get_cur_charge()) # 90
    print(get_cur_temp()) # 22.5
    print(get_cur_battery_health()) # False

    simulate_activity("use",40)
    print(get_cur_charge()) # 10
    print(get_cur_temp()) # 62.5

    simulate_activity("charge",80)
    print(get_cur_charge()) # 80
    print(get_cur_temp()) # 82.5

    initialize()
    # add your tests here
