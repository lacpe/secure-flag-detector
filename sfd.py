import subprocess
import re


def check_flag_secure(path: str):
    search_term_1 = "Landroid/view/Window;->setFlags(II)V"
    results = subprocess.run(["grep", "-r", search_term_1, path], capture_output=True).stdout.decode("UTF-8").split("\n")
    for r in results:
        if r == '':
            continue
        path = r[:r.find(".smali:") + 6]
        line = r[r.find(".smali:") + 11:]
        method_expression = "invoke-virtual \{.*, (?P<varname>.*), (?P=varname)\}, Landroid/view/Window;->setFlags\(II\)V"
        variable_name = re.search(method_expression, line).group('varname')
        constant_expression = variable_name + ".*0x20000"
        const_index = 0
        const_line = ""
        method_index = 0
        method_line = ""
        with open(path, "r+") as f:
            lines = f.read().split("\n")
            for i, v in enumerate(lines):
                if re.search(constant_expression, v) is not None:
                    const_index = i
                    const_line = v
                if re.search(method_expression, v) is not None:
                    method_index = i
                    method_line = v
            if const_index < method_index:
                package_path_start = path.rfind('/') + 1
                print(f"FLAG_SECURE set for {search_path[package_path_start:]} at location {path[package_path_start:]}"
                      f"\nLine n°{const_index}: {const_line}"
                      f"\nLine n°{method_index}: {method_line}")
        f.close()



if __name__ == "__main__":
    search_path = "PATH TO UNPACKED APK HERE"
    check_flag_secure(search_path)
