# Code review bot
This bot was made for getting automated updates about changing status of code review. Every 20 minutes it sends a request to the API of the online education platform and sends a message to Telegram in case of change in status of code review. It also logs cases of getting the wrong answer from server. You have to enroll the course to get authentication from API of the platform.


# To-do 
- expand events that are logged 
  - absence of required environment variables at the moment of start (level CRITICAL) 
  - message was sent  (level INFO)
  - failed to send message to Telegram (level ERROR)
  - endpoint of education platform isn't responding and any other error connected with endpoint response (level ERROR)