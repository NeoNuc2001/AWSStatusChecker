import boto3,csv
import time
import pyautogui
import tkinter as tk
import datetime
import os
from keyboard_event import *
from glob import glob
def load_api_key(folder_path="./api_fol"):
    files=glob(folder_path+"/*.csv")
    files.sort(key=os.path.getmtime)
    token=None
    for file in files:
        with open(file,"r",encoding="UTF-8-sig") as f:
            reader=csv.DictReader(f)
            token=[row for row in reader][0]
        if 'Access key ID' in token.keys() and 'Secret access key' in token.keys():
            break
    if token is None:
        raise FileNotFoundError("Failed to load API file. Please check if your API key file is in \"api_fol\" folder.")
    return token
def main():
    RED = '\033[31m'
    END = '\033[0m'
    token=load_api_key()
    ec2_r=boto3.resource("ec2",aws_access_key_id=token['Access key ID'],aws_secret_access_key=token['Secret access key'],region_name='ap-northeast-1')
    print("Executing...")
    while True:
        for inst in ec2_r.instances.all():
            status=inst.state["Name"]
            if status=="running":
                SafePressKey("up")
                print(f"[{datetime.datetime.now()}]Instance:{inst.instance_id} with instace type:{RED}{inst.instance_type}{END} seems to be up.")
            elif status=="terminated":
                print(f"[{datetime.datetime.now()}]Instance:{inst.instance_id} with instace type:{RED}{inst.instance_type}{END} seems to be terminated.")
        time.sleep(60*5)        


class EC2GUI(tk.Frame):
    def __init__(self):
        with open("EC2Maneger_accessKeys.csv","r",encoding="UTF-8-sig") as f:
            reader=csv.DictReader(f)
            token=[row for row in reader][0]
        self.ec2_r=boto3.resource("ec2",aws_access_key_id=token['Access key ID'],aws_secret_access_key=token['Secret access key'],region_name='ap-northeast-1')

    def update(self):
        for inst in self.ec2_r.instancesa.all():
            
            pass
        self.after(1000*60,self.update)
        
if __name__ =="__main__":
    main()