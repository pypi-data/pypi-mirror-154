
<p>
    <div align="center">
    <h1>ggpython</h1>
    </div>
</p>

<h4 align="center">Tracker Network Wrapper In Python.</h4>

<p align="center">
  <a>
    <img alt="AppVeyor badge" src="https://img.shields.io/badge/build-passing-brightgreen">
  </a>
  <a href = "https://github.com/nakashimas/ggpython/releases">
    <img src="https://img.shields.io/badge/releace-v0.0.1%20-58839b.svg?style=flat">
  </a>
  <a href="./LICENSE">
    <img src="http://img.shields.io/badge/license-MIT-blue.svg?style=flat">
  </a>
  <br>
  <a>
    <img src="https://img.shields.io/badge/platform-win--32%20%7C%20win--64-lightgrey">
  </a>
</p>

<h2> Contents </h2>

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)
- [License](#license)
- [Requirements](#requirements)
- [Release signature](#release-signature)
- [Development](#development)
- [Author](#author)

## Description

TrackerNetwork 非公式API。  
Discord bot 用に作成しているものをPythonライブラリとして管理している。

Among its features... :

- ゲームの情報を取得する機能
  - Valorant (Match, PlayableCharacter, Map, Weapon, Custom, Award, and its Summary)
- 文字列整形機能
  - for console standard output.
  - for Discord text chat output.
- スクレイピング用のChromiumエンジンWrapper

For more information, refer to the [Documentation](https://nakashimas.github.io/ggpython/html/index.html) 
or [Sample](https://github.com/nakashimas/ggpython/blob/master/SAMPLE.md).


## Installation

You can [Download](https://github.com/nakashimas/ggpython/releases) the latest installable version of _ggpython_ for Windows (zip format).

The simplest way to install the latest version from PyPI is by using:

```sh
pip install --upgrade ggpython
```

If you want to install this for development purposes,  
you can install directly from the GitHub repository:

```sh
git clone https://github.com/nakashimas/ggpython.git
cd ggpython
pip install .
```

also following:

```sh
pip install git+https://github.com/nakashimas/ggpython
```


## Usage

Valorantのマッチリザルトを取得できる。(最大20件)

```py
from ggpython import GGTrackerAPI, GAME

with GGTrackerAPI(GAME.VALORANT) as gg:
    res = gg.get_match_result("Username", "#tag", mode = "unrated")
```

Discord Bot用に出力結果を整形できる。(調整中)

サンプル: 

```py
print(convert_valorant_match_to_discord(res))
# -> to paste discord plane text
```

結果: 

<p style="text-align:center;">
  <img src="https://github.com/nakashimas/ggpython/blob/master/img/discord_1.png?raw=true" style="width:60%"/>
</p>

Discordサーバに絵文字を登録しておく必要がある


## Documentation

Document is available from [there](https://nakashimas.github.io/ggpython/html/index.html).


## License

This project is licensed under the terms of the [MIT](https://github.com/nakashimas/ggpython/blob/master/LICENSE).

このプロジェクトは [MIT](https://github.com/nakashimas/ggpython/blob/master/LICENSE) ライセンスに基づいて管理されています。


## Requirements

- selenium
- chromedriver_binary
- chromedriver_autoinstaller

You find requirements at also [requirements.txt](https://github.com/nakashimas/ggpython/blob/master/requirements.txt).


## Release signature

- ggpython-0.0.1-py3-none-any.whl
- ggpython-0.0.1.tar.gz


## Development

We would love to have you as part of the community.
If you find a bug / new-feature, feel free to write a new [Issue](https://github.com/nakashimas/ggpython/issues) with a *respective title* and *description* on this repository. 

If you need help with an [Issue](https://github.com/nakashimas/ggpython/issues) or Development, please refer to the [guidelines](https://github.com/nakashimas/ggpython/blob/master/SAMPLE.md#development) or ask [me](https://github.com/nakashimas).


## Author

_ggpython_ authors.
