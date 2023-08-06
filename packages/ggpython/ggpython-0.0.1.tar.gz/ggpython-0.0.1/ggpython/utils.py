# -*- coding: utf-8 -*-
# =============================================================================>
# ##############################################################################
# ## 
# ## utils.py
# ## 
# ##############################################################################
# =============================================================================>
# imports default

# =============================================================================>
# imports third party

# =============================================================================>
# imports local

# =============================================================================>
# local method

def to_two_byte(s):
    return s.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)})).replace(" ", "　")

# =============================================================================>
# valorant

def valorant_agent_to_discord(s):
    return (":" + s.lower() + ":")


def valorant_rank_to_discord(t):
    return (":" + t[0].lower() + ":") + to_two_byte(str(t[1])) + " "


def convert_valorant_match_to_discord(result_list, min_out = False):
    # 全角文字にする
    _output_all = []

    for match_result in result_list:
        _current_team = 1
        _output = []
        _output.append("")
        
        _output.append(
            to_two_byte(
                "<" + str(match_result["map"])
            ) + "　　" + to_two_byte(
                "{:>2}".format(str(match_result["score"][0])) + " vs " + "{:>2}".format(str(match_result["score"][1])) + ">"
            )
        )
        
        if min_out:
            _header = "　　".join([to_two_byte(i) for i in ["#", "AGENT", " K/D/A  "]])
        else:
            _header = "　　".join([to_two_byte(i) for i in ["#", "AGENT", "ACS", " K/D/A  ", "+/-", "HS", "FK"]])
        
        _output.append(_header)
        _output.append("－" * (len(_header) + 1))
        for user_data in match_result["user"]:
            if not _current_team == user_data["Team"]:
                _current_team = user_data["Team"]
                _output.append("－" * (len(_header) + 1))
            
            _row = []
            _row.append(to_two_byte(str(user_data["TeamRank"])))
            _row.append(valorant_agent_to_discord(user_data["Agents"]) + "　" + valorant_rank_to_discord(user_data["CurrentRank"]))
            if not min_out:
                _row.append(to_two_byte("{:>3}".format(str(user_data["ACS"]))))
            _row.append(to_two_byte("{:>2}/{:>2}/{:<2}".format(user_data["K"], user_data["D"], user_data["A"])))
            if not min_out:
                _row.append(to_two_byte(
                    "{:^3}".format(str(user_data["PM"]))
                ))
                _row.append(to_two_byte(
                    "{:>2}".format(str(int(user_data["HS"] * 100)))
                ))
                _row.append(to_two_byte(
                    "{:>2}".format(str(user_data["FK"]))
                ))
            _row = "　　".join(_row)
            _output.append(_row)
        
        _output.append("－" * (len(_header) + 1))
        _output = "\n".join(_output)
        _output_all.append(_output)
    
    return _output_all


def convert_valorant_match_to_ascii(result_list):
    row_format = "| {} | PT{} | {:<10} | {:<11} | {:　<15}{:>6} | {:>3} | {:>2}/{:>2}/{:<2} {:>3} | {:^3} | {:>5} | {:>2} | {:>2}/{:<2} | {:>2} | {:>4} |"
    _output_all = []

    for match_result in result_list:
        _output = []
        _current_team = 1
        _header = row_format.format(
            "#", " ", "Agents", "Rank", to_two_byte("Username"), "#Tag", "ACS", "K", "D", "A","KD", "+/-", "ADR", "HS", "FK", "FD", "MK", "Econ"
        )
        _hr = "+" + "-" * (3) + "+" + "-" * (5) + "+" + "-" * (12) + "+"  + "-" * (13) + "+" + "-" + "－" * (15) + "-" * (7) + "+"
        _hr += "-" * (5) + "+" + "-" * (14) + "+" + "-" * (5) + "+" + "-" * (7) + "+" + "-" * (4) + "+" + "-" * (7) + "+" + "-" * (4) + "+" + "-" * (6) + "+"
        _output.append(_hr)
        _output.append(_header)
        _output.append(_hr)
        for user_data in match_result["user"]:
            _row = row_format.format(
                user_data["TeamRank"],
                user_data["PartyNumber"], 
                user_data["Agents"], 
                user_data["CurrentRank"][0] + str(user_data["CurrentRank"][1]),
                to_two_byte(user_data["Name"]), user_data["NameTag"],
                user_data["ACS"],
                user_data["K"], user_data["D"], user_data["A"],
                user_data["KD"],
                user_data["PM"], user_data["ADR"],
                str(user_data["HS"] * 100)[:2],
                user_data["FK"], user_data["FD"], user_data["MK"], 
                user_data["Econ"]
            )
            if not _current_team == user_data["Team"]:
                _output.append(_hr)
                _current_team = user_data["Team"]

            _output.append(_row)
        
        _output.append(_hr)
        
        _output_all.append("\n".join(_output))
    
    return _output_all

# =============================================================================>
# main

def convert_to_ascii(result_list):
    return result_list


def convert_to_discord(result_list):
    return "```sh\n{}\n```".format(convert_to_ascii(result_list))

# =============================================================================>
  
if __name__ == "__main__":
    pass
