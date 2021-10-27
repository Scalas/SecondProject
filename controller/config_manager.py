from json import dump, load, JSONDecodeError


# config 파일의 내용을 불러와 geometry 값을 수정하여 저장
def set_geometry(geometry, is_maximized):
    with open('config.json', 'w+') as config_file:
        try:
            config = load(config_file)
        except JSONDecodeError:
            config = {}

        config['geometry'] = {
            'max': is_maximized,
            'x': geometry.x(),
            'y': geometry.y(),
            'height': geometry.height(),
            'width': geometry.width()
        }
        dump(config, config_file, indent=4)


# config 파일의 내용을 불러와 geometry 값을 읽어 리스트형태로 반환
def get_geometry():
    try:
        with open('config.json', 'r') as config_file:
            try:
                config = load(config_file)
            except JSONDecodeError:
                return None
    except FileNotFoundError:
        return None
    return [config['geometry'][key] for key in ['max', 'x', 'y', 'width', 'height']]
