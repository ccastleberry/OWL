# This file contains python strings of the queries to create the overwatch db.


CREATE_HERO_TABLE = """
    CREATE TABLE Hero (
        `id` INT     NOT NULL UNIQUE AUTO_INCREMENT,
        `Hero_Name` VARCHAR(60) NOT NULL UNIQUE,
        `Hero_Category` VARCHAR(60),
        PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""

CREATE_MAP_TABLE = """
    CREATE TABLE Map (
        `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
        `Map_Name` VARCHAR NOT NULL UNIQUE,
        `Map_Category` VARCHAR,
        PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""


CREATE_TEAM_TABLE = """
    CREATE TABLE `Team` (
      `Team_ID` INT NOT NULL UNIQUE AUTO_INCREMENT,
      `Team_Name` VARCHAR(60) NOT NULL UNIQUE,
      `Team_Abbr` VARCHAR(10) UNIQUE,
      `Location` VARCHAR(60),
      `Division` VARCHAR(60),
      PRIMARY KEY (`Team_ID`)
    ) DEFAULT CHARSET=utf8;
"""

CREATE_PLAYER_TABLE = """
    CREATE TABLE `Player` (
      `Player_ID` INT NOT NULL UNIQUE AUTO_INCREMENT,
      `Tag` VARCHAR(60) UNIQUE,
      `First_Name` VARCHAR(60),
      `Last_Name` VARCHAR(60),
      `Team_ID` INT,
      `Team_Name` VARCHAR(60),
      `Team_Abbr` VARCHAR(10),
      `Country` VARCHAR(60),
      `Hometown` VARCHAR(60),
      PRIMARY KEY (`Player_ID`)
    ) DEFAULT CHARSET=utf8;
"""

CREATE_MATCH_RESULTS_TABLE = """
    CREATE TABLE `Match_Results` (
      `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
      `WL_Match_ID` INT UNIQUE NOT NULL,
      `Date` VARCHAR(60),
      `Match_Time` VARCHAR,

      `Team_A_ID` INT,
      `Team_A_Name` VARCHAR(60),
      `Team_B_ID` INT,
      `Team_B_Name` VARCHAR(60),

      `A_Score` INT,
      `B_Score` INT,
      `A_Fights` INT,
      `B_Fights` INT,
      `A_Kills` INT,
      `B_Kills` INT,

      `Winning_Team_ID` INT,
      `Winning_Team_Name` VARCHAR(60),

       PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""

CREATE_MATCH_PLAYER_SUMMARY_TABLE = """
    CREATE TABLE `Match_Player_Summary` (
        `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
        `Match_ID` INT NOT NULL,
        `WL_Match_ID` INT UNIQUE NOT NULL,
        `Date` VARCHAR(60),
        `Player_ID` INT,
        `Player_Tag` VALUES(60),
        `Team_ID` INT,
        `Team_Name` VARCHAR(60)

        `Kills` INT,
        `Deaths` INT,
        `KD` INT,
        `Ults` INT,
        `First_Kill_Differential` INT,
        `WL_Rating` INT,

        PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""

CREATE_MATCH_PLAYER_DETAIL_TABLE = """
    CREATE TABLE `Match_Player_Detail` (
        `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
        `Match_ID` INT NOT NULL,
        `WL_Match_ID` INT,
        `Date` VARCHAR(60),
        `Player_ID` INT NOT NULL,
        `Player_Tag` VARCHAR(60)
        `Hero_ID` INT NOT NULL,
        `Hero Name` VARCHAR(60) NOT NULL,
        `Team_ID` INT NOT NULL,
        `Team_Name` VARCHAR(60) NOT NULL,

        `Play_Time` VARCHAR(60),
        `WL_Match_Hero_Rating` INT,
        `Fight_Win_Percentage` FLOAT,
        `Percentage_Team_Kills` FLOAT,

        `Kills` INT,
        `Deaths` INT,
        `Ults` INT,
        `Kills_Per_10` FLOAT,
        `Deaths_Per_10` FLOAT,
        `Ults_Per_10` FLOAT,

        `Time_To_Charge_Ult` INT,
        `Kills_Per_Ult` INT,
        `Ult_Efficiency` FLOAT,
        `Ults_Outside_Fight` FLOAT,
        `First_Kill_Percentage` FLOAT,
        `First_Death_Percentage` FLOAT,

        `WL_Impact` INT,

        PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""

CREATE_ROUND_RESULTS_TABLE = """
    CREATE TABLE `Round_Results` (
      `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
      `WL_Match_ID` INT NOT NULL,
      `Match_ID` INT NOT NULL,
      `Match_Round` INT NOT NULL,
      `Map_ID` INT NOT NULL,
      `Map_Name` VARCHAR(60) NOT NULL,
      `Map_Type` VARCHAR(60),
      `Date` VARCHAR(60),
      `Round_Time` VARCHAR,

      `Team_A_ID` INT,
      `Team_A_Name` VARCHAR(60),
      `Team_B_ID` INT,
      `Team_B_Name` VARCHAR(60),

      `A_Score` INT,
      `B_Score` INT,
      `A_Fights` INT,
      `B_Fights` INT,
      `A_Kills` INT,
      `B_Kills` INT,

      `Winning_Team_ID` INT,
      `Winning_Team_Name` VARCHAR(60),

      PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""


CREATE_ROUND_PLAYER_SUMMARY_TABLE = """
    CREATE TABLE `Round_Player_Summary` (
        `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
        `Match_ID` INT NOT NULL,
        `WL_Match_ID` INT UNIQUE NOT NULL,
        `Match_Round` INT,
        `Round_ID` INT,
        `Map_ID` INT NOT NULL,
        `Map_Name` VARCHAR(60) NOT NULL,
        `Map_Type` VARCHAR(60),
        `Date` VARCHAR(60),
        `Player_ID` INT,
        `Player_Tag` VALUES(60),
        `Team_ID` INT,
        `Team_Name` VARCHAR(60)

        `Kills` INT,
        `Deaths` INT,
        `KD` INT,
        `Ults` INT,
        `First_Kill_Differential` INT,
        `WL_Rating` INT,

        PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""


CREATE_ROUND_PLAYER_DETAIL_TABLE = """
    CREATE TABLE `Round_Player_Detail` (
        `id` INT NOT NULL UNIQUE AUTO_INCREMENT,
        `Match_ID` INT NOT NULL,
        `WL_Match_ID` INT,
        `Match_Round` INT,
        `Round_ID` INT,
        `Map_ID` INT NOT NULL,
        `Map_Name` VARCHAR(60) NOT NULL,
        `Map_Type` VARCHAR(60),D
        `Date` VARCHAR(60),
        `Player_ID` INT NOT NULL,
        `Player_Tag` VARCHAR(60)
        `Hero_ID` INT NOT NULL,
        `Hero Name` VARCHAR(60) NOT NULL,
        `Team_ID` INT NOT NULL,
        `Team_Name` VARCHAR(60) NOT NULL,

        `Play_Time` VARCHAR(60),
        `WL_Match_Hero_Rating` INT,
        `Fight_Win_Percentage` FLOAT,
        `Percentage_Team_Kills` FLOAT,

        `Kills` INT,
        `Deaths` INT,
        `Ults` INT,
        `Kills_Per_10` FLOAT,
        `Deaths_Per_10` FLOAT,
        `Ults_Per_10` FLOAT,

        `Time_To_Charge_Ult` INT,
        `Kills_Per_Ult` INT,
        `Ult_Efficiency` FLOAT,
        `Ults_Outside_Fight` FLOAT,
        `First_Kill_Percentage` FLOAT, #Percentage of fights
        `First_Death_Percentage` FLOAT,

        `WL_Impact` INT,

        PRIMARY KEY (`id`)
    ) DEFAULT CHARSET=utf8;
"""