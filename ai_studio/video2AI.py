from IPython.display import display, Image, Audio
import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64

from openai import OpenAI
import pyaudio
import wave
import time
import threading
import queue

from ai_studio.Chat2AI import chat_with_ai
from config import *
from wave2AI import speech2text
from record_audio import record_audio

set_gpt4o()
client = OpenAI()

'''"""
语言输入
"""
OUTPUT_DIR = "E:\\YanYi\\study_technology\\AI-agent\\AI_studio\\ai_studio\\sounds"
filename = os.path.join(OUTPUT_DIR, "temp_audio.wav")
# 关键词
WAKE_WORD = "小君"


# 转录音频函数
def transcribe_audio():
    #录音
    record_audio(filename)

    #音频转文本
    transcription_text = speech2text(filename)
    # 实时打印转录结果
    print("转录结果:", transcription_text)
    # 检查是否包含唤醒词
    if WAKE_WORD in transcription_text:
        listening = True
        last_activity_time = time.time()
        print(f"检测到唤醒词 '{WAKE_WORD}'")'''

#  视频输入
# 存储最近5秒内的帧，每秒5帧
base64Frames = queue.Queue(maxsize=25)


def capture_frames():
    video = cv2.VideoCapture(0)
    if not video.isOpened():
        print("无法打开摄像头")
        return

    while True:
        # 捕捉视频帧
        ret, frame = video.read()

        if not ret:
            print("无法接收帧（stream end?）")
            break

        # 将图片编码并添加到队列中
        _, buffer = cv2.imencode(".jpg", frame)
        frame_data = base64.b64encode(buffer).decode("utf-8")

        if base64Frames.full():
            base64Frames.get()

        base64Frames.put(frame_data)

        # 显示帧
        cv2.imshow('camera', frame)

        # 按下 'q' 键退出
        if cv2.waitKey(1) == ord('q'):
            break

        time.sleep(0.2)  # 每秒采样5帧

    # 释放摄像头和关闭窗口
    video.release()
    cv2.destroyAllWindows()

# 处理视频帧
def process_video_frames():
    while True:
        if not base64Frames.empty():
            frame_list = list(base64Frames.queue)
            PROMPT_MESSAGES = [
                {
                    "role": "user",
                    "content": [
                        "These are frames from a video that I want to upload. Generate a compelling description that I can upload along with the video.",
                        *map(lambda x: {"image": x, "resize": 768}, frame_list[0::5]),
                    ],
                },
            ]
            params = {
                "model": "gpt-4o",
                "messages": PROMPT_MESSAGES,
                "max_tokens": 200,
            }

            try:
                result = client.chat.completions.create(**params)
                print(result.choices[0].message.content)

                # 假设 result.choices[0].message.content 是你要转换成语音的文本
                text_to_speech = result.choices[0].message.content

                # 调用API生成音频
                response = client.audio.speech.create(
                    model="tts-1-1106",
                    input=text_to_speech,
                    voice="alloy"
                )

                # 处理音频响应
                audio_data = response['data']

                # 在Jupyter Notebook中直接播放音频
                display(Audio(audio_data))

            except Exception as e:
                print(f"An error occurred: {e}")

            # 等待一段时间后再处理下一组帧
            time.sleep(5)

# 创建并启动捕捉视频帧的线程
capture_thread = threading.Thread(target=capture_frames)
capture_thread.start()

# 创建并启动处理视频帧的线程
process_thread = threading.Thread(target=process_video_frames)
process_thread.start()

# 等待捕捉线程和处理线程完成
capture_thread.join()
process_thread.join()

'''
# 假设 result.choices[0].message.content 是你要转换成语音的文本
text_to_speech = result.choices[0].message.content

try:
    # 调用API生成音频
    response = client.audio.speech.create(
        model="tts-1-1106",
        input=text_to_speech,
        voice="alloy"
    )

    # 处理音频响应
    audio_data = response['data']

    # 在Jupyter Notebook中直接播放音频
    display(Audio(audio_data))

except Exception as e:
    print(f"An error occurred: {e}")'''
