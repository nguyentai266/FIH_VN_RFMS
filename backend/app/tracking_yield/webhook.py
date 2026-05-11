from json import dumps

from httplib2 import Http

url = "https://chat.googleapis.com/v1/spaces/AAQAKkrRG6w/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=f33fCHEzxgYeD8-qQUyDVCJbSQFG4rNIg5-hG-5WIIE"
def notify_send_message(payload):
    headers= {"Content-Type": "application/json; charset=UTF-8"}
    http_obj=Http()

    response = http_obj.request(
        uri=url,
        method="POST",
        headers=headers,
        body=dumps(payload),
    )
