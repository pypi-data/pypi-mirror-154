# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#  * Neither the name of NVIDIA CORPORATION nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#!/usr/bin/env python

import argparse
import os
import sys
import time
import wave

import grpc
import numpy as np
import pyaudio

import riva_api
import riva_api.proto.riva_audio_pb2 as ra
import riva_api.proto.riva_tts_pb2 as rtts
import riva_api.proto.riva_tts_pb2_grpc as rtts_srv
from riva_api.audio_io import SoundCallBack, list_output_devices


def parse_args():
    parser = argparse.ArgumentParser(description="Streaming transcription via Riva AI Services")
    parser.add_argument("--server", default="localhost:50051", type=str, help="URI to GRPC server endpoint")
    parser.add_argument("--voice", type=str, help="voice name to use", default="English-US-Female-1")
    parser.add_argument("-o", "--output", default=None, type=str, help="Output file to write last utterance")
    parser.add_argument("--list-devices", action="store_true", help="list output devices indices")
    parser.add_argument("--output-device", type=int, help="Output device to use")
    parser.add_argument("--ssl_cert", type=str, default="", help="Path to SSL client certificatates file")
    parser.add_argument(
        "--use_ssl", default=False, action='store_true', help="Boolean to control if SSL/TLS encryption should be used"
    )
    return parser.parse_args()


def old_main():
    args = parse_args()
    if args.ssl_cert != "" or args.use_ssl:
        root_certificates = None
        if args.ssl_cert != "" and os.path.exists(args.ssl_cert):
            with open(args.ssl_cert, 'rb') as f:
                root_certificates = f.read()
        creds = grpc.ssl_channel_credentials(root_certificates)
        channel = grpc.secure_channel(args.server, creds)
    else:
        channel = grpc.insecure_channel(args.server)
    tts_client = rtts_srv.RivaSpeechSynthesisStub(channel)
    audio_handle = pyaudio.PyAudio()

    if args.list_devices:
        for i in range(audio_handle.get_device_count()):
            info = audio_handle.get_device_info_by_index(i)
            if info['maxOutputChannels'] < 1:
                continue
            print(f"{info['index']}: {info['name']}")
        sys.exit(0)

    print("Connecting...")
    print("Example query:")
    print(
        "  Hello, My name is Linda"
        + ", and I am demonstrating streaming speech synthesis with Riva {@EY2}.I. services, running on NVIDIA {@JH}{@IY1}_{@P}{@IY}_{@Y}{@UW0}s."
    )
    req = rtts.SynthesizeSpeechRequest()
    req.text = "Hello"
    req.language_code = "en-US"
    req.encoding = ra.AudioEncoding.LINEAR_PCM
    req.sample_rate_hz = 44100
    req.voice_name = args.voice

    stream = audio_handle.open(
        format=pyaudio.paInt16,
        output_device_index=args.output_device,
        channels=1,
        rate=req.sample_rate_hz,
        output=True,
    )
    while True:
        print("Speak: ", end='')
        req.text = str(input())
        if args.output:
            wav = wave.open(args.output, 'wb')
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(req.sample_rate_hz)

        print("Generating audio for request...")
        print(f"  > '{req.text}': ", end='')
        start = time.time()
        responses = tts_client.SynthesizeOnline(req)
        stop = time.time()
        first = True
        for resp in responses:
            stop = time.time()
            if first:
                print(f"Time to first audio: {(stop-start):.3f}s")
                first = False
            stream.write(resp.audio)
            if args.output:
                wav.writeframesraw(resp.audio)
        if args.output:
            wav.close()
    stream.stop_stream()
    stream.close()


def main() -> None:
    args = parse_args()
    if args.list_devices:
        list_output_devices()
        return
    auth = riva_api.Auth(args.ssl_cert, args.use_ssl, args.server)
    service = riva_api.SpeechSynthesisService(auth)
    nchannels = 1
    sampwidth = 2
    with SoundCallBack(
        args.output_device, nchannels=nchannels, sampwidth=sampwidth, framerate=args.sample_rate_hz
    ) as sound_stream:
        try:
            if args.output is not None:
                out_f = wave.open(str(args.output), 'wb')
                out_f.setnchannels(nchannels)
                out_f.setsampwidth(sampwidth)
                out_f.setframerate(args.sample_rate_hz)
            else:
                out_f = None
            while True:
                text = input("Speak: ")
                print("Generating audio for request...")
                print(f"  > '{text}': ", end='')
                start = time.time()
                responses = service.synthesize_online(
                    text, args.voice, args.language_code, sample_rate_hz=args.sample_rate_hz
                )
                first = True
                for resp in responses:
                    stop = time.time()
                    if first:
                        print(f"Time to first audio: {(stop - start):.3f}s")
                        first = False
                    sound_stream(resp.audio)
                    if out_f is not None:
                        out_f.writeframesraw(resp.audio)
        finally:
            if args.output is not None:
                out_f.close()


if __name__ == '__main__':
    #old_main()
    main()
