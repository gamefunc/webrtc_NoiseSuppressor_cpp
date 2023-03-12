webrtc_NoiseSuppressor_cpp
=======
Get all relative code files of webrtc NoiseSuppressor module;  
and a simple wmv denoise example written using cpp code;

Author: gamefunc:
----------------
    website: https://www.gamefunc.top:9029
    github: https://github.com/gamefunc
    qq: 32686647
    weixin: gamefunc
    mail: fevefun@hotmail.com  
    
    
How to use:
----------------
1. gclient sync webrtc code;
2. get_webrtc_ns_relative.py:    
    . Set the following two paths:  
        WEBRTC_INCLUDE_ROOT_PATH =  r"C:\cpps\libs\webrtc\src"  
        WEBRTC_THIRD_PARTY_ROOT_PATH =  r"C:\cpps\libs\webrtc\src\third_party\abseil-cpp"  
    . And run it to get the webrtc ns relative code file:  
3. ok, now you can run my ns_test_unit_wav.cpp;  



Test unit:
----------------
1. get webrtc ns relative code files:  
![image](https://github.com/gamefunc/webrtc_NoiseSuppressor_cpp/blob/main/imgs/0_run_py_get_source_code_compressed.jpg)  
2. do cmake:  
![image](https://github.com/gamefunc/webrtc_NoiseSuppressor_cpp/blob/main/imgs/1_build_cpp_final_compressed.jpg)  
3. do denoise:
![image](https://github.com/gamefunc/webrtc_NoiseSuppressor_cpp/blob/main/imgs/2_run_cpp_compressed.jpg)  

License:
----------------
BSD 3  
free to use and modify, but need keep the above information.  
  

          
