from pygame import mixer

class Music:
    def __init__(self) -> None:
        mixer.init()

    def play_music(self):
        file = 'music\Indila_-_Ainsi_bas_la_vida_(NoniBase.Com).mp3'
        mixer.music.load(file, 'mp3')
        mixer.music.set_volume(0.3)
        mixer.music.play(-1)
        mixer.music.set_pos(60.2)
        if mixer.music.set_pos(67.8):
            mixer.music.rewind()
    
    def stop_music(self):
        mixer.music.stop()