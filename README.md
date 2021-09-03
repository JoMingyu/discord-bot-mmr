# What is my MMR?
<img width="357" alt="스크린샷 2021-09-03 오후 8 29 42" src="https://user-images.githubusercontent.com/21031883/131998867-507429c8-89f1-45c4-8ff4-44f4ae69857a.png">

MMR 알려주는 디스코드 봇입니다. 명령어는 `/mmr {nickname}` 하나밖에 없음. 데이터 근거는 [whatismymmr API](https://dev.whatismymmr.com/) 이용.

[봇 추가하는 링크](https://discord.com/api/oauth2/authorize?client_id=882649601188958248&permissions=2048&scope=bot)

## Deployment
heroku로 올리고, bot token은 heroku app에 envvar로 추가해 뒀습니다. 코드 공개를 하면서 token은 비밀로 해야 하다보니 어쩔수 없었음. 
