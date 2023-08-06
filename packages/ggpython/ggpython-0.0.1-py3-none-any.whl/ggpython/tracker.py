# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## tracker.py
# ## 
# ##############################################################################
# =============================================================================>
# Definition
VALORANT_TRACKER_WEBSITE = "https://tracker.gg/valorant/"
VALORANT_AGENT_ICONS = {
    "jett"      : "https://titles.trackercdn.com/valorant-api/agents/add6443a-41bd-e414-f6ad-e58d267f4e95/displayicon.png",
    "kayo"      : "https://titles.trackercdn.com/valorant-api/agents/601dbbe7-43ce-be57-2a40-4abd24953621/displayicon.png",
    "fade"      : "https://titles.trackercdn.com/valorant-api/agents/dade69b4-4f5a-8528-247b-219e5a1facd6/displayicon.png",
    "brimstone" : "https://titles.trackercdn.com/valorant-api/agents/9f0d8ba9-4140-b941-57d3-a7ad57c6b417/displayicon.png",
    "viper"     : "https://titles.trackercdn.com/valorant-api/agents/707eab51-4836-f488-046a-cda6bf494859/displayicon.png",
    "omen"      : "https://titles.trackercdn.com/valorant-api/agents/8e253930-4c05-31dd-1b6c-968525494517/displayicon.png",
    "killjoy"   : "https://titles.trackercdn.com/valorant-api/agents/1e58de9c-4950-5125-93e9-a0aee9f98746/displayicon.png",
    "cypher"    : "https://titles.trackercdn.com/valorant-api/agents/117ed9e3-49f3-6512-3ccf-0cada7e3823b/displayicon.png",
    "sova"      : "https://titles.trackercdn.com/valorant-api/agents/320b2a48-4d9b-a075-30f1-1f93a9b638fa/displayicon.png",
    "sage"      : "https://titles.trackercdn.com/valorant-api/agents/569fdd95-4d10-43ab-ca70-79becc718b46/displayicon.png",
    "phoenix"   : "https://titles.trackercdn.com/valorant-api/agents/eb93336a-449b-9c1b-0a54-a891f7921d69/displayicon.png",
    "reyna"     : "https://titles.trackercdn.com/valorant-api/agents/a3bfb853-43b2-7238-a4f1-ad90e9e46bcc/displayicon.png",
    "raze"      : "https://titles.trackercdn.com/valorant-api/agents/f94c3b30-42be-e959-889c-5aa313dba261/displayicon.png",
    "breach"    : "https://titles.trackercdn.com/valorant-api/agents/5f8d3a7f-467b-97f3-062c-13acf203c006/displayicon.png",
    "skye"      : "https://titles.trackercdn.com/valorant-api/agents/6f2a04ca-43e0-be17-7f36-b3908627744d/displayicon.png",
    "yoru"      : "https://titles.trackercdn.com/valorant-api/agents/7f94d92c-4234-0a36-9646-3a87eb8b5c89/displayicon.png",
    "astra"     : "https://titles.trackercdn.com/valorant-api/agents/41fb69c1-4189-7b37-f117-bcaf1e96f1bf/displayicon.png",
    "chamber"   : "https://titles.trackercdn.com/valorant-api/agents/22697a3d-45bf-8dd7-4fec-84a9e28c69d7/displayicon.png",
    "neon"      : "https://titles.trackercdn.com/valorant-api/agents/bb2a4828-46eb-8cd1-e765-15848195d751/displayicon.png"
}

CHROME_UPDATE = True

# =============================================================================> 
# imports default
from xml.etree import ElementTree
import urllib.parse
import re
import time
import functools

# =============================================================================> 
# imports third party
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import chromedriver_binary
import chromedriver_autoinstaller as chromedriver

try:
    if CHROME_UPDATE:
        chromedriver.install()
except Exception as e:
    print("ERRR:", e)

# =============================================================================> 
# imports local

# =============================================================================> 
# define local metod

def dict_find_key(_dict, _value):
    key_list = list(_dict.keys())
    value_list = list(_dict.values())
    _pos = value_list.index(_value)
    return key_list[_pos]

# =============================================================================> 
# define class

