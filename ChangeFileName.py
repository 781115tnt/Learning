import re
from pathlib import Path

DIR = Path("/Volumes/3TB-A/_NEW")

def rename_files_regex():
    for path in DIR.iterdir():
        if path.is_file():
            new_name = path.stem
            new_name = re.sub(r"(\d+)\.(\d{4})", r"\2.\1", new_name) #n.nnnn to nnnn.n
            new_name = re.sub(r"(\d{4})-(\d+)", r"\1.\2", new_name) #nnnn- to nnnn.n
            new_name = re.sub(r"([A-Za-z])-([A-Za-z])", r"\1\2", new_name) #c-c to cc
            new_name = re.sub(r'\[[^\]]+\]\s', '', new_name).lstrip().rstrip() #c-c to cc
            path.rename(path.with_name(f"{new_name}{path.suffix}"))
            #print(f"{path.stem} -> {new_name}")


def rename_files(replace_list, replacement):
    for path in DIR.iterdir():
        if path.is_file():
            new_name = path.stem
            for s in replace_list:
                new_name = new_name.replace(s, replacement)
            path.rename(path.with_name(f"{new_name}{path.suffix}"))
            #print(new_name)


def set_publisher_title():
    for path in DIR.iterdir():
        if path.is_file():
            s = path.stem
            publisher, title = s.split("-", 1) if "-" in s else (s, "")
            
            new_name = path.stem

            if publisher != "":
                new_name = f"{title}--{publisher}".rstrip().lstrip()

            path.rename(path.with_name(f"{new_name}{path.suffix}"))
            #print(f"{path.stem}->{new_name}")


def chgname():
    list1 = ["(", ")"]
    str1 = ""
    rename_files(list1, str1)

    rename_files_regex()

    list1 = ["Maven Analytics -"]
    str1 = "MavenAnalytics -"
    rename_files(list1, str1)

    list1 = ["Frontend Masters -"]
    str1 = "FrontendMasters -"
    rename_files(list1, str1)

    list1 = ["Pack -"]
    str1 = "Packt -"
    rename_files(list1, str1)

    list1 = [","]
    str1 = " "
    rename_files(list1, str1)

    list1 = ["Nodejs", "NodeJs", "Node.js", "Node.JS", "node.js", "node.Js"]
    str1 = "NodeJS"
    rename_files(list1, str1)

    list1 = ["Nextjs", "NextJs", "Next.js", "Next.JS", "next.js", "next.Js"]
    str1 = "NextJS"
    rename_files(list1, str1)

    list1 = ["csharp", "Csharp", "CSharp", "C Sharp", "C sharp"]
    str1 = "C#"
    rename_files(list1, str1)

    list1 = ["cpp", "CPP", "C p p", "C P P", "C + +", "c++"]
    str1 = "C++"
    rename_files(list1, str1)

    list1 = ["DOTNET", "Dotnet", "dotnet", "DOT NET", "dot net", "Dot Net"]
    str1 = "NET"
    rename_files(list1, str1)

    list1 = ["FASTAPI", "Fastapi", "fastapi", "FAST API", "Fast API", "fast api"]
    str1 = "FastAPI"
    rename_files(list1, str1)

    list1 = ["ASP ", "Asp ", "asp "]
    str1 = "ASP "
    rename_files(list1, str1)

    list1 = ["ASP.NET"]
    str1 = "ASP NET"
    rename_files(list1, str1)

    list1 = ["qt", "QT"]
    str1 = "Qt"
    rename_files(list1, str1)

    list1 = ["  "]
    str1 = " "
    rename_files(list1, str1)

chgname()

set_publisher_title()
