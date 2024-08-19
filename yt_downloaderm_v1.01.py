from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pytubefix import YouTube
from tkinter.messagebox import showinfo, showerror
import threading
import os
import subprocess
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re

# 創建主視窗
window = Tk()
window.title('YouTube Video DownloadErm')
window.geometry('600x600')

# 置中主視窗
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

window.resizable(height=FALSE, width=FALSE)

# 設置窗口圖標
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
window.iconbitmap(icon_path)

# 創建畫布
canvas = Canvas(window, width=600, height=600)
canvas.pack()

# 載入圖標
logo = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'Icon.png'))
logo_label = Label(window, image=logo)
canvas.create_window(300, 95, window=logo_label)

# 標籤和樣式
label_style = ttk.Style()
label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 15))
entry_style = ttk.Style()
entry_style.configure('TEntry', font=('Dotum', 15))
button_style = ttk.Style()
button_style.configure('TButton', foreground='#000000', font='DotumChe')

# 創建URL輸入框
url_label = ttk.Label(window, text='Enter Video URL:', style='TLabel')
url_entry = ttk.Entry(window, width=58, style='TEntry')
canvas.create_window(136.8, 200, window=url_label)
canvas.create_window(294, 230, window=url_entry)

# 創建解析度標籤和下拉框
resolution_label = Label(window, text='Resolution:')
canvas.create_window(70, 260, window=resolution_label)
video_resolution = ttk.Combobox(window, width=10, state='readonly')
canvas.create_window(84, 280, window=video_resolution)

# 創建選項按鈕
download_option = StringVar(value='video')
video_radio = Radiobutton(window, text='Video (MP4)', variable=download_option, value='video')
audio_radio = Radiobutton(window, text='Audio (MP3)', variable=download_option, value='audio')
canvas.create_window(480, 285, window=video_radio)
canvas.create_window(480, 315, window=audio_radio)

# 創建解析度搜索按鈕
search_resolution = ttk.Button(window, text='Search Resolution')
canvas.create_window(84, 315, window=search_resolution)

#存檔位置的按鈕
def select_save_path():
    path = filedialog.askdirectory()
    save_path_var.set(path)

save_path_label = ttk.Label(window, text='Select Save Location:', style='TLabel')
canvas.create_window(168, 350, window=save_path_label)
save_path_button = ttk.Button(window, text='Browse', command=select_save_path, style='TButton')
canvas.create_window(90, 375, window=save_path_button)
save_path_var = StringVar()
save_path_entry = ttk.Entry(window, textvariable=save_path_var, width=40, state='readonly')
canvas.create_window(330, 375, window=save_path_entry)

# 添加开始和结束时间的输入框
start_time_label = ttk.Label(window, text='Start Time:', style='TLabel')
canvas.create_window(109, 410, window=start_time_label)
start_time_entry = ttk.Entry(window, width=8, style='TEntry')
canvas.create_window(220, 410, window=start_time_entry)

end_time_label = ttk.Label(window, text='End Time:', style='TLabel')
canvas.create_window(400, 410, window=end_time_label)
end_time_entry = ttk.Entry(window, width=8, style='TEntry')
canvas.create_window(500, 410, window=end_time_entry)

# 創建處理方式的選項
process_option = StringVar(value='none')
process_radio1 = Radiobutton(window, text='No Processing', variable=process_option, value='none')
process_radio2 = Radiobutton(window, text='Quick Cut', variable=process_option, value='quick')
process_radio3 = Radiobutton(window, text='Detailed Cut', variable=process_option, value='detailed')
canvas.create_window(150, 460, window=process_radio1)
canvas.create_window(300, 460, window=process_radio2)
canvas.create_window(450, 460, window=process_radio3)

# 進度標籤和進度條
progress_label = Label(window, text='')
canvas.create_window(288, 500, window=progress_label)
progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=540, mode='determinate')
canvas.create_window(300, 524, window=progress_bar)

# 下載按鈕
download_button = ttk.Button(window, text='Download Video', style='TButton')
canvas.create_window(288, 560, window=download_button)


