login_data = {
    "status": "Success",
    "message": "OTP Generated Successfully",
}
error_json = {
    "status": "Error",
    "message": "Incorrect Request Format",
}
auth_data = {
    "status": "Success",
    "message": "User Authenticated Successfully",
}

profile_json = {
    "status": "Success",
}

user_json = {
    "name": "Test Name",
    "phone": '1111111111'
}

body = {
    "to": "cHpkJCAFQwSL937LKTPHD9:APA91bEjerattHR8BgZvueKY1p9DxmTftbGhJlgeayAKA3pmta5EU2YgZKVPB73WelS8RhUy_SEkLfXZ6Jh2LqfPao4j8AymliH7Fl3t4cVm5lQbeHd-lXneAoF4m3qgD3O3sjQpe2bC",
    "priority":"high",
    "notification" :{
        "body" : "Hello Bro you got a request",
        "title": "India vs. Pakistan",
        "subtitle":"This is Great",
        "android_channel_id": "hello"
    },
    "data": {
        "tag_notification" : "700",
        "tag_call" : "400",
        "tag_ignore": "600"
    }
}

headers = {"Content-Type":"application/json",
        "Authorization": "key=AAAA8c8MGo4:APA91bGurUViWniyZwNqGX98QT7wdm_9byIh6hR1j7woLDG7dAuaU1-7I9cEPyS-5kkwxV3auCHdIUgIGXp8V7vToV6CPD36SabTg5f1G-THYVQxUH2KiARApMFrVDa11VSYmG2UmtCb"}



