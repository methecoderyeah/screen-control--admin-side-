import tkinter as tk
from tkinter import ttk
from hovertext import HoverText


def df_to_treeview(window, df):
    # Outer container (background matches your app)
    outer = tk.Frame(
        window,
        bg="#BFDDF0",
        highlightthickness=0
    )

    # Inner rounded-corner illusion panel
    frame = tk.Frame(
        outer,
        bg="#BFDDF0",
        bd=0,
        highlightthickness=0
    )
    frame.pack(
        padx=56,   # 1.25x padding
        pady=12,
        ipadx=37,  # 1.25x internal padding
        ipady=12
    )

    # Treeview widget
    tree = ttk.Treeview(
        frame,
        columns=list(df.columns),
        show="headings",
        height=10
    )
    tree.grid(row=0, column=0, sticky="nw")

    # Scrollbars using plain tk.Scrollbar (so no theme colors)
    vsb = tk.Scrollbar(
        frame,
        orient="vertical",
        command=tree.yview,
        bg="#E3F2FD",
        activebackground="#E3F2FD",
        highlightthickness=0,
        bd=0
    )
    hsb = tk.Scrollbar(
        frame,
        orient="horizontal",
        command=tree.xview,
        bg="#E3F2FD",
        activebackground="#E3F2FD",
        highlightthickness=0,
        bd=0
    )

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # Correctly sized corner filler (fixes the blue square)
    corner = tk.Frame(frame, bg="#BFDDF0", width=24, height=24)
    corner.grid(row=1, column=1, sticky="nsew")

    # Prevent stretching
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_columnconfigure(0, weight=0)

    # Column widths (1.25x wider)
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=650, anchor="center")

    # Tooltip storage
    cell_tooltips = {}

    # Insert rows
    for _, row in df.iterrows():
        display_values = []

        for col, value in row.items():
            if isinstance(value, list):
                preview = value[:2]
                preview_str = str(preview)

                if len(value) > 2:
                    preview_str = preview_str[:-1] + ", ...]"

                display_values.append(preview_str)
            else:
                display_values.append(value)

        item_id = tree.insert("", "end", values=display_values)

        # Save tooltip text
        for col, value in row.items():
            if isinstance(value, list):
                col_index = list(df.columns).index(col)
                cell_tooltips[(item_id, col_index)] = str(value)

    # Tooltip tracking
    active_tooltip = {"obj": None}

    def on_motion(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            if active_tooltip["obj"]:
                active_tooltip["obj"].hide_tooltip()
                active_tooltip["obj"] = None
            return

        row_id = tree.identify_row(event.y)
        col_id = tree.identify_column(event.x)

        if not row_id or not col_id:
            return

        col_index = int(col_id[1:]) - 1
        key = (row_id, col_index)

        if key in cell_tooltips:
            text = cell_tooltips[key]

            if active_tooltip["obj"]:
                if active_tooltip["obj"].text == text:
                    return
                active_tooltip["obj"].hide_tooltip()

            active_tooltip["obj"] = HoverText(tree, text)
            active_tooltip["obj"].show_tooltip()

        else:
            if active_tooltip["obj"]:
                active_tooltip["obj"].hide_tooltip()
                active_tooltip["obj"] = None

    def on_row_click(event):
        tree = event.widget
        row_id = tree.identify_row(event.y)

        if row_id:
            user = tree.item(row_id, "values")
            user = user[0]
            print("Row clicked:", user)
            # function here eventually

    tree.bind("<ButtonRelease-1>", on_row_click)
    tree.bind("<Motion>", on_motion)

    return outer
