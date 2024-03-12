from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from shared import Shared


class ListPlayer(MDBoxLayout):
    selection = 0

    def __init__(self, **kwargs):
        super(ListPlayer, self).__init__(**kwargs)
        self.data_tables = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            use_pagination=False,
            rows_num=100,
            check=False,

            column_data=
            [
                ["No.", dp(10)],
                ["Title", dp(15)],
                ["Author", dp(25)],
                ["Album", dp(25)]
            ],
            row_data=[],
        )
        self.add_widget(self.data_tables)
        self.data_tables.bind(on_row_press=self.on_row_press)

    def update_size(self, width, scale_width=1.0):
            self.remove_widget(self.data_tables)
            self.data_tables.bind(on_row_press=self.on_row_press)

            self.data_tables = MDDataTable(
                pos_hint={'center_x': 0.5, 'center_y': 0.5},
                use_pagination=False,
                check=False,
                rows_num=100,
                column_data=
                [
                 ["No.", dp(width * scale_width / 33)],
                 ["Title", dp((width * scale_width) / 16)],
                 ["Author", dp((width * scale_width) / 16)],
                 ["Album", dp((width * scale_width) / 16)]
                ],
                row_data=[[Shared.fields.index[no],
                           Shared.fields.at[no, 'Title'],
                           Shared.fields.at[no, 'Author'],
                           Shared.fields.at[no, 'Album']]
                          for no in range(len(Shared.fields['Title']))],
            )
            self.add_widget(self.data_tables)

    def add_row(self):
        last_row_no = len(Shared.fields['Title'])-1
        self.data_tables.add_row((Shared.fields.index[last_row_no],
                                  Shared.fields.at[last_row_no, 'Title'],
                                  Shared.fields.at[last_row_no, 'Author'],
                                  Shared.fields.at[last_row_no, 'Album']))

    def on_row_press(self, table, row):
        # get start index from selected row item range
        start_index, _ = row.table.recycle_data[row.index]["range"]
        self.selection = start_index

    def del_row(self):
        if len(self.data_tables.row_data) > 0:

            index_remove = (self.selection+1) // 4
            self.data_tables.remove_row(self.data_tables.row_data[index_remove])
            Shared.index = len(self.data_tables.row_data)

            for i in range(index_remove, len(self.data_tables.row_data)):
                row_to_modify = list(self.data_tables.row_data[i])
                row_to_modify[0] = i
                self.data_tables.row_data[i] = tuple(row_to_modify)

            return index_remove
        else:
            return -1

    def del_all_rows(self):
        self.data_tables.row_data = []
