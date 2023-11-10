import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from google.cloud import texttospeech
from typing import BinaryIO, Optional
from openai import OpenAI
from pygame import mixer
import base64
import time


def encode_image(img_path: str) -> str:
    """Encodes the image in a given path to a base64 string.

    Parameters
    ----------
    img_path : str
        Path of the image to be encoded.

    Returns
    -------
    str
        Encoded base64 img of the input image.
    """
    with open(img_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def audio_to_text(audio: BinaryIO) -> str:
    """Transcripts a given audio file using OpenAI whisper API.

    Parameters
    ----------
    audio : BinaryIO
        Binary audio file to be converted to string.

    Returns
    -------
    str
        Transcription of the input file.
    """
    client = OpenAI()
    return client.audio.transcriptions.create(
        model="whisper-1", file=audio, response_format="text"
    )


def text_to_audio(text: str) -> BinaryIO:
    """Synthesizes speech from a given text using GCP Text to Speech API.

    Parameters
    ----------
    text : str
        Text to be synthesized.

    Returns
    -------
    BinaryIO
        Audio file of the synthesized speech.
    """
    # Taken from the GCP examples I won't hide
    # https://cloud.google.com/text-to-speech/docs/samples/tts-synthesize-text

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    return response.audio_content


def ask_about_img(question: str, img_b64: str) -> str:
    """Queries GPT-4V with a question and an image and returns the answer.

    Parameters
    ----------
    question : str
        Question to ask GPT-4V about the image.
    img : str
        Base64-encoded image that will be sent to GPT-4V.

    Returns
    -------
    str
        Answer to the question from GPT-4V.
    """

    # TODO: Error handling + If there is an error, use a cached error audio file without querying T2S.
    # TODO: Enhance/experiment further with the prompt.

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{question}. Be concise, use as few sentences as possible.",
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{img_b64}",
                    },
                ],
            }
        ],
        max_tokens=200,
    )

    return response.choices[0].message.content


def play_audio(audio_path: str) -> None:
    """Plays a given audio file.

    Parameters
    ----------
    audio_path : str
        Path to the audio file to be played.
    """
    mixer.init()
    mixer.music.load(audio_path)
    mixer.music.play()
    # wait for music to finish playing
    while mixer.music.get_busy():
        time.sleep(1)


def run(question_path: str, img_path: str) -> BinaryIO:
    """Generates an audio response given an audio question and an image.

    Parameters
    ----------
    question_path : str
        Path to the input audio file with a question.
    img_path : str
        Path to the input img with visual context.

    Returns
    -------
    binaryIO
        Binary file with the audio response to the question.
    """
    # TODO: Maybe make the input files binary as well for consistency

    question_audio = open(question_path, "rb")
    question_text = audio_to_text(question_audio)

    # TODO: Add resize based on the smaller side of the captured frame to a sensible size
    img_b64 = encode_image(img_path)

    answer_text = ask_about_img(question_text, img_b64)
    return text_to_audio(answer_text)


if __name__ == "__main__":
    # TODO: Specify files through cli args
    # TODO: Move fns to utils file and make a tiresias class, share the same client
    # TODO: Add support for openAI key specified in the code?
    FILE = 1
    AUDIO_FILE = f"input_{FILE}.mp3"
    IMG_FILE = f"input_{FILE}.png"
    AUDIO_OUTPUT = f"output_{FILE}.mp3"

    answer_audio = run(AUDIO_FILE, IMG_FILE)

    # store audio
    with open(AUDIO_OUTPUT, "wb") as out:
        out.write(answer_audio)

    play_audio(AUDIO_OUTPUT)
