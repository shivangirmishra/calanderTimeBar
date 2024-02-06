import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCalendarWidget, QVBoxLayout, QProgressBar, QLabel, QComboBox
from PyQt5.QtCore import QDate, QDateTime, QTimer, Qt

class CalendarApp(QWidget):
    def __init__(self):
        super().__init__()
        self.prev_progress_percentage = 0  # Initialize the variable here
        self.initUI()

    def initUI(self):
        # Create a calendar widget
        self.calendarWidget = QCalendarWidget(self)

        # Create a progress bar
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(1000)  # Increase precision
        self.progressBar.setFormat('%p%')  # Display percentage in the progress bar

        # Style the progress bar
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #000000;  /* Set a 1px black border */
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #007BFF;  /* Set the progress bar color to blue */
                width: 1px;  /* Set the width of the progress bar chunk */
            }
        """)

        # Create a label to display the time
        self.timeLabel = QLabel(self)
        self.timeLabel.setAlignment(Qt.AlignCenter)  # Align the text in the center
        self.timeLabel.setStyleSheet("font-size: 16px;")  # Set font size explicitly

        # Create a label to display the progress percentage
        self.percentLabel = QLabel(self)
        self.percentLabel.setAlignment(Qt.AlignCenter)  # Align the text in the center
        self.percentLabel.setStyleSheet("font-size: 16px;")  # Set font size explicitly

        # Create a dropdown button for selecting dark mode
        self.darkModeComboBox = QComboBox(self)
        self.darkModeComboBox.addItem("Light Mode")
        self.darkModeComboBox.addItem("Dark Mode")
        self.darkModeComboBox.currentIndexChanged.connect(self.toggle_dark_mode)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.calendarWidget)
        layout.addWidget(self.progressBar)
        layout.addWidget(self.percentLabel)
        layout.addWidget(self.timeLabel)
        layout.addWidget(self.darkModeComboBox)
        self.setLayout(layout)

        # Set window properties
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Year Progress Calendar')

        # Set up a timer to update the progress bar, time, and percentage every 100 milliseconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.timeout.connect(self.update_time)  # Connect the timer to update the time
        self.timer.start(100)  # Update every 100 milliseconds

        # Connect the date selection to update the progress bar
        self.calendarWidget.selectionChanged.connect(self.update_progress_bar)

        # Initialize the progress bar, time, and percentage
        self.update_progress_bar()
        self.update_time()

        # Set the initial font size and dark mode style
        self.setStyleSheet("""
            font-size: 16px;
            background-color: #ffffff;
            color: #000000;
        """)

        self.show()

    def update_progress_bar(self):
        # Calculate the percentage of the year passed
        current_datetime = QDateTime.currentDateTime()
        selected_date = self.calendarWidget.selectedDate()

        # Calculate the start and end of the selected year
        start_of_year = QDateTime(QDate(selected_date.year(), 1, 1))
        end_of_year = QDateTime(QDate(selected_date.year(), 12, 31))
        total_days_in_year = start_of_year.date().daysTo(end_of_year.date()) + 1  # Include the last day

        elapsed_days = start_of_year.date().daysTo(selected_date)
        progress_percentage = (elapsed_days / total_days_in_year) * 100

        # Set progress to 100% on December 31st
        if selected_date == QDate(selected_date.year(), 12, 31):
            progress_percentage = 100

        # Update the progress bar
        self.progressBar.setValue(int(progress_percentage * 10))  # Multiply by 10 for the progress bar's precision

        # Update the percentage label with higher precision
        self.percentLabel.setText(f"Progress: {progress_percentage:.10f}%")

        # Update the previous progress percentage
        self.prev_progress_percentage = progress_percentage

    def update_time(self):
        # Update the label with the current time
        current_time = QDateTime.currentDateTime().toString('hh:mm:ss')
        self.timeLabel.setText(f"Time: {current_time}")

    def toggle_dark_mode(self, index):
        # Get the selected item from the dropdown and toggle dark mode
        selected_item = self.darkModeComboBox.currentText()
        if selected_item == "Dark Mode":
            self.setStyleSheet("""
                font-size: 16px;
                background-color: #1e1e1e;
                color: #ffffff;
            """)
        else:
            self.setStyleSheet("""
                font-size: 16px;
                background-color: #ffffff;
                color: #000000;
            """)  # Use the default style


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalendarApp()
    sys.exit(app.exec_())
