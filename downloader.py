import yt_dlp
import os

def show_credits():
    """Script එක පුරාම පෙන්වන ඔබේ විස්තර"""
    print("\033[1;32m" + "="*50)
    print("Developed By: \033[1;36mShenol Perera\033[0m")
    print("Visit Website: \033[4;34mhttps://shenolperera.wuaze.com/\033[0m")
    print("\033[1;32m" + "="*50 + "\033[0m")

def get_strings(lang):
    data = {
        'en': {
            'mode': "\nSelect Mode:\n1. Video (with Quality selection)\n2. Audio Only (MP3)",
            'input_url': "Paste YouTube URL: ",
            'checking': "\nChecking information...",
            'avail_quality': "--- Available Quality ---",
            'select_choice': "Select quality number: ",
            'downloading': "Downloading... (FFmpeg active)",
            'success': "✅ Success! Saved to Downloads folder.",
            'exit': "Press Enter to exit..."
        },
        'si': {
            'mode': "\nක්‍රමය තෝරන්න:\n1. වීඩියෝ (Quality තෝරාගත හැක)\n2. ඕඩියෝ පමණක් (MP3)",
            'input_url': "YouTube ලින්ක් එක මෙහි paste කරන්න: ",
            'checking': "\nතොරතුරු පරීක්ෂා කරමින් පවතී...",
            'avail_quality': "--- ලබාගත හැකි Quality වර්ග ---",
            'select_choice': "Quality අංකය ලබා දෙන්න: ",
            'downloading': "බාගත වෙමින් පවතී... (FFmpeg භාවිතා කරයි)",
            'success': "✅ සාර්ථකයි! Downloads folder එකට save විය.",
            'exit': "පිටවීමට Enter ඔබන්න..."
        },
        'ru': {
            'mode': "\nВыберите режим:\n1. Видео (с выбором качества)\n2. Только аудио (MP3)",
            'input_url': "Вставьте ссылку на YouTube: ",
            'checking': "\nПроверка информации...",
            'avail_quality': "--- Доступное качество ---",
            'select_choice': "Выберите номер качества: ",
            'downloading': "Загрузка... (FFmpeg активен)",
            'success': "✅ Успешно! Сохранено в папку Загрузки.",
            'exit': "Нажмите Enter, чтобы выйти..."
        }
    }
    return data.get(lang, data['en'])

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    show_credits()
    
    # 1. භාෂාව තෝරාගැනීම
    print("Select Language: 1. English | 2. Sinhala | 3. Russian")
    lang_choice = input("Choice: ").strip()
    lang_code = 'si' if lang_choice == '2' else ('ru' if lang_choice == '3' else 'en')
    txt = get_strings(lang_code)
    
    # 2. Mode එක තෝරාගැනීම (Video or Audio)
    print(txt['mode'])
    mode = input("Choice (1/2): ").strip()

    # 3. URL ලබාගැනීම
    url = input(f"\n{txt['input_url']}").strip()
    if not url: return

    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    try:
        print(txt['checking'])
        
        if mode == '2':  # Audio Only Mode
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        
        else:  # Video Mode
            with yt_dlp.YoutubeDL({'noplaylist': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])

            print(f"\n{txt['avail_quality']}")
            display_list = []
            seen_res = set()
            for f in formats:
                height = f.get('height')
                if height and f.get('vcodec') != 'none':
                    res = f"{height}p"
                    if res not in seen_res:
                        display_list.append(f)
                        seen_res.add(res)

            for i, f in enumerate(display_list):
                print(f"{i + 1}. {f['height']}p ({f['ext']})")

            choice = int(input(f"\n{txt['select_choice']}")) - 1
            selected_height = display_list[choice]['height']

            ydl_opts = {
                'format': f'bestvideo[height<={selected_height}]+bestaudio/best',
                'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'noplaylist': True,
            }
            
            print(f"\n{txt['downloading']}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        print(f"\n{txt['success']}")

    except Exception as e:
        print(f"\n{txt['error']}{e}")

    show_credits() # අවසානයටත් පෙන්වයි
    input(f"\n{txt['exit']}")

if __name__ == "__main__":
    main()