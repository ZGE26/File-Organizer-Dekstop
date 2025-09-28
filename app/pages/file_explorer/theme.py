THEME = """
    QWidget { background-color: #141414; color: #EDEDED; }
    QLabel#PathLabel { font-weight: 700; font-size: 16px; padding: 4px; }

    .QCard {
    background-color: #1E1E1E;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    }

    /* tombol icon */
    QToolButton {
    background: #222;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 0px;
    }
    QToolButton:hover { background: #2A2A2A; }
    QToolButton:pressed { background: #1A1A1A; }

    /* input */
    QLineEdit, QComboBox {
    background: #1C1C1C;
    border: 1px solid #2C2C2C;
    border-radius: 8px;
    padding: 6px 10px;
    selection-background-color: #4A90E2;
    }
    QComboBox::drop-down { border: none; width: 24px; }
    QComboBox QAbstractItemView {
    background: #1C1C1C;
    border: 1px solid #2C2C2C;
    selection-background-color: #303F9F;
    }

    /* list */
    QListWidget {
    background: #1A1A1A;
    border: 1px solid #2A2A2A;
    border-radius: 10px;
    padding: 6px;
    }
    QListWidget::item { padding: 8px 6px; }
    QListWidget::item:selected {
    background: #263238;
    border-radius: 6px;
    }
"""
