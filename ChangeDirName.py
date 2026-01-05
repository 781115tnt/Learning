import re
from pathlib import Path

DIR = Path("/Volumes/3TB-B/_NEWDIR")

def rename_dirs_regex():
    for path in DIR.iterdir():
        if path.is_dir():
            new_name = path.name
            new_name = re.sub(r"(\d+)\.(\d{4})", r"\2.\1", new_name) #n.nnnn to nnnn.n
            new_name = re.sub(r"(\d{4})-(\d+)", r"\1.\2", new_name) #nnnn- to nnnn.n
            new_name = re.sub(r"([A-Za-z])-([A-Za-z])", r"\1\2", new_name) #c-c to cc
            new_name = re.sub(r'\[[^\]]+\]\s', '', new_name).lstrip().rstrip() #c-c to cc
            path.rename(path.with_name(new_name))
            #print(f"{path.name} -> {new_name}")



def rename_dirs(replace_list, replacement):
    for path in DIR.iterdir():
        if path.is_dir():
            new_name = path.name
            for s in replace_list:
                new_name = new_name.replace(s, replacement).lstrip().rstrip()
            path.rename(path.with_name(new_name))
            #print(f"{path.name} -> {new_name}")


def set_publisher_title():
    for path in DIR.iterdir():
        if path.is_dir():
            s = path.name
            publisher, title = s.split("-", 1) if "-" in s else (s, "")
            
            new_name = path.name

            if publisher != "":
                new_name = f"{title}--{publisher}".rstrip().lstrip()

            path.rename(path.with_name(new_name))
            #print(f"{path.name} -> {new_name}")


def chgname():
    list1 = ["(", ")"]
    str1 = ""
    rename_dirs(list1, str1)

    rename_dirs_regex()

    list1 = ["Maven Analytics -"]
    str1 = "MavenAnalytics -"
    rename_dirs(list1, str1)

    list1 = ["Frontend Masters -"]
    str1 = "FrontendMasters -"
    rename_dirs(list1, str1)

    list1 = ["Pack -"]
    str1 = "Packt -"
    rename_dirs(list1, str1)

    list1 = [","]
    str1 = " "
    rename_dirs(list1, str1)

    list1 = ["Nodejs", "NodeJs", "Node.js", "Node.JS", "node.js", "node.Js"]
    str1 = "NodeJS"
    rename_dirs(list1, str1)

    list1 = ["Nextjs", "NextJs", "Next.js", "Next.JS", "next.js", "next.Js"]
    str1 = "NextJS"
    rename_dirs(list1, str1)

    list1 = ["csharp", "Csharp", "CSharp", "C Sharp", "C sharp"]
    str1 = "C#"
    rename_dirs(list1, str1)

    list1 = ["cpp", "CPP", "C p p", "C P P", "C + +", "c++"]
    str1 = "C++"
    rename_dirs(list1, str1)

    list1 = ["DOTNET", "Dotnet", "dotnet", "DOT NET", "dot net", "Dot Net"]
    str1 = "NET"
    rename_dirs(list1, str1)

    list1 = ["FASTAPI", "Fastapi", "fastapi", "FAST API", "Fast API", "fast api"]
    str1 = "FastAPI"
    rename_dirs(list1, str1)

    list1 = ["ASP ", "Asp ", "asp "]
    str1 = "ASP "
    rename_dirs(list1, str1)

    list1 = ["ASP.NET"]
    str1 = "ASP NET"
    rename_dirs(list1, str1)

    list1 = ["qt", "QT"]
    str1 = "Qt"
    rename_dirs(list1, str1)

    list1 = ["  "]
    str1 = " "
    rename_dirs(list1, str1)

chgname()

set_publisher_title()

