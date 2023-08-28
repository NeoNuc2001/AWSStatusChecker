import boto3,csv
import time
import pyautogui
import tkinter as tk
import datetime
from keyboard_event import *
def main():
    with open("EC2Maneger_accessKeys.csv","r",encoding="UTF-8-sig") as f:
        reader=csv.DictReader(f)
        token=[row for row in reader][0]
    
    ec2_r=boto3.resource("ec2",aws_access_key_id=token['Access key ID'],aws_secret_access_key=token['Secret access key'],region_name='ap-northeast-1')
    print("Executing...")
    while True:
        for inst in ec2_r.instances.all():
            if not inst.state["Name"]=="stopped":
                SafePressKey("up")
                print(f"[{datetime.datetime.now()}]Instance:{inst.instance_id} with instace type:{inst.instance_type} seems to be up.")
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