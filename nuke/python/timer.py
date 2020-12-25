def wait_houdini_window():
    global app
    app = get_Houdini_Window()
    if not app:
        timerFilesSerch.start()
    else:
        active()

timerFilesSerch = QTimer()
timerFilesSerch.setSingleShot(True)
timerFilesSerch.setInterval(100)
timerFilesSerch.timeout.connect( wait_houdini_window )
timerFilesSerch.start()