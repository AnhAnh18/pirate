import pygetwindow as gw
import pyautogui
import keyboard
import threading
from pynput.mouse import Listener

# Hàm lấy danh sách cửa sổ Chrome
def get_chrome_windows():
    all_windows = gw.getAllTitles()
    chrome_windows = [win for win in all_windows if "Chrome" in win]
    return chrome_windows

# Lắng nghe và đồng bộ click chuột
def listen_mouse_click(main_window, other_windows):
    def on_click(x, y, button, pressed):
        if pressed:  # Kiểm tra nếu nhấn chuột (click)
            try:
                # Kiểm tra nếu sự kiện xảy ra trên cửa sổ Chrome
                active_window = gw.getActiveWindow()
                if not active_window or "Chrome" not in active_window.title:
                    return  # Không xử lý sự kiện nếu không phải cửa sổ Chrome

                print(f"Toạ độ chuột: ({x}, {y})")

                # Lấy tọa độ cửa sổ chính
                main_window_obj = gw.getWindowsWithTitle(main_window)[0]
                main_rect = main_window_obj._rect
                offset_x, offset_y = x - main_rect.left, y - main_rect.top

                # Click trên cửa sổ chính
                pyautogui.click(x, y)

                # Đồng bộ click trên các cửa sổ khác
                for window in other_windows:
                    if gw.getWindowsWithTitle(window):  # Kiểm tra cửa sổ có tồn tại
                        win = gw.getWindowsWithTitle(window)[0]
                        win.activate()  # Kích hoạt cửa sổ phụ trước khi click
                        new_x = win.left + offset_x
                        new_y = win.top + offset_y
                        pyautogui.click(new_x, new_y)
            except Exception as e:
                print(f"Lỗi khi đồng bộ chuột: {e}")

    # Lắng nghe chuột chỉ trên cửa sổ Chrome
    with Listener(on_click=on_click) as listener:
        listener.join()

# Lắng nghe và đồng bộ phím
def listen_keyboard(main_window, other_windows):
    while True:
        event = keyboard.read_event()
        if event.event_type == "down":
            key = event.name
            try:
                # Đồng bộ phím trên cửa sổ chính
                print(f"Vừa nhấn nút: {key}")
                pyautogui.typewrite(key)
                # Đồng bộ phím trên các cửa sổ phụ
                for window in other_windows:
                    if gw.getWindowsWithTitle(window):  # Kiểm tra cửa sổ có tồn tại
                        win = gw.getWindowsWithTitle(window)[0]
                        win.activate()  # Kích hoạt cửa sổ phụ trước khi gửi phím
                        pyautogui.typewrite(key)
            except Exception as e:
                print(f"Lỗi khi đồng bộ phím: {e}")

# Chương trình chính
def main():
    # Lấy danh sách các cửa sổ Chrome
    chrome_windows = get_chrome_windows()
    if not chrome_windows:
        print("Không tìm thấy cửa sổ Chrome nào đang mở!")
        return

    print("Danh sách cửa sổ Chrome:")
    for i, title in enumerate(chrome_windows):
        print(f"{i + 1}. {title}")

    # Nhập số lượng cửa sổ muốn điều khiển
    num_windows = int(input(f"Bạn muốn điều khiển bao nhiêu cửa sổ? (tối đa {len(chrome_windows)}): "))
    if num_windows > len(chrome_windows):
        print("Số lượng vượt quá số cửa sổ đang mở, đặt lại thành tối đa.")
        num_windows = len(chrome_windows)

    # Chọn cửa sổ chính và phụ
    main_window = chrome_windows[0]  # Luôn lấy cửa sổ đầu tiên làm chính
    other_windows = chrome_windows[1:num_windows]

    print(f"Cửa sổ chính: {main_window}")
    print(f"Cửa sổ phụ: {other_windows}")

    # Tạo thread lắng nghe chuột và bàn phím
    mouse_thread = threading.Thread(target=listen_mouse_click, args=(main_window, other_windows))
    keyboard_thread = threading.Thread(target=listen_keyboard, args=(main_window, other_windows))

    # Khởi chạy
    mouse_thread.start()
    keyboard_thread.start()

    mouse_thread.join()
    keyboard_thread.join()

if __name__ == "__main__":
    main()
