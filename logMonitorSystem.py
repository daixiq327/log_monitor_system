import re
import time
import threading
import smtplib
from email.mime.text import MIMEText

files = [
    file_path1,
    file_path2,
    file_path3
]

sender = 'xxx@163.com'
receiver = ['xxx@xx.com']
mail_host = 'smtp.163.com'
mail_user = 'xxx@163.com'
title = 'logErrorReport'


class Tail(object):
    def __init__(self, tailed_file):
        self.tailed_file = tailed_file

    def follow(self, s=1):
        with open(self.tailed_file) as file_:
            file_.seek(0, 2)
            while True:
                flag = 0
                curr_position = file_.tell()
                line = file_.readlines()
                str_line = []
                if not line:
                    file_.seek(curr_position)
                    time.sleep(s)
                else:
                    for line1 in line:
                        if flag == 1:
                            str_line.append(line1)
                            res2 = re.findall(".*Error.*", line1)
                            if res2 != []:
                                flag = 0
                        else:
                            res1 = re.findall(".*Traceback.*", line1)
                            if res1 != []:
                                flag = 1
                                str_line.append(line1)
                    i = 0
                    while i < len(str_line):
                        if str_line[i].find('RuntimeError') == -1:
                            i += 1
                        else:
                            for j in range(i, -1, -1):
                                if str_line[j].find('Traceback') == -1:
                                    str_line.pop(j)
                                else:
                                    str_line.pop(j)
                                    i = j - 1
                                    break
                    x = ''.join(list(str_line))
                    file_.seek(0, 2)
                    if x != '':
                        print x
                        x = self.tailed_file + '\n' + x
                        msg = MIMEText(x, 'plain', 'utf-8')
                        msg['From'] = '{}'.format(sender)
                        msg['To'] = ','.join(receiver)
                        msg['Subject'] = 'logErrorReport'
                        try:
                            server = smtplib.SMTP_SSL(mail_host, 465)
                            server.login(mail_user, 'xxx')
                            server.sendmail(sender, receiver, msg.as_string())
                            print 'mail has been send successfully'
                        except smtplib.SMTPException as e:
                            print e


def tail_thread(f):
    t = Tail(f)
    t.follow(5)


if __name__ == '__main__':
    for f in files:
        thread = threading.Thread(target=tail_thread, args=(f,))
        thread.start()