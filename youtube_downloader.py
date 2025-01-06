import os
from pytubefix import YouTube
from pyffmpeg import FFmpeg
from moviepy import VideoFileClip, AudioFileClip

def baixar_video(link, resolution, only_video=bool):
    # get the stream 
    yt = YouTube(link)
    stream = yt.streams.filter(adaptive=True, mime_type="video/mp4", resolution=resolution).first()

    if only_video:
        stream.download()
    else:
        # download both video and audio
        downloaded_video = stream.download()
        os.rename(downloaded_video, "video.mp4")
        downloaded_audio = baixar_audio(link)
        os.rename(downloaded_audio, "audio.m4a")

        # combine both video and audio in one file
        video_clip = VideoFileClip("video.mp4")
        audio_clip = AudioFileClip("audio.m4a")
        final_clip = video_clip.with_audio(audio_clip)
        final_clip.write_videofile(downloaded_video)

        # remove video and audio parts
        os.remove("audio.m4a")
        os.remove("video.mp4")

def escolher_resolucao(link):
    yt = YouTube(link)
    stream = yt.streams.filter(adaptive=True, mime_type="video/mp4")
    resolution_list=[]
    for res in stream:
        if res.resolution not in resolution_list:
            resolution_list.append(res.resolution)
    
    for i, res in enumerate(resolution_list):
        print(f'[{i}] {res}')

    while True:
        try:
            opcao = int(input('Selecione a resolucao: '))
            if opcao not in range(len(resolution_list)):
                raise IndexError ('Error - Insira um numero valido')
        except IndexError as ie:
            print(ie)
        except ValueError:
            print('Error - Insira uma opcao valida')
        else:
            break

    return opcao, resolution_list

def baixar_audio(link, only_audio=False):
    yt = YouTube(link)
    stream = yt.streams.filter(mime_type="audio/mp4").first()
    downloaded_file = stream.download()
    if only_audio:
        converter_arquivo(downloaded_file, '.mp4')
    return downloaded_file

    # title = yt.title
    # os.rename(downloaded_file, f"{title}.mp4")

def converter_arquivo(file, sufix=str):
    inp = file
    out = file[:-4] + sufix
    
    
    ff = FFmpeg()
    try:
        ff.convert(inp, out)
    except:
        pass

    while True:
        try:
            opcao = input('Deseja remover o arquivo anterior: [S/N] ').strip().lower()[0]
            if opcao not in ('s', 'n'):
                raise ValueError ('Error - Insira \'s\' ou \'n\'')
            if opcao == 's':
                os.remove(file)
        except ValueError as ve:
            print(ve)
        else:
            break

def menu():
    link = input('Link: ')
    print('''
[0] Baixar vídeo completo
[1] Baixar áudio
[2] Baixar somente o video
''')
    while True:
        try:
            opcao = input('>>> ')
            if opcao not in ('0', '1', '2'):
                raise ValueError ("Escolha uma opção válida")
        except ValueError as ve:
            print(ve)
        else:
            break
    
    if opcao == '0':
        opcao, resolution_list = escolher_resolucao(link)

        resolution = resolution_list[opcao]
        baixar_video(link, resolution, False)
        
    if opcao == '1':
        baixar_audio(link, True)

    elif opcao == '2':
        opcao, resolution_list = escolher_resolucao(link)

        resolution = resolution_list[opcao]
        baixar_video(link, resolution, True)



menu()
input()
