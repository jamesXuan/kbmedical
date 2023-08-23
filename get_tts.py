from aip import AipSpeech
import pygame, time
file_path = './output_file/'

def get_mp3file(text):
    APP_ID = '16374578'
    API_KEY = 'M1jGasw2GWfNqGTiy5i6S11A'
    SECRET_KEY = 'fiIdhkysjnAMkpnaQjPZj19sRPHozbAB'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text,'zh',1,{'vol':5,})
    tmp_name = ''
    for i in range(5):
        tmp_name = tmp_name + text[i]
    file_name = file_path+tmp_name+'.mp3'
    if not isinstance(result, dict):
        with open(file_name, 'wb') as f:
            f.write(result)
    return file_name

def mp3_play(text_length, file_name):
    pygame.mixer.init()
    track = pygame.mixer.music.load(file_name)
    pygame.mixer.music.play()
    sleep_time = int((10/35)*text_length)
    time.sleep(sleep_time)
    pygame.mixer.music.stop()

if __name__ == '__main__':
    text = '您好，我是您的医药智能助理，希望可以帮到您！'
    file_name = get_mp3file(text)
    mp3_play(len(text), file_name)