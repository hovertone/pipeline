


a = {
    "vikingA": [
        {"shot_name": "SH_100", "f_start": "100", "f_end": "200"},
        {"shot_name": "SH_200", "f_start": "100", "f_end": "200"}],
    "vikingB": [
        {"shot_name": "SH_20", "frame_start": "20", "f_end": "50"},
        {"shot_name": "SH_300", "frame_start": "15", "f_end": "40"}]
    }



for i in a:
    print i
    for z in a[i]:
        print z['shot_name']