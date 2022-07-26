<h1 align="center">
  <br>
   💸 Custom Server Economy Bot 💸
  <br>
</h1>
<p align="center">A discord bot to implement custom economy for your server! Add, remove, leaderboard, shop, etc available!</p>
<h4 align="center"> Special Thanks to <a href="https://metagoons.gg/">MetaGoons</a> and <a href="https://twitter.com/elitejakey", target="_blank">Jakey</a> for commissioning this bot.</h4>

## ❗ Features
* ✏️ Administrators can add or remove points 
* 🔁 Allows members to see their own and someone else's points
* ❓ Custom help menu 
* 👍 Easy functionality
* 🛒 Shop feature 
* 🔒 Monitor shop purchases by setting up `log_channel` in [config.py](https://github.com/DorianAarno/PointsBot/blob/main/config.py)
* 🧐 Shop prizes can be either role or a DM message 
* ➿ Add unlimited items in the shop 
* 🤖 Supports prefix commands only
* 🆗 See ranks of all members in the leaderboard 


## ❓ How to use it?
In [config.py](https://github.com/DorianAarno/PointsBot/blob/main/config.py) replace `TOKEN` with your application's token. 
**That's it, you're ready to use the bot, you may edit other parameters in config file as per your needs.**

## 📘 Other libraries used
* [disnake-pagination](https://github.com/DorianAarno/Paginator) 
   * [Leaderboard line 67](https://github.com/DorianAarno/PointsBot/blob/main/cogs/points_commands.py)
* [discordpy-antispam](https://github.com/DorianAarno/SpamFilter) 
   * [on_message event line 14](https://github.com/DorianAarno/PointsBot/blob/main/cogs/points_system.py)

 
## 📖 License
Released under the [Apache License 2.0](https://github.com/DorianAarno/PointsBot/blob/main/LICENSE) license.
