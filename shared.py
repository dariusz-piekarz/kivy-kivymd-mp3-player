from pandas import DataFrame


class Shared:
    update_bg = None
    update_details_data = None

    get_total_length = None
    update_current_pos = None
    max_slider_value = None
    slider_pos = None

    slider_val_update = None
    slider_change = None
    timer_beginning = None

    clear_music_data = None
    clear_timer = None
    pg_bar_clear = None
    clear_details = None

    loops = 0
    current_choice = 0
    folder_path = str()
    temp = str()
    index = 0
    fields = DataFrame(columns=['Path', 'Title', 'Author', 'Album'])