class WebsiteAPI(webdriver.Chrome):
    """WebsiteAPI

    Args:
        webdriver.Chrome (_type_): _description_
    References:
        - to solve `--headless timeout`
            https://stackoverflow.com/questions/67744514/timeout-exception-error-on-using-headless-chrome-webdriver
    """
    # =========================================================================>
    # Default
    def __init__(self, *args, **kwargs):
        """ __init__ """
        self.options = webdriver.ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--ignore-ssl-errors')
        self.options.add_argument('--headless')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        webdriver.Chrome.__init__(self, *args, options = self.options, **kwargs)

        self.set_window_size("12000", "11000")
    
    def __del__(self):
        """ __del__ """
        try:
            self.quit()
        except Exception as e:
            print("_____", "close error")
    
    def __enter__(self):
        """ __enter__ """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """ __exit__ """
        try:
            self.quit()
        except Exception as e:
            print("_____", "close error")
    
    def __str__(self):
        """ __str__ """
        return "WebsiteAPI"
    
    # =========================================================================>
    # SetGet
    @property
    def options(self):
        """ get options """
        return self.__options
    
    @options.setter
    def options(self, options):
        """ set options """
        if options is None:
            raise TypeError('invalid options')
        self.__options = options

    # =========================================================================>
    # Utils
    def wait_element(self, seconds, element_by = By.CLASS_NAME, target_string = "", timeout = 30):
        wait = WebDriverWait(self, timeout)
        element = wait.until(
            expected_conditions.presence_of_element_located(
                (element_by, target_string)
            )
        )
        time.sleep(seconds)
        return element
    
    def wait_element_clickable(self, seconds, element_by = By.CLASS_NAME, target_string = "", timeout = 30):
        wait = WebDriverWait(self, timeout)
        element = wait.until(
            expected_conditions.element_to_be_clickable(
                (element_by, target_string)
            )
        )
        time.sleep(seconds)
        return element


