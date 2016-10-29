from requests import post


class NotificationService:

    def __init__(self):
        self._firebase_api = 'https://fcm.googleapis.com/fcm/send'
        self._web_api_key = 'AIzaSyDAWg37tH5hyukTXPHUuBZ1UP-GxpNDXTY'
        self._headers = {
            'Content-type': 'application/json',
            'Authorization': 'key={api_key}'.format(api_key=self._web_api_key)
        }

    def __repr__(self):
        pass

    def send_notification(self, notification):
        payload = notification.to_body()
        response = post(
            self._firebase_api,
            headers=self._headers,
            json=payload
        )

        if not response.ok:
            # In the future, error handle, for now, log
            print(response.text)
