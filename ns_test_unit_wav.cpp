/*
 *  Copyright (c) 2012 The WebRTC project authors. All Rights Reserved.
 *
 *  Use of this source code is governed by a BSD-style license
 *  that can be found in the LICENSE file in the root of the source
 *  tree. An additional intellectual property rights grant can be found
 *  in the file PATENTS.  All contributing project authors may
 *  be found in the AUTHORS file in the root of the source tree.
 */


/*  webrtc_NoiseSuppressor_cpp_build test unit with wmv

author: gamefunc
    website: https://www.gamefunc.top:9029
    github: https://github.com/gamefunc
    qq: 32686647
    weixin: gamefunc
    mail: fevefun@hotmail.com
free to use and modify, but need keep the above information.

test env:
    win_10: cl: 19.35.32215;
    debian_11: gcc: 10.2.1; 
*/

#include <string>
#include <filesystem>
#include <fstream>
#include <iostream>
#ifdef WIN32
    #include <format>
#endif
#include "modules/audio_processing/ns/noise_suppressor.h"

// #include "gamefunc/Os_Control.h"
// Os_Control os_ctl;


#ifdef WIN32
    std::string NOISE_WAV_IN_PATH("../../noise_tmoive.wav");
    std::string DENOISED_WAV_OUT_PATH("../../denoised_tmoive.wav");
#else
    std::string NOISE_WAV_IN_PATH("../noise_tmoive.wav");
    std::string DENOISED_WAV_OUT_PATH("../denoised_tmoive.wav");
#endif

auto DENOISE_LEVEL = webrtc::NsConfig::SuppressionLevel::k12dB;


struct WAV_HEADER{
    char riff_flag[4];
    int wav_size; 
    char wave_flag[4];
    char fmt_flag[4]; 
    int fmt_chunk_size; 
    short audio_format; 
    short num_channels;
    int sample_rate;
    int byte_rate; 
    short sample_alignment; 
    short bit_depth;
    char data_flag[4]; 
    int data_bytes; 
    // pcm data start:
    // 2声道的话数据是 LRLRLRLR记录;
    // 单声道就是 LLLLLLL 这样;

    // 尾部可能有其他文字信息;
};// WAV_HEADER()



int main(){
    if(!std::filesystem::exists(
            std::filesystem::u8path(NOISE_WAV_IN_PATH))){
        #ifdef WIN32
            std::cout << std::format(
                "file not exists: {};\n",
                NOISE_WAV_IN_PATH
            );
        #endif
        return 0;
    }

    // open src noise wav:
    // std::string wav_data = os_ctl.read_all(
    //     NOISE_WAV_IN_PATH, "rb");
    std::ios_base::openmode read_mode = 
        std::fstream::in | std::fstream::binary;
    std::fstream src_wav_fobj(
        std::filesystem::u8path(NOISE_WAV_IN_PATH), read_mode);
    std::string wav_data(
        (std::istreambuf_iterator<char>(src_wav_fobj)), 
        std::istreambuf_iterator<char>() 
    );
    src_wav_fobj.close();

    if(wav_data.size() == 0){
        #ifdef WIN32
            std::cout << std::format(
                "file not exists: {};\n",
                NOISE_WAV_IN_PATH
            );
        #endif
        return 0;
    }// if WAV 文件不存在

    WAV_HEADER *wav_header = (WAV_HEADER*)&wav_data[0];
    if(wav_header->fmt_chunk_size != 16){
        #ifdef WIN32
            std::cout << std::format(
                "not standard: {}:  wav file: {};\n",
                wav_header->fmt_chunk_size,
                NOISE_WAV_IN_PATH
            );
        #endif
        return 0;
    }// if wav chunk size != 16;

    // 取pcm数据:
    if(wav_header->bit_depth != 16){
        #ifdef WIN32
            std::cout << std::format(
                "only support 16bit: this wav is: {}bit;\n",
                wav_header->bit_depth
            );
        #endif
        return 0;
    }// if wav bit depth != 16;

    // 取 pcm array 部分:
    int16_t *pcm_data = (int16_t*)&wav_data[44];
    int num_of_pcm_samples = wav_header->data_bytes 
        / (wav_header->bit_depth / 8);

    webrtc::AudioBuffer audio_buff(
        wav_header->sample_rate, wav_header->num_channels,
        wav_header->sample_rate, wav_header->num_channels,
        wav_header->sample_rate, wav_header->num_channels);

    webrtc::StreamConfig stream_config(
        wav_header->sample_rate, wav_header->num_channels);

    webrtc::NsConfig ns_config;
    ns_config.target_level = DENOISE_LEVEL;

    webrtc::NoiseSuppressor ns(
        ns_config, 
        wav_header->sample_rate, 
        wav_header->num_channels);

    // 采样 == 16K 的话 num_frames() 会得到 160;
    #ifdef WIN32
        std::cout <<  std::format(
            "inti ok: stream_config.num_frames: {}; "
            "num_samples(): {}; "
            "num_channels(): {};"
            "\n",
            stream_config.num_frames(),
            // 每轮处理几帧: impl为: sample_rate_hz / 100 * num_channels;
            stream_config.num_samples(),
            stream_config.num_channels()
        );
    #endif


    bool need_split_bands = wav_header->sample_rate > 16'000;
    for(uint64_t pos = 0; ; ){
        uint64_t next_pos = pos + stream_config.num_samples();
        if(next_pos > num_of_pcm_samples){ break; }
        audio_buff.CopyFrom(&pcm_data[pos], stream_config);
        // 采样 > 16K 要进行分频:
        if(need_split_bands){
            audio_buff.SplitIntoFrequencyBands();
        }// if 需要分频:
      
        ns.Analyze(audio_buff);
        ns.Process(&audio_buff);
        
        // 之前进行过分频处理就合并:
        if(need_split_bands){
            audio_buff.MergeFrequencyBands();
        }
        audio_buff.CopyTo(stream_config, &pcm_data[pos]);

        #ifdef WIN32
            std::cout << std::format(
                "num_of_pcm_samples: {}; now_pos: {}; "
                "next_pos: {}; (num_of_pcm_samples - pos): {}; "
                "stream_config.num_samples(): {}; "
                "\n", 
                num_of_pcm_samples, pos, next_pos,
                num_of_pcm_samples - pos,
                stream_config.num_samples()
                );
        #endif

        pos = next_pos;
    }// for in range


    // os_ctl.write_all(
    //     DENOISED_WAV_OUT_PATH, "wb",
    //     wav_data);
    std::ios_base::openmode write_mode
        = std::fstream::out | std::fstream::binary;
    std::fstream denoised_wav_obj(
        std::filesystem::u8path(DENOISED_WAV_OUT_PATH), 
        write_mode);
    denoised_wav_obj.write(&wav_data[0], wav_data.size());
    denoised_wav_obj.flush();
    denoised_wav_obj.sync();
    denoised_wav_obj.close();


    std::cout << "denoise final" << std::endl;
    std::cout << "report: github: gamefunc; qq: 32686647" << std::endl;
    std::cout << "https://www.gamefunc.top:9029" << std::endl;
    std::cout << "noise_tmoive.wav -> denoised_tmoive.wav" << std::endl;
    return 0;
}// main()
