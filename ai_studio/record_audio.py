import pyaudio
import wave

# 设置音频捕捉参数
FORMAT = pyaudio.paInt16  # 16位格式
CHANNELS = 1  # 单声道
RATE = 16000  # 采样率 16000Hz
CHUNK = 1024  # 每次读取的音频数据大小
RECORD_SECONDS = 5  # 每次录音的时长为5秒
OUTPUT_DIR = "E:\\YanYi\\study_technology\\AI-agent\\AI_studio\\ai_studio\\sounds"


def record_audio(output_filename):
    # 初始化PyAudio
    audio_interface = pyaudio.PyAudio()

    # 打开音频流
    stream = audio_interface.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

    print("开始录音...")

    frames = []

    # 录制音频数据
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束")

    # 关闭音频流
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    # 将音频数据保存为WAV文件
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


'''output_filename = f"{OUTPUT_DIR}\\recorded_audio.wav"
record_audio(output_filename)
print(f"音频已保存到 {output_filename}")'''
