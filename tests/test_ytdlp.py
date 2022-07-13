import yt_dlp
import json



def test_parse_json_and_update_progressbar(qtbot):
    from src.main import Window
    window = Window()
    qtbot.addWidget(window)

    with(open('../tests/d.json', 'r')) as f:  # get some sample data
        data = f.read()
        f.close()
    #d = json.load(str(data)
    parse_result = window.parse_json_and_update_progressbar(data)
    assert parse_result is not None
    assert parse_result is not None

