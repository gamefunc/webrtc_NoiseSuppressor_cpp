
"""
get webrtc NoiseSuppressor modules relative code files from webrtc source;

this script need have webrtc full project code:
    and need setting:
        WEBRTC_INCLUDE_ROOT_PATH
        WEBRTC_THIRD_PARTY_ROOT_PATH

author: gamefunc
    website: https://www.gamefunc.top:9029
    github: https://github.com/gamefunc
    qq: 32686647
    weixin: gamefunc
    mail: fevefun@hotmail.com
free to use and modify, but need keep the above information.

test env: win 10;
"""

import os, sys, re, shutil, re

F = os.path.dirname(__file__)


# webrtc_ns root path:
WEBRTC_INCLUDE_ROOT_PATH = r"C:\cpps\libs\webrtc\src"

# webrtc_ns third party include dir:
WEBRTC_THIRD_PARTY_ROOT_PATH = r"C:\cpps\libs\webrtc\src\third_party\abseil-cpp"

# copy webrtc ns modules relative code file to:
CODE_FILES_OUT_DIR_PATH = F
# do real copy, not just print copy cmd:
IS_DO_REAL_COPY = True


# webrtc_ns need parse code files: sep must: "/" :
WEBRTC_NS_FILES_RPATHS = [
    "modules/audio_processing/ns/noise_suppressor.cc",
    "common_audio/audio_util.cc",
    "common_audio/resampler/sinc_resampler_sse.cc",
    "common_audio/signal_processing/splitting_filter.c",
    # "common_audio/resampler/sinc_resampler_avx2.cc",
    # "system_wrappers/source/cpu_features.cc",
    # "system_wrappers/source/field_trial.cc",

    # arm :
    # "common_audio/resampler/sinc_resampler_neon.cc",
]

WEBRTC_INCLUDE_ROOT_PATH = os.path.normcase(
    WEBRTC_INCLUDE_ROOT_PATH)
WEBRTC_THIRD_PARTY_ROOT_PATH = os.path.normcase(
    WEBRTC_THIRD_PARTY_ROOT_PATH)



# 还需要查找同目录下哪些文件:
CODE_FILE_EXTS = ["cc", "cpp", "h", "hpp", "ipp", "c"]
PARSED_FILES_ABS_PATH = []
ALL_NEED_INCLUDES_AND_CC_FILES = {}
NOT_FOUND_INCLUDES = {}



