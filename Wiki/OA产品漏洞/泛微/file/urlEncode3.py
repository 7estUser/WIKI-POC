import os
def main():
    clearFlag = "y"
    while(1):
        if clearFlag == "y" or clearFlag == "Y":
            os.system("cls")
        clearFlag = ""
        string = input("请输入需要转换的字符串 :")
        type = input("(输入1：进行三次url全字符编码 ) :")
        while(type != "1"):
            type = input("操作类型输入错误(输入1：进行三次url全字符编码) :")
        if type == "1" :
            for i in range(3):
                string = encode(string)
            encode_string = string
            print("编码结果为："+encode_string+"\n")

#编码
def encode(string):
    encode_string = ""
    for char in string:
        encode_char = hex(ord(char)).replace("0x","%")
        encode_string += encode_char
    return encode_string
main()