class ValorantTrackerWebsiteAPI(WebsiteAPI):
    def __init__(self):
        super().__init__()
    
    # =========================================================================>
    # Class Method
    @classmethod
    def get_match_result(cls, match_url):
        """_summary_

        Args:
            match_url (_type_): _description_
        Returns:
            {
                Agents, PartyNumber,
                Name, Name Tag, CurrentRank, 
                ACS, K, D, A, PM, KD, 
                ADR, HS, FK, FD, MK, Econ
            }
        """
        _output = {}

        match_driver = WebsiteAPI()
        match_driver.get(match_url)
        
        match_driver.wait_element(2.0, element_by = By.CSS_SELECTOR, target_string = ".scoreboard__table:last-child")
        team_elements = match_driver.find_elements(By.CSS_SELECTOR, ".scoreboard__table tbody")

        # =====================================================================>
        # .scoreboard__table tbodyを取得 <- チーム毎
        # tr を取得                      <- ユーザー毎
        # td を取得
        #     td0  キャラ img:src
        #          パーティ svg:class party--color-*
        #          ユーザー名 span.trn-ign__username:inner-html
        #          ユーザータグ span.trn-ign__discriminator:inner-html
        #     td1  ランク img:title
        #     td2- inner-html
        # =====================================================================>
        user_list = []
        for team_number in range(len(team_elements)):
            team_members = team_elements[team_number].find_elements(By.TAG_NAME, "tr")
            for member_rank in range(len(team_members)):
                # =============================================================>
                member_status = team_members[member_rank].find_elements(By.TAG_NAME, "td")
                _res = {}
                # =============================================================>
                _res["Team"] = team_number + 1
                _res["TeamRank"] = member_rank + 1

                # =============================================================>
                # get agents
                _tmp_agent = member_status[0].find_elements(By.TAG_NAME, "img")
                if len(_tmp_agent) > 0:
                    _tmp_agent = dict_find_key(VALORANT_AGENT_ICONS, str(_tmp_agent[0].get_attribute("src")))
                    _res["Agents"] = _tmp_agent
                else:
                    _res["Agents"] = "error"

                # =============================================================>
                # get party number
                _tmp_party = member_status[0].find_elements(By.TAG_NAME, "svg")
                if len(_tmp_party) > 0:
                    _tmp_party = int(str(_tmp_party[0].get_attribute("class"))[-1])
                    _res["PartyNumber"] = _tmp_party
                else:
                    _res["PartyNumber"] = 0

                # =============================================================>
                # get name and name tag
                _tmp_name = member_status[0].find_elements(By.CSS_SELECTOR, "span.trn-ign__username")
                if len(_tmp_name) > 0:
                    _res["Name"] = str(_tmp_name[0].text)
                else:
                    _res["Name"] = "error"
                
                _tmp_tag = member_status[0].find_elements(By.CSS_SELECTOR, "span.trn-ign__discriminator")
                if len(_tmp_tag) > 0:
                    _res["NameTag"] = str(_tmp_tag[0].text)
                else:
                    _res["NameTag"] = "error"
                
                # =============================================================>
                # get rank
                _tmp_rank = member_status[1].find_elements(By.TAG_NAME, "img")
                if len(_tmp_rank) > 0:
                    _tmp_rank = _tmp_rank[0].get_attribute("title").split(" ")
                    if "Unrated" in _tmp_rank:
                        _res["CurrentRank"] = (_tmp_rank[0], 0)
                    else:
                        _res["CurrentRank"] = (_tmp_rank[0], _tmp_rank[1])
                else:
                    _res["CurrentRank"] = ("error", 0)
                
                # =============================================================>
                # others
                _res["ACS"] = int(member_status[2].text)
                _res["K"], _res["D"], _res["A"] = [int(i.text) for i in member_status[3:6]]
                _res["PM"] = member_status[6].text
                _res["KD"] = float(member_status[7].text)
                _res["ADR"] = float(member_status[8].text)
                _res["HS"] = float(str(member_status[9].text).replace("%", "")) / 100
                _res["FK"], _res["FD"], _res["MK"], _res["Econ"] = [int(i.text) for i in member_status[10:]]

                # =============================================================>
                user_list.append(_res)
        
        _output["user"] = user_list

        # =====================================================================>
        # マップ名 metadata__playlist-map
        # スコア team__value
        # 
        # =====================================================================>
        map_name = match_driver.find_elements(By.CLASS_NAME, "metadata__playlist-map")
        if len(map_name) > 0:
            _output["map"] = str(map_name[0].text)
        else:
            _output["map"] = "error"
        
        # =====================================================================>
        map_score = match_driver.find_elements(By.CSS_SELECTOR, ".metadata__score span.team__value")
        if len(map_score) > 1:
            _output["score"] = (int(map_score[0].text), int(map_score[1].text))
        else:
            _output["score"] = (0, 0)

        del match_driver
        
        return _output
    
    # =========================================================================>
    # Utils
    def get(self, user_name, user_tag, tracker = "matches", tracker_query = {}):
        """_summary_

        Args:
            user_name (str) : valorant user name
            user_tag (str)  : valorant user name such as #(.*?)
            tracker (str, optional): target tracker url. Defaults to "matches".
            tracker_query (dict, optional): query string. Defaults to {}.
        """
        user_url = str(urllib.parse.quote(str(user_name))) + str(urllib.parse.quote(str(user_tag)))
        tracker_query_url = urllib.parse.urlencode(tracker_query)

        target_url = user_url + "/" + str(tracker) + "?" + tracker_query_url
        target_url = VALORANT_TRACKER_WEBSITE + "profile/riot/" + target_url # アップデートで使用不可になったら変更する
        super().get(target_url)
    
    def get_match_url_list(self, user_name, user_tag, n_match = None, mode = "unrated"):
        """_summary_

        Args:
            user_name (str): _description_
            user_tag (str): _description_
            mode (str, optional): match playlist . Defaults to "unrated".
                "unrated"|"competitive"|"spikerush"|"snowball"|"replication"|"deathmatch"
        """
        # アクセス
        self.get(user_name, user_tag, tracker_query = {"playlist" : mode})
        
        # リスト取得
        self.wait_element(2.0, element_by = By.CSS_SELECTOR, target_string = ".match:last-child")
        elements = self.find_elements(By.CLASS_NAME, "match")

        
        if n_match is None:
            n_match = len(elements)
        elif n_match > len(elements):
            n_match = len(elements)
        
        match_url_list = []
        for i in range(n_match):
            a_tag = elements[i].find_elements_by_css_selector("a")
            if len(a_tag) > 0:
                match_url_list.append(a_tag[0].get_attribute("href"))

        return match_url_list
    
    def get_match_result_list(self, user_name, user_tag, n_match = None, mode = "unrated"):
        match_url_list = self.get_match_url_list(user_name, user_tag, n_match = n_match, mode = mode)

        _output = []
        for i in match_url_list:
            _output.append(self.get_match_result(i))

        return _output

# =============================================================================> 

if __name__ == "__main__":
    pass
