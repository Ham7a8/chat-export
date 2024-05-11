import re
import pandas as pd
import matplotlib.pyplot as plt

arabic_to_english = {
    "حمزة الريسي": "Hamza Al-Risi",,
}

link = r"C:\Users\hamza\Downloads\chat.txt" 

title = link.split("\\")[-1][:len(link) - 4]

cht = open(link, encoding="utf8")
list_of_date_time_author_msg = []
total_msg = 0
total_msg_and_notification = 0
total_valid_msg = 0

timestamp_pattern = r"^\[(\d{2}/\d{2}/\d{2}), (\d{1,2}:\d{2}:\d{2}\s*[AP]M)\]"


def startsWithDate(s):
    return re.match(timestamp_pattern, s) is not None


def findColon(s):
    return s.count(":") 


while 1:
    rd = cht.readline()
    if not rd:
        break

    total_msg_and_notification += 1
    if startsWithDate(rd):
        match = re.match(timestamp_pattern + r"\s*(.*?):\s*(.*)", rd)
        if match:
            date, time, sender, message = match.groups()
            total_msg += 1
            if findColon(rd) > 0:
                total_valid_msg += 1
                sender_english = arabic_to_english.get(sender, sender)
                list_of_date_time_author_msg.append([date, time, sender_english, message])

cht.close()

print("\n\nTotal msg-", total_msg, "\nTotal valid msg-", total_valid_msg,
      "\ntotal_msg_and_notification", total_msg_and_notification)

df = pd.DataFrame(list_of_date_time_author_msg,
                  columns=["Date", "Time", "GroupMember", "Message"])

member_counts = df['GroupMember'].value_counts()

plt.figure(figsize=(8, len(member_counts) * 0.3))
plt.bar(member_counts.index, member_counts.values, width=0.5) 

plt.title("Group: " + title)
plt.xlabel("Group Members")
plt.ylabel("Number of Messages")
plt.xticks(rotation=90)

for x, y in zip(member_counts.index, member_counts.values):
    plt.text(x, y + 5, str(y), ha='center', color='red')

plt.text(len(member_counts) - len(member_counts) // 2, max(member_counts),
         'Total Active Members: ' + str(len(member_counts)) +
         ", Total Message-" + str(total_valid_msg),
         color='red')

plt.tight_layout() 

plt.show()
