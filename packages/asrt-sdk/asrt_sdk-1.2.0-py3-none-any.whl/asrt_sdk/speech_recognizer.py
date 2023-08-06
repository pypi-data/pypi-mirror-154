#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2016-2099 Ailemon.net
#
# This file is part of ASRT Speech Recognition Tool Python SDK.
#
# ASRT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# ASRT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ASRT.  If not, see <https://www.gnu.org/licenses/>.
# ============================================================================

"""
@author: nl8590687
ASRT语音识别Python SDK 语音识别接口调用类库
"""

import grpc
import json
import time
from .utils import AsrtApiSpeechRequest, AsrtApiLanguageRequest, AsrtApiResponse
from .network.asrt_pb2_grpc import AsrtGrpcServiceStub
from .network.asrt_pb2 import SpeechRequest, LanguageRequest, WavData
from .utils import read_wav_datas
from .network import get_http_session

def get_speech_recognizer(host:str, port:str, protocol:str):
    '''
    获取一个ASRT语音识别SDK接口调用实例对象 \\
    参数：\\
        host: 主机域名或IP.
        port: 主机端口号.
        protocol: 网络协议类型.
    '''
    if protocol.lower() in ('http', 'https'):
        return HttpSpeechRecognizer(host, port, protocol)
    elif protocol.lower() in ('grpc', 'grpcs'):
        return GrpcSpeechRecognizer(host, port, protocol.lower() == 'grpcs')
    return None


class BaseSpeechRecognizer():
    '''
    ASRT语音识别SDK接口调用类基类
    '''
    def __init__(self, host:str, port:str, protocol:str):
        self.host = host
        self.port = port
        self.protocol = protocol

    def recognite(self, wav_data, frame_rate, channels, byte_width):
        '''
        完整识别wav语音序列为文本
        '''
        print("call `recognite()` with", self.protocol, self.host, self.port)
        print(len(wav_data), frame_rate, channels, byte_width)
        raise Exception("Method Unimpletment")

    def recognite_speech(self, wav_data, frame_rate, channels, byte_width):
        '''
        调用声学模型识别wav语音序列为拼音序列
        '''
        print("call `recognite_speech()` with", self.protocol, self.host, self.port)
        print(len(wav_data), frame_rate, channels, byte_width)
        raise Exception("Method Unimpletment")

    def recognite_language(self, sequence_pinyin):
        '''
        调用语言模型识别拼音序列为文本
        '''
        print("call `recognite_language()` with", self.protocol, self.host, self.port)
        print(sequence_pinyin)
        raise Exception("Method Unimpletment")

    def recognite_file(self, filename):
        '''
        识别一条wav语音文件为文本
        '''
        print("call `recognite_file()` with", self.protocol, self.host, self.port)
        print(filename)
        raise Exception("Method Unimpletment")