# 函數定義
def is_valid_time_format(time_str):
    # 使用正则表达式检查时间格式
    pattern = re.compile(r'^\d{2}:\d{2}:\d{2}$')
    if not pattern.match(time_str):
        return False
    
    # 检查小时、分钟和秒数的范围
    parts = time_str.split(':')
    hours, minutes, seconds = int(parts[0]), int(parts[1]), int(parts[2])
    if hours < 0 or hours > 23:
        return False
    if minutes < 0 or minutes > 59:
        return False
    if seconds < 0 or seconds > 59:
        return False
    
    return True

def fetch_thumbnail(video):
    thumbnail_url = video.thumbnail_url
    response = requests.get(thumbnail_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((256, 162), Image.LANCZOS)  # 調整縮圖大小以適應窗口
    return ImageTk.PhotoImage(img)

def searchResolution():
    video_link = url_entry.get()
    if video_link == '':
        showerror(title='Error', message='Provide the video link please!')
    else:
        try:
            video = YouTube(video_link)
            thumbnail_image = fetch_thumbnail(video)
            logo_label.config(image=thumbnail_image)
            logo_label.image = thumbnail_image  # 保存對象引用，防止垃圾回收

            # 获取视频时长并格式化为 hh:mm:ss
            video_length = video.length
            start_time_entry.delete(0, END)
            end_time_entry.delete(0, END)
            start_time_entry.insert(0, "00:00:00")
            end_time_entry.insert(0, f"{video_length // 3600:02}:{(video_length % 3600) // 60:02}:{video_length % 60:02}")

            resolutions = [i.resolution for i in video.streams.filter(adaptive=True, file_extension='mp4')]
            video_resolution['values'] = resolutions
            showinfo(title='Search Complete', message='Check the Combobox for the available video resolutions')
        except:
            showerror(title='Error', message='An error occurred while searching for video resolutions!')


def searchThread():
    t1 = threading.Thread(target=searchResolution)
    t1.start()

search_resolution.config(command=searchThread)

def generate_new_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}({counter}){ext}"
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base} ({counter}){ext}"
    return new_filename

def generate_new_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = f"{base}({counter}){ext}"
    while os.path.exists(new_filename):
        counter += 1
        new_filename = f"{base} ({counter}){ext}"
    return new_filename

def get_nearest_keyframe_before(file_path, timestamp):
    command = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'frame=pts_time,pict_type',
        '-of', 'csv=p=0', '-read_intervals', f"{timestamp}%+10", file_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    keyframes = [line.split(',')[0] for line in result.stdout.splitlines() if 'I' in line]
    if keyframes:
        return keyframes[0]
    return None
def get_nearest_keyframe_after(file_path, timestamp):
    command = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'frame=pts_time,pict_type',
        '-of', 'csv=p=0', '-read_intervals', f"{timestamp}%+10", file_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    keyframes = [line.split(',')[0] for line in result.stdout.splitlines() if 'I' in line]
    if keyframes:
        if len(keyframes) > 1:
            return keyframes[1]
        else:
            return keyframes[0]
    return None

def time_to_seconds(time_str):
    h, m, s = [float(part) for part in time_str.split(':')]
    return h * 3600 + m * 60 + s    
    
def seconds_to_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:06.3f}"

def get_video_length(file_path):
    command = [
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path
    ]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if result.returncode != 0:
        raise RuntimeError(f"Error getting video length: {result.stderr}")
    return float(result.stdout.strip())

def update_progress_bar(process, total_duration, progress_bar, progress_label, window):
    for line in process.stderr:
        if "time=" in line:
            time_split = line.split("time=")
            if len(time_split) > 1:
                time_str = time_split[1].split(" ")[0]
                time_parts = time_str.split(':')
                if len(time_parts) == 3:
                    try:
                        time_in_seconds = (int(time_parts[0]) * 3600) + (int(time_parts[1]) * 60) + float(time_parts[2])
                        percentage_completed = round((time_in_seconds / total_duration) * 100)
                        if percentage_completed > 100:
                            percentage_completed = 100
                        progress_bar['value'] = percentage_completed
                        progress_label.config(text=f'FFmpeg Processing: {percentage_completed}%')
                        window.update()
                    except ValueError:
                        continue

