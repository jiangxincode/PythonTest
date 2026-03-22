"""
MiMo-V2-TTS 文本转语音小工具

两种模式：
  1. 交互模式（默认）：输入文本，实时合成并播放
     python mimo-v2-tts-test.py

  2. 文件模式：读取文本文件，合成后输出为 wav 文件
     python mimo-v2-tts-test.py -f story.txt -o output.wav

使用前请设置环境变量：
  $env:LLM_API_KEY = "your-api-key"

依赖安装：
  pip install openai

参考文档：https://platform.xiaomimimo.com/#/docs/usage-guide/speech-synthesis
"""

import os
import sys
import argparse
import base64
import tempfile
import subprocess
import platform
import wave
import struct
from openai import OpenAI

# API 配置
API_KEY = os.environ.get("LLM_API_KEY")
BASE_URL = "https://api.xiaomimimo.com/v1"
MODEL = "mimo-v2-tts"

# 可选音色: mimo_default, default_zh, default_en
DEFAULT_VOICE = "mimo_default"

# 单次请求最大文本长度（避免超限），按段落拆分
MAX_CHUNK_LEN = 2000


def check_api_key():
    if not API_KEY:
        print("错误：请先设置环境变量 LLM_API_KEY")
        print('  $env:LLM_API_KEY = "your-api-key"')
        sys.exit(1)


def get_client() -> OpenAI:
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)


def synthesize(text: str, voice: str = DEFAULT_VOICE) -> bytes:
    """调用 MiMo-V2-TTS 合成语音，返回 wav 音频字节"""
    client = get_client()

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "assistant", "content": text}
        ],
        extra_body={
            "audio": {
                "format": "wav",
                "voice": voice,
            }
        },
    )

    message = completion.choices[0].message
    audio_data = getattr(message, "audio", None)
    if audio_data is None:
        raise RuntimeError("API 未返回音频数据")

    return base64.b64decode(audio_data.data)


def split_text(text: str) -> list[str]:
    """将长文本按段落拆分，确保每段不超过 MAX_CHUNK_LEN"""
    # 先按空行分段
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    chunks = []
    for para in paragraphs:
        if len(para) <= MAX_CHUNK_LEN:
            chunks.append(para)
        else:
            # 按句号、感叹号、问号拆分长段落
            sentences = []
            current = ""
            for char in para:
                current += char
                if char in "。！？!?.":
                    sentences.append(current)
                    current = ""
            if current:
                sentences.append(current)

            # 合并短句，不超过限制
            buf = ""
            for s in sentences:
                if len(buf) + len(s) > MAX_CHUNK_LEN:
                    if buf:
                        chunks.append(buf)
                    buf = s
                else:
                    buf += s
            if buf:
                chunks.append(buf)

    return chunks


def concat_wav(wav_list: list[bytes]) -> bytes:
    """拼接多段 wav 音频字节为一个完整的 wav"""
    if len(wav_list) == 1:
        return wav_list[0]

    # 读取第一段获取参数
    import io
    with wave.open(io.BytesIO(wav_list[0]), "rb") as w:
        params = w.getparams()
        frames = [w.readframes(w.getnframes())]

    # 读取后续段的 PCM 数据
    for data in wav_list[1:]:
        with wave.open(io.BytesIO(data), "rb") as w:
            frames.append(w.readframes(w.getnframes()))

    # 写入合并后的 wav
    out = io.BytesIO()
    with wave.open(out, "wb") as w:
        w.setparams(params)
        for f in frames:
            w.writeframes(f)

    return out.getvalue()





def play_audio(filepath: str):
    """跨平台播放音频文件"""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run(
                [
                    "powershell", "-c",
                    f'(New-Object Media.SoundPlayer "{filepath}").PlaySync()',
                ],
                check=True,
            )
        elif system == "Darwin":
            subprocess.run(["afplay", filepath], check=True)
        else:
            for player in ["mpv", "ffplay", "aplay", "paplay"]:
                if (
                    subprocess.run(
                        ["which", player], capture_output=True
                    ).returncode == 0
                ):
                    cmd = [player]
                    if player == "ffplay":
                        cmd += ["-nodisp", "-autoexit"]
                    elif player == "mpv":
                        cmd += ["--no-video"]
                    cmd.append(filepath)
                    subprocess.run(cmd, check=True)
                    return
            print(f"未找到音频播放器，文件已保存至：{filepath}")
    except Exception as e:
        print(f"播放失败：{e}")
        print(f"音频文件已保存至：{filepath}")


def synthesize_and_play(text: str, voice: str = DEFAULT_VOICE):
    """合成语音并播放（交互模式用）"""
    print(f"正在合成语音：{text[:50]}{'...' if len(text) > 50 else ''}")
    audio_bytes = synthesize(text, voice)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes)
        tmp_path = f.name

    print("语音已生成，正在播放...")
    play_audio(tmp_path)

    try:
        os.unlink(tmp_path)
    except OSError:
        pass


def file_mode(input_file: str, output_file: str, voice: str = DEFAULT_VOICE):
    """文件模式：读取文本文件，逐段合成，拼接后输出为 mp3"""
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("错误：输入文件为空")
        return

    chunks = split_text(text)
    print(f"文本已拆分为 {len(chunks)} 段")

    wav_parts = []
    for i, chunk in enumerate(chunks, 1):
        preview = chunk[:40].replace("\n", " ")
        print(f"[{i}/{len(chunks)}] 合成中：{preview}...")
        try:
            audio = synthesize(chunk, voice)
            wav_parts.append(audio)
        except Exception as e:
            print(f"  第 {i} 段合成失败：{e}，跳过")

    if not wav_parts:
        print("错误：没有成功合成任何音频")
        return

    print("正在拼接音频...")
    merged = concat_wav(wav_parts)

    with open(output_file, "wb") as f:
        f.write(merged)
    print(f"已保存：{output_file}")


def interactive_mode():
    """交互模式：输入文本实时合成播放"""
    print("=" * 40)
    print("  MiMo-V2-TTS 文本转语音工具")
    print("=" * 40)
    print("输入文本后按回车合成语音，输入 q 退出")
    print(f"当前音色：{DEFAULT_VOICE}")
    print("提示：可用 <style>开心</style> 等标签控制风格\n")

    while True:
        try:
            text = input("请输入文本> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not text:
            continue
        if text.lower() == "q":
            print("再见！")
            break

        try:
            synthesize_and_play(text)
        except Exception as e:
            print(f"合成失败：{e}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="MiMo-V2-TTS 文本转语音工具"
    )
    parser.add_argument(
        "-f", "--file", help="输入文本文件路径"
    )
    parser.add_argument(
        "-o", "--output", default="output.wav",
        help="输出音频文件路径（默认 output.wav）"
    )
    parser.add_argument(
        "-v", "--voice", default=DEFAULT_VOICE,
        help=f"音色（默认 {DEFAULT_VOICE}，可选 default_zh/default_en）"
    )
    args = parser.parse_args()

    check_api_key()

    if args.file:
        file_mode(args.file, args.output, args.voice)
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
