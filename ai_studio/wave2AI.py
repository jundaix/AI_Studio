from openai import OpenAI
import pyaudio
import wave
import os
import time
from record_audio import record_audio

from config import *

set_gpt4o()
client = OpenAI()


def speech2text(output_filename):
    # 打开音频文件并调用OpenAI的API进行转录
    try:
        with open(output_filename, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # 直接访问Transcription对象的属性
        transcription_text = response.text

        return transcription_text
        # 实时打印转录结果

    except Exception as e:
        print(f"处理API响应时出错: {e}")


'''
使用实例
OUTPUT_DIR = "E:\\YanYi\\study_technology\\AI-agent\\AI_studio\\ai_studio\\sounds"
filename = os.path.join(OUTPUT_DIR, "temp_audio.wav")

record_audio(filename)

text = speech2text(filename)
print("转录结果:", text)'''