def download_video():   
    try:
        video_link = url_entry.get()
        resolution_or_bitrate = video_resolution.get()
        download_type = download_option.get()  # 獲取當前所選的選項
        save_path = save_path_var.get()
        process_type = process_option.get()
        start_time = start_time_entry.get()
        end_time = end_time_entry.get()

        if resolution_or_bitrate == '' and video_link == '':
            showerror(title='Error', message='Please enter both the video URL and resolution/bitrate!!')
        elif resolution_or_bitrate == '' and download_type == 'video':
            showerror(title='Error', message='Please select a video resolution or audio bitrate!!')
        elif resolution_or_bitrate == 'None' and download_type == 'video':
            showerror(title='Error', message='None is an invalid video resolution or audio bitrate!!\nPlease select a valid option')
        elif not save_path:
            showerror(title='Error', message='Please select a save location!')
        elif process_type != 'none' and not(is_valid_time_format(start_time) and is_valid_time_format(end_time)):
            showerror(title='Error', message='Please enter both start and end times for the selected processing option! (Format "hh:mm:ss")')
        else:
            try:
                def on_progress(stream, chunk, bytes_remaining):
                    total_size = stream.filesize
                    bytes_downloaded = total_size - bytes_remaining
                    percentage_completed = round(bytes_downloaded / total_size * 100)
                    progress_bar['value'] = percentage_completed
                    progress_label.config(text=str(percentage_completed) + '%, File size:' + f"{total_size / (1024*1024):.2f} MB")
                    window.update()

                video = YouTube(video_link, on_progress_callback=on_progress)
                
                if download_type == 'video':  # 當前選項為視頻下載
                    video_stream = video.streams.filter(res=resolution_or_bitrate, adaptive=True, file_extension='mp4').first()
                    audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').first()

                    video_path = video_stream.download(filename='video.mp4')
                    audio_path = audio_stream.download(filename='audio.mp4')

                    video_title = video.title.replace(" ", "_")  # 獲取影片標題並替換空格
                    output_path = os.path.join(save_path, f'{video_title}.mp4' if download_type == 'video' else f'{video_title}.mp3')
                    if os.path.exists(output_path):
                        output_path = generate_new_filename(output_path)
                    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')  # 指定 ffmpeg 的完整路徑

                    # 判断处理选项
                    if process_type == 'none':
                        command = [
                            ffmpeg_path, '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path
                        ]
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                        update_progress_bar(process, video.length, progress_bar, progress_label, window)

                        process.wait()
                        
                        if process.returncode == 0:
                            showinfo(title='Download Complete', message='Download completed successfully.')
                        else:
                            showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr.read()}')
                    elif process_type == 'quick':
                        start_keyframe = get_nearest_keyframe_before(video_path, start_time)
                        end_keyframe = get_nearest_keyframe_after(video_path, end_time)
                        if start_keyframe and end_keyframe:
                            temp_output = 'temp.mp4'
                            # 影音結合
                            command = [
                                ffmpeg_path, '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', temp_output
                            ]
                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                            update_progress_bar(process, video.length, progress_bar, progress_label, window)

                            process.wait()
                            if process.returncode != 0:
                                showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr}')
                                return
                            # 快速剪輯片段
                            command = [
                                ffmpeg_path, '-ss', start_keyframe, '-i', temp_output, '-to', end_keyframe, '-c', 'copy', output_path
                            ]
                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                            update_progress_bar(process, get_video_length(temp_output), progress_bar, progress_label, window)

                            process.wait()
                            if process.returncode != 0:
                                showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr}')
                                return
                        if process.returncode == 0:
                            showinfo(title='Download Complete', message='Download completed successfully.')
                        else:
                            showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr.read()}')
                    elif process_type == 'detailed':
                        start_keyframe = get_nearest_keyframe_before(video_path, start_time) # type 'second'
                        end_keyframe = get_nearest_keyframe_after(video_path, end_time) # type 'second'
                        if start_keyframe and end_keyframe:
                            temp_output = 'temp.mp4'
                            # 影音結合
                            command = [
                                ffmpeg_path, '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', temp_output
                            ]
                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                            update_progress_bar(process, video.length, progress_bar, progress_label, window)

                            process.wait()
                            if process.returncode != 0:
                                showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr}')
                                return
                            
                            # 快速剪輯片段
                            tmp_output = 'tmp.mp4'
                            command = [
                                ffmpeg_path, '-ss', start_keyframe, '-i', temp_output, '-to', end_keyframe, '-c', 'copy', tmp_output
                            ]
                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                            update_progress_bar(process, get_video_length(temp_output), progress_bar, progress_label, window)

                            process.wait()
                            if process.returncode != 0:
                                showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr}')
                                return
                            
                            # 詳細剪輯片段
                            start_seconds = time_to_seconds(start_time)
                            end_seconds = time_to_seconds(end_time)
                            start_offset = start_seconds - float(start_keyframe)
                            end_duration = end_seconds - start_seconds
                            start_offset_time = seconds_to_time(start_offset)
                            end_duration_time = seconds_to_time(end_duration)

                            command = [
                                ffmpeg_path, '-ss', start_offset_time, '-i', tmp_output, '-to', end_duration_time, '-c:v', 'libx264', '-c:a', 'aac', output_path
                            ]

                            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                            update_progress_bar(process, video.length, progress_bar, progress_label, window)

                            process.wait()
                            
                            if process.returncode == 0:
                                showinfo(title='Download Complete', message='Download completed successfully.')
                            else:
                                showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr.read()}')

                else:  # 當前選項為音頻下載
                    audio_stream = video.streams.filter(only_audio=True, file_extension='mp4').first()
                    audio_path = audio_stream.download(filename='audio.mp4')
                    
                    video_title = video.title.replace(" ", "_")  # 獲取影片標題並替換空格
                    output_path = os.path.join(save_path, f'{video_title}.mp3')
                    if os.path.exists(output_path):
                        output_path = generate_new_filename(output_path)
                    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')  # 指定 ffmpeg 的完整路徑
                    
                    if process_type == 'none':
                        command = [
                            ffmpeg_path, '-i', audio_path, '-q:a', '0', '-map', 'a', output_path
                        ]
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                        update_progress_bar(process, video.length, progress_bar, progress_label, window)
                        process.wait()
                        
                        if process.returncode == 0:
                            showinfo(title='Download Complete', message='Download completed successfully.')
                        else:
                            showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr.read()}')

                    else:
                        # 詳細剪輯片段
                        start_seconds = time_to_seconds(start_time)
                        end_seconds = time_to_seconds(end_time)
                        end_duration = end_seconds - start_seconds
                        end_duration_time = seconds_to_time(end_duration)

                        command = [
                            ffmpeg_path, '-ss', start_time, '-i', audio_path, '-t', end_duration_time, '-c:a', 'libmp3lame', '-b:a', '320k', output_path
                            ]
                        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)
                        update_progress_bar(process, video.length, progress_bar, progress_label, window)
                        process.wait()

                        if process.returncode == 0:
                            showinfo(title='Download Complete', message='Download completed successfully.')
                        else:
                            showerror(title='FFmpeg Error', message=f'Error processing media: {process.stderr.read()}')
                    
                progress_label.config(text='')
                progress_bar['value'] = 0

                # Clean up temporary files
                os.remove(audio_path)
                if download_type == 'video':
                    os.remove(video_path)
                    if process_type != 'none':
                        os.remove(temp_output)
                    if process_type == 'detailed':
                        os.remove(tmp_output)

            except Exception as e:
                showerror(title='Download Error', message=f'Failed to download video for this resolution: {e}')
                progress_label.config(text='')
                progress_bar['value'] = 0
    except Exception as e:
        showerror(title='Download Error', message=f'An error occurred while trying to download the video: {e}')
        progress_label.config(text='')
        progress_bar['value'] = 0



def downloadThread():
    t2 = threading.Thread(target=download_video)
    t2.start()

download_button.config(command=downloadThread)

window.mainloop()
