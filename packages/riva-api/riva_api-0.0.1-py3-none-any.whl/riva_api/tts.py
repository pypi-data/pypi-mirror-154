# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT

from typing import Generator

import riva_api.proto.riva_tts_pb2 as rtts
import riva_api.proto.riva_tts_pb2_grpc as rtts_srv
from riva_api import Auth
from riva_api.proto.riva_audio_pb2 import AudioEncoding


class SpeechSynthesisService:
    """
    A class for synthesizing speech from text. Provides :meth:`synthesize` which returns entire audio for a text
    and :meth:`synthesize_online` which returns audio in small chunks as it is becoming available.
    """
    def __init__(self, auth: Auth) -> None:
        """
        Initializes an instance of the class.

        Args:
            auth (:obj:`Auth`): an instance of :class:`riva_api.auth.Auth` which is used for
                authentication metadata generation.
        """
        self.auth = auth
        self.stub = rtts_srv.RivaSpeechSynthesisStub(self.auth.channel)

    def synthesize(
        self,
        text: str,
        voice_name: str,
        language_code: str = 'en-US',
        encoding: AudioEncoding = AudioEncoding.LINEAR_PCM,
        sample_rate_hz: int = 44100,
    ) -> rtts.SynthesizeSpeechResponse:
        """
        Synthesizes an entire audio for text :param:`text`.

        Args:
            text (:obj:`str`): an input text.
            voice_name (:obj:`str`): a name of the voice, e.g. ``"English-US-Female-1"``. You may find available
                voices in server logs or in server model directory.
            language_code (:obj:`str`): a language to use.
            encoding (:obj:`AudioEncoding`): an output audio encoding, e.g. ``AudioEncoding.LINEAR_PCM``.
            sample_rate_hz (:obj:`int`): number of frames per second in output audio.

        Returns:
            :obj:`riva_api.proto.riva_tts_pb2.SynthesizeSpeechResponse`: a response with output. You may find
            :class:`riva_api.proto.riva_tts_pb2.SynthesizeSpeechResponse` fields description
            `here <https://docs.nvidia.com/deeplearning/riva/user-guide/docs/reference/protos/protos.html#riva-proto-riva-tts-proto>`_.
        """
        req = rtts.SynthesizeSpeechRequest(
            text=text,
            voice_name=voice_name,
            language_code=language_code,
            sample_rate_hz=sample_rate_hz,
            encoding=encoding,
        )
        return self.stub.Synthesize(req, metadata=self.auth.get_auth_metadata())

    def synthesize_online(
        self,
        text: str,
        voice_name: str,
        language_code: str = 'en-US',
        encoding: AudioEncoding = AudioEncoding.LINEAR_PCM,
        sample_rate_hz: int = 44100,
    ) -> Generator[rtts.SynthesizeSpeechResponse, None, None]:
        """
        Synthesizes and yields output audio chunks for text :param:`text` as the chunks
        becoming available.

        Args:
            text (:obj:`str`): an input text.
            voice_name (:obj:`str`): a name of the voice, e.g. ``"English-US-Female-1"``. You may find available
                voices in server logs or in server model directory.
            language_code (:obj:`str`): a language to use.
            encoding (:obj:`AudioEncoding`): an output audio encoding, e.g. ``AudioEncoding.LINEAR_PCM``.
            sample_rate_hz (:obj:`int`): number of frames per second in output audio.

        Yields:
            :obj:`riva_api.proto.riva_tts_pb2.SynthesizeSpeechResponse`: a response with output. You may find
            :class:`riva_api.proto.riva_tts_pb2.SynthesizeSpeechResponse` fields description
            `here <https://docs.nvidia.com/deeplearning/riva/user-guide/docs/reference/protos/protos.html#riva-proto-riva-tts-proto>`_.
        """
        req = rtts.SynthesizeSpeechRequest(
            text=text,
            voice_name=voice_name,
            language_code=language_code,
            sample_rate_hz=sample_rate_hz,
            encoding=encoding,
        )
        return self.stub.SynthesizeOnline(req, metadata=self.auth.get_auth_metadata())
