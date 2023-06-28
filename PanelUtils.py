def add_label(item, text, enabled=True):
    item.separator(factor=1)
    row = item.row()
    row.enabled = enabled
    row.scale_y = 0.3
    row.label(text=text)

def add_simple_text(item, text):
    row = item.row()
    row.scale_y = 0.3
    row.label(text=text)