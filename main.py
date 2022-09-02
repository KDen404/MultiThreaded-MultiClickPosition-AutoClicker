# importing time and threading
import os
import time
import threading
import win32api
import win32con

click_positions = []
LShiftKey = 160
RShiftKey = 161
LControlKey = 162
RControlKey = 163

loop_click_positions_state = False
add_click_position_state = False
end_application_state = False

LControlKey_parsed_state = False
create_fixed_reports_state = False


reportCount = 10000


def save_cursor_position_to_click_positions():
    global add_click_position_state
    x, y = win32api.GetCursorPos()
    click_position_dict = {
        "positionX": x,
        "positionY": y
    }
    print(x, y, "added to list")
    click_positions.append(click_position_dict)
    add_click_position_state = False


def click(position):
    x = position["positionX"]
    y = position["positionY"]
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def click_for_all_positions():
    for position in click_positions:
        time.sleep(0.1)
        click(position)


def get_click_position():
    return win32api.GetCursorPos()


def get_key_pressed(key):
    return win32api.GetKeyState(key)


def parse_key_state(state):
    key_states = {
        "pressed": state < -1,
        "toggled": state == 1,
    }
    return key_states


def keyboard_state_thread():
    global loop_click_positions_state
    global add_click_position_state
    global end_application_state
    global LControlKey_parsed_state
    global create_fixed_reports_state
    while not end_application_state:
        if parse_key_state(get_key_pressed(LControlKey))["pressed"]:
            if LControlKey_parsed_state != parse_key_state(get_key_pressed(LControlKey))["pressed"]:
                add_click_position_state = True
                LControlKey_parsed_state = True
        else:
            add_click_position_state = False
            LControlKey_parsed_state = False

        loop_click_positions_state = parse_key_state(get_key_pressed(LShiftKey))["pressed"]

        if parse_key_state(get_key_pressed(RControlKey))["pressed"]:
            end_application_state = True

        if parse_key_state(get_key_pressed(RShiftKey))["pressed"]:
            create_fixed_reports_state = True


def main():
    global loop_click_positions_state
    global add_click_position_state
    global end_application_state
    global create_fixed_reports_state
    while not end_application_state:
        if add_click_position_state:
            save_cursor_position_to_click_positions()

        if loop_click_positions_state:
            click_for_all_positions()

        if create_fixed_reports_state:
            for i in range(reportCount):
                x, y = get_click_position()
                click_position_dict = {
                    "positionX": x,
                    "positionY": y
                }
                click(click_position_dict)
                time.sleep(0.01)
            create_fixed_reports_state = False
            print(f"created {reportCount} report Dialogs!")

    print("application ended")


if __name__ == "__main__":
    t1 = threading.Thread(target=keyboard_state_thread)
    t2 = threading.Thread(target=main)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

exit(0)