class Cpp_Parse:
    @staticmethod
    def get_includes(file_abs_path: str) -> list:
        includes_paths = []
        p = r'#include[^\"\']*[\"\'][^\"\']*[\"\']'
        into_comment = False
        with open(file_abs_path, 
                "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("/*"):
                    into_comment = True
                    continue
                if line.endswith("*/"):
                    into_comment = False
                    continue
                if line.startswith("//"): continue
                if into_comment: continue

                result = re.findall(p, line)
                if len(result) != 1: continue
                include_path = result[0].replace(
                    "#include", "", 1)
                for s in ['"', '"']:
                    include_path = include_path.replace(
                        s, "")
                include_path = include_path.strip()
                includes_paths.append(include_path)

        return list(set(includes_paths))
                




def search_includes(file_abs_path: str):
    global WEBRTC_INCLUDE_ROOT_PATH
    global WEBRTC_THIRD_PARTY_ROOT_PATH
    global ALL_NEED_INCLUDES_AND_CC_FILES
    global CODE_FILE_EXTS
    global PARSED_FILES_ABS_PATH
    global NOT_FOUND_INCLUDES

    # 规范化系统路径:
    file_abs_path = os.path.normcase(file_abs_path)
    # 去掉 "../../" 这些:
    file_abs_path = os.path.normpath(file_abs_path)

    if not os.path.exists(file_abs_path):
        return

    if file_abs_path in PARSED_FILES_ABS_PATH:
        return
    
    PARSED_FILES_ABS_PATH.append(file_abs_path)


    # 查看该文件下是否有其他c, cpp, hpp 等文件:
    this_file_prefix = file_abs_path.rsplit(".", 1)[0]
    for ext in CODE_FILE_EXTS:
        search_includes(f"{this_file_prefix}.{ext}")
    

    this_file_folder_path = os.path.dirname(
        file_abs_path)

    includes_paths = Cpp_Parse.get_includes(
        file_abs_path)
    for include_path in includes_paths:
        # 直接本文件夹内开始找:
        path1 = os.path.join(
            this_file_folder_path,
            include_path)
        # 在根目录找:
        path2 = os.path.join(
            WEBRTC_INCLUDE_ROOT_PATH,
            include_path)
        # 在第3方目录找:
        path3 = os.path.join(
            WEBRTC_THIRD_PARTY_ROOT_PATH,
            include_path)
        if (path1 in ALL_NEED_INCLUDES_AND_CC_FILES) or (
                path2 in ALL_NEED_INCLUDES_AND_CC_FILES) or (
                path3 in ALL_NEED_INCLUDES_AND_CC_FILES
                ):
            continue
        if os.path.exists(path1):
            ALL_NEED_INCLUDES_AND_CC_FILES[path1] = include_path
            search_includes(path1)
        elif os.path.exists(path2):
            ALL_NEED_INCLUDES_AND_CC_FILES[path2] = include_path
            search_includes(path2)
        elif os.path.exists(path3):
            ALL_NEED_INCLUDES_AND_CC_FILES[path3] = include_path
            search_includes(path3)
        else:
            if file_abs_path not in NOT_FOUND_INCLUDES:
                NOT_FOUND_INCLUDES[file_abs_path] = []
            if include_path in NOT_FOUND_INCLUDES[file_abs_path]:
                continue
            NOT_FOUND_INCLUDES[file_abs_path].append(
                include_path)



def copy_code_files_to_out_dir():
    global CODE_FILES_OUT_DIR_PATH
    global CODE_FILE_EXTS
    global PARSED_FILES_ABS_PATH
    global ALL_NEED_INCLUDES_AND_CC_FILES
    global WEBRTC_NS_FILES_RPATHS
    
    # 输出目录不存在就创建:
    if not os.path.exists(CODE_FILES_OUT_DIR_PATH):
        os.makedirs(CODE_FILES_OUT_DIR_PATH)

    # for 相对路径: 所有相对路径:
    for file_abs_path in ALL_NEED_INCLUDES_AND_CC_FILES:
        rpath = ALL_NEED_INCLUDES_AND_CC_FILES[file_abs_path]
        rdir = os.path.dirname(rpath)
        out_dir_abs_path = os.path.join(
            CODE_FILES_OUT_DIR_PATH, rdir)
        if not os.path.exists(out_dir_abs_path):
            os.makedirs(out_dir_abs_path)

        src_files_abs_path_prefix = file_abs_path.rsplit(".", 1)[0]
        for ext in CODE_FILE_EXTS:
            src_abs_path = f"{src_files_abs_path_prefix}.{ext}"
            src_file_name = os.path.basename(src_abs_path)
            out_abs_path = os.path.join(
                out_dir_abs_path, src_file_name)
            if os.path.exists(src_abs_path):
                print(f"cp {src_abs_path} -> {out_abs_path}")
                if IS_DO_REAL_COPY:
                    shutil.copy(src_abs_path, out_abs_path)




def  modify_common_audio_resampler_sinc_resampler_cc():
    code_file_abs_path = os.path.join(
        CODE_FILES_OUT_DIR_PATH,
        "common_audio/resampler/sinc_resampler.cc")

    func_impl = """
// gamefunc modify start: bug report: github: gamefunc; qq: 32686647;
void SincResampler::InitializeCPUSpecificFeatures() {
    #if defined(WEBRTC_HAS_NEON)
        convolve_proc_ = Convolve_NEON;
    #elif defined(WEBRTC_ARCH_X86_FAMILY)
        convolve_proc_ = Convolve_SSE;
    #else
        // Unknown architecture.
        convolve_proc_ = Convolve_C;
    #endif
}// InitializeCPUSpecificFeatures()
// gamefunc modify end: bug report: github: gamefunc; qq: 32686647;
    """

    msg = """########## gamefunc modify start:
# 文件: "common_audio/resampler/sinc_resampler.cc":
    void SincResampler::InitializeCPUSpecificFeatures(){
        impl..
    }

# replace to: 
        func_impl
# and // include: cpu_features_wrapper.h;
########## gamefunc modify end;
    """.replace("func_impl", func_impl)

    if not os.path.exists(code_file_abs_path):
        print(f"{code_file_abs_path} not exist: modify yourself")
        print(msg)
        return

    
    out_code_txt = ""
    into_function_impl = False
    with open(code_file_abs_path, 
            "r", encoding="utf-8") as f:
        for line in f:
            # 改函数:
            if "void SincResampler::InitializeCPUSpecificFeatures()" in line:
                into_function_impl = True
                out_code_txt += func_impl
                continue
            if into_function_impl and ("}\n" in line):
                into_function_impl = False
                continue
            if into_function_impl: continue

            # 改 include:
            if '#include "system_wrappers/include/cpu_features_wrapper.h"' in line:
                out_code_txt += "// "

            out_code_txt += line

    with open(code_file_abs_path, 
            "w", encoding="utf-8",
            newline="\n") as f:
        f.write(out_code_txt)
    
    print(msg)



"""
main()
"""
def main():
    global ALL_NEED_INCLUDES_AND_CC_FILES

    for rpath in WEBRTC_NS_FILES_RPATHS:
        print(f"will parse: {rpath}")
        abs_path = os.path.join(
            WEBRTC_INCLUDE_ROOT_PATH, rpath)
        search_includes(abs_path)
        ALL_NEED_INCLUDES_AND_CC_FILES[abs_path] = \
            rpath

    copy_code_files_to_out_dir()

    print("found:")
    for x in ALL_NEED_INCLUDES_AND_CC_FILES:
        print(f"    {ALL_NEED_INCLUDES_AND_CC_FILES[x]}: {x}")

    print("\nnot found:")
    for x in NOT_FOUND_INCLUDES:
        print(f"    {x}: {NOT_FOUND_INCLUDES[x]}")

    modify_common_audio_resampler_sinc_resampler_cc()

    print("report: github: gamefunc; qq: 32686647;")
    print("https://www.gamefunc.top:9029")


main()