class HttpSpeechRecognizer(BaseSpeechRecognizer):
    '''
    ASRT语音识别SDK基于HTTP协议接口调用类 \\
    参数: \\
        host: 主机域名或IP.
        port: 主机端口号.
        protocol: 网络协议类型.
        sub_path: 接口所在URL的子路径, 默认为""
    '''
    def __init__(self, host:str, port:str, protocol:str, sub_path:str=''):
        super().__init__(host, port, protocol)
        if protocol not in ('http', 'https'):
            raise Exception('Unsupport netword protocol `' + protocol +'`')
        self._url_ = protocol + '://' + host + ':' + port
        self.sub_path = sub_path
        self._wav_data_max_length = 16000 * 2 * 16

    def recognite(self, wav_data, frame_rate:int, channels:int, byte_width:int) -> AsrtApiResponse:
        '''
        完整识别wav语音序列为文本
        '''
        if len(wav_data) > self._wav_data_max_length:
            raise Exception('Too long wave sample byte length: `' + str(len(wav_data))
                + "`, the max length is `" + str(self._wav_data_max_length) + "`")

        request_body = AsrtApiSpeechRequest(wav_data, frame_rate, channels, byte_width)
        headers = {'Content-Type': 'application/json'}
        http_request = get_http_session()
        try:
            response_object = http_request.post(self._url_ + self.sub_path + '/all',
                                    headers=headers,
                                    data=request_body.to_json())
            if response_object.status_code != 200:
                raise Exception("ASRT API server http statue code exception: " + str(response_object.status_code))
        except Exception as exception_info:
            raise Exception("Error to send speech recognition request to ASRT API server:" +
                exception_info.__str__())

        try:
            response_body_dict = json.loads(response_object.text)
            response_body = AsrtApiResponse()
            response_body.from_json(**response_body_dict)
            return response_body
        except Exception as exception_info:
            raise Exception("Unormal data format is responsed by ASRT API server with HTTP protocol: " +
                exception_info.__str__())


    def recognite_speech(self, wav_data, frame_rate, channels, byte_width):
        '''
        调用声学模型识别wav语音序列为拼音序列
        '''
        if len(wav_data) > self._wav_data_max_length:
            raise Exception('Too long wave sample byte length: `' + str(len(wav_data))
                + "`, the max length is `" + str(self._wav_data_max_length) + "`")

        request_body = AsrtApiSpeechRequest(wav_data, frame_rate, channels, byte_width)
        headers = {'Content-Type': 'application/json'}
        http_request = get_http_session()
        try:
            response_object = http_request.post(self._url_ + self.sub_path + '/speech',
                                    headers=headers,
                                    data=request_body.to_json())
            if response_object.status_code != 200:
                raise Exception("ASRT API server http statue code exception: " + str(response_object.status_code))
        except Exception as exception_info:
            raise Exception("Error to send speech recognition request to ASRT API server:" +
                exception_info.__str__())

        try:
            response_body_dict = json.loads(response_object.text)
            response_body = AsrtApiResponse()
            response_body.from_json(**response_body_dict)
            return response_body
        except Exception as exception_info:
            raise Exception("Unormal data format is responsed by ASRT API server with HTTP protocol: " +
                exception_info.__str__())

    def recognite_language(self, sequence_pinyin):
        '''
        调用语言模型识别拼音序列为文本
        '''
        request_body = AsrtApiLanguageRequest(sequence_pinyin)
        headers = {'Content-Type': 'application/json'}
        http_request = get_http_session()
        try:
            response_object = http_request.post(self._url_ + self.sub_path + '/language',
                                    headers=headers,
                                    data=request_body.to_json())
            if response_object.status_code != 200:
                raise Exception("ASRT API server http statue code exception: " + str(response_object.status_code))
        except Exception as exception_info:
            raise Exception("Error to send speech recognition request to ASRT API server:" +
                exception_info.__str__())

        try:
            response_body_dict = json.loads(response_object.text)
            response_body = AsrtApiResponse()
            response_body.from_json(**response_body_dict)
            return response_body
        except Exception as exception_info:
            raise Exception("Unormal data format is responsed by ASRT API server with HTTP protocol: " +
                exception_info.__str__())

    def recognite_long(self, wav_data, frame_rate, channels, byte_width):
        '''
        完整识别wav长语音序列为文本, 会自动分段
        '''
        if frame_rate != 16000:
            raise Exception('Unsupport wave sample rate `' + str(frame_rate) +'`')

        if channels != 1:
            raise Exception('Unsupport wave channels number `' + str(channels) +'`')

        if byte_width != 2:
            raise Exception('Unsupport wave byte width `' + str(byte_width) +'`')

        asrt_result = list()
        duration = 2*16000*10
        for index in range(0, len(wav_data)//duration+1):
            rsp = self.recognite(wav_data=wav_data[index*duration:min((index+1)*duration, len(wav_data))],
                            frame_rate=frame_rate,
                            channels=channels,
                            byte_width=byte_width
                            )
            asrt_result.append(rsp)
        return asrt_result

    def recognite_file(self, filename):
        '''
        识别一条wav语音文件为文本
        '''
        wave_data = read_wav_datas(filename)
        str_data = wave_data.str_data
        frame_rate = wave_data.sample_rate
        channels = wave_data.channels
        byte_width = wave_data.byte_width
        return self.recognite_long(str_data, frame_rate, channels, byte_width)


class GrpcSpeechRecognizer(BaseSpeechRecognizer):
    '''
    ASRT语音识别SDK基于GRPC协议接口调用类 \\
    参数: \\
        host: 主机域名或IP.
        port: 主机端口号.
        enable_transport_security: 是否启用安全传输协议.
    '''
    def __init__(self, host:str, port:str, enable_transport_security:bool=False):
        protocol = "grpc"
        if enable_transport_security:
            protocol = "grpcs"
        super().__init__(host, port, protocol)
        self.conn = grpc.insecure_channel(host+':'+port)
        self.client = AsrtGrpcServiceStub(channel=self.conn)
        self._wav_data_max_length = 16000 * 2 * 16

    def recognite(self, wav_data, frame_rate, channels, byte_width):
        '''
        完整识别wav语音序列为文本
        '''
        wav_data = WavData(samples=wav_data, sample_rate=frame_rate,
                        channels=channels, byte_width=byte_width)
        request = SpeechRequest(wav_data=wav_data)
        response = self.client.All(request)
        return response

    def recognite_speech(self, wav_data, frame_rate, channels, byte_width):
        '''
        调用声学模型识别wav语音序列为拼音序列
        '''
        wav_data = WavData(samples=wav_data, sample_rate=frame_rate,
                        channels=channels, byte_width=byte_width)
        request = SpeechRequest(wav_data=wav_data)
        response = self.client.Speech(request)
        return response

    def recognite_language(self, sequence_pinyin):
        '''
        调用语言模型识别拼音序列为文本
        '''
        request = LanguageRequest(pinyins=sequence_pinyin)
        response = self.client.Language(request)
        return response

    def recognite_long(self, wav_data, frame_rate, channels, byte_width):
        '''
        完整识别wav长语音序列为文本, 会自动分段
        '''
        if frame_rate != 16000:
            raise Exception('Unsupport wave sample rate `' + str(frame_rate) +'`')

        if channels != 1:
            raise Exception('Unsupport wave channels number `' + str(channels) +'`')

        if byte_width != 2:
            raise Exception('Unsupport wave byte width `' + str(byte_width) +'`')

        asrt_result = list()
        duration = 2*16000*10
        for index in range(0, len(wav_data)//duration+1):
            rsp = self.recognite(wav_data=wav_data[index*duration:min((index+1)*duration, len(wav_data))],
                            frame_rate=frame_rate,
                            channels=channels,
                            byte_width=byte_width
                            )
            asrt_result.append(rsp)
        return asrt_result

    def recognite_stream(self, wav_data_generator, duration, callback_function):
        '''
        启动流式语音识别
        '''
        wav_data_iter = wav_data_generator()
        # 制造客户端发送的请求体
        def make_request_data():
            for wav_obj in wav_data_iter:
                time.sleep(duration)
                wav_data, frame_rate, channels, byte_width = wav_obj
                wav_data = WavData(samples=wav_data, sample_rate=frame_rate,
                        channels=channels, byte_width=byte_width)
                yield SpeechRequest(wav_data=wav_data)
        try:
            status_response = self.client.Stream(make_request_data())
            for ret in status_response:
                callback_function(ret)
        except Exception as any_exception:
            print(f'err in send_status:{any_exception}')
            return

    def recognite_file(self, filename):
        '''
        识别一条wav语音文件为文本
        '''
        wave_data = read_wav_datas(filename)
        str_data = wave_data.str_data
        frame_rate = wave_data.sample_rate
        channels = wave_data.channels
        byte_width = wave_data.byte_width
        return self.recognite_long(str_data, frame_rate, channels, byte_width)
