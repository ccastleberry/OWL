''' THis file is to define the schema and set up the OWL database'''

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Sequence,
    Float
)
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.ext.declarative import declarative_base

import datetime

Base = declarative_base()


HERO_TYPE_DICT = {'Ana': 'Support',
 'Bastion': 'Defense',
 'D.Va': 'Tank',
 'Doomfist': 'Offense',
 'Genji': 'Offense',
 'Hanzo': 'Defense',
 'Junkrat': 'Defense',
 'Lúcio': 'Support',
 'McCree': 'Offense',
 'Mei': 'Defense',
 'Mercy': 'Support',
 'Moira': 'Support',
 'Orisa': 'Tank',
 'Pharah': 'Offense',
 'Reaper': 'Offense',
 'Reinhardt': 'Tank',
 'Roadhog': 'Tank',
 'Soldier: 76': 'Offense',
 'Sombra': 'Offense',
 'Symmetra': 'Support',
 'Torbjörn': 'Defense',
 'Tracer': 'Offense',
 'Widowmaker': 'Defense',
 'Winston': 'Tank',
 'Zarya': 'Tank',
 'Zenyatta': 'Support'}


MAP_TYPE_DICT = {'Black Forest': 'Arena',
 'Blizzard World': 'Hybrid',
 'Castillo': 'Arena',
 'Château Guillard': 'Deathmatch',
 'Dorado': 'Escort',
 'Ecopoint: Antarctica': 'Arena',
 'Eichenwalde': 'Hybrid',
 'Hanamura': 'Assault',
 'Hollywood': 'Hybrid',
 'Horizon Lunar Colony': 'Assault',
 'Ilios': 'Control',
 'Junkertown': 'Escort',
 "King's Row": 'Hybrid',
 'Lijiang Tower': 'Control',
 'Necropolis': 'Arena',
 'Nepal': 'Control',
 'Numbani': 'Hybrid',
 'Oasis': 'Control',
 'Route 66': 'Escort',
 'Temple of Anubis': 'Assault',
 'Volskaya Industries': 'Assault',
 'Watchpoint: Gibraltar': 'Escort'}

# Table Definitions

class Map(Base):
    __tablename__ = 'map'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    map_type = Column(String)
    
    def __repr__(self):
        return "<Map (Name={}, Type={})>".format(self.name, self.map_type)

class Hero(Base):
    __tablename__ = 'hero'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hero_type = Column(String)
    
    def __repr__(self):
        return "<Map (Name={}, Type={})>".format(self.name, self.map_type)

class Team(Base):
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    abbr = Column(String)
    location = Column(String)
    division = Column(String)

    def __repr__(self):
        return "<Team (name={}, abbr={})>".format(self.name, self.abbr)

class Player(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    tag = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))
    # Relationships
    
    def __repr__(self):
        return "<Player (tag={})>".format(self.tag)

class Match_Results(Base):
    __tablename__ = 'match_results'
    id = Column(Integer, primary_key=True)
    wl_match_id = Column(Integer)
    date = Column(DateTime)
    team_a_id = Column(String, ForeignKey('team.id'))
    team_b_id = Column(String, ForeignKey('team.id'))
    a_score = Column(Integer)
    b_score = Column(Integer)  
    a_fights = Column(Integer)
    b_fights = Column(Integer)
    a_kills = Column(Integer)
    b_kills = Column(Integer)
    winning_team_id = Column(String, ForeignKey('team.id'))
    
    def __repr__(self):
        return "<Match_Results (WinstonsLab ID={})>".format(self.wl_match_id)

class Match_Player_Summary(Base):
    __tablename__ = 'match_player_summary'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match_results.id'))
    wl_match_id = Column(Integer)
    date = Column(DateTime)
    player_id = Column(String, ForeignKey('player.id'))
    team_id = Column(String, ForeignKey('team.id'))

    kills = Column(Integer)
    deaths = Column(Integer)
    kd = Column(Float)
    ults = Column(Integer)
    fk_diff = Column(Integer)
    wl_match_rating = Column(Integer)

    def __repr__(self):
        return "<Match Player Summary (WinstonsLab ID={})>".format(self.wl_match_id)

class Match_Player_Detail(Base):
    __tablename__ = 'match_player_detail'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match_results.id'))
    wl_match_id = Column(Integer)
    date = Column(DateTime)
    player_id = Column(String, ForeignKey('player.id'))
    hero_id = Column(String, ForeignKey('hero.id'))
    team_id = Column(String, ForeignKey('team.id'))

    play_time = Column(DateTime)
    wl_match_hero_rating = Column(Integer)
    fight_win_percent = Column(Float)
    percent_of_teams_kills = Column(Float)
    
    kills = Column(Integer)
    deaths = Column(Integer)
    ults = Column(Integer)
    kills_per_10 = Column(Float)
    deaths_per_10 = Column(Float)
    ults_per_10 = Column(Float)

    time_to_charge_ult = Column(Integer)
    kills_per_ult = Column(Integer)
    ults_efficiency = Column(Float)
    ults_outside_fight = Column(Float)

    first_kills_percent = Column(Float)
    first_deaths_percent = Column(Float)

    impact = Column(Integer)

    def __repr__(self):
        return "<Match Player Detail (WinstonsLab ID={})>".format(self.wl_match_id)

class Round_Results(Base):
    __tablename__ = 'round_results'
    id = Column(Integer, primary_key=True)
    wl_match_id = Column(Integer)
    match_id = Column(Integer, ForeignKey('match_results.id'))
    match_round = Column(Integer)
    map_id = Column(Integer, ForeignKey('map.id'))

    date = Column(DateTime)
    team_a_id = Column(String, ForeignKey('team.id'))
    team_b_id = Column(String, ForeignKey('team.id'))
    a_score = Column(Integer)
    b_score = Column(Integer)  
    a_fights = Column(Integer)
    b_fights = Column(Integer)
    a_kills = Column(Integer)
    b_kills = Column(Integer)
    winning_team_id = Column(String, ForeignKey('team.id'))
    
    def __repr__(self):
        return "<Round Results (WinstonsLab ID={}, Map={})>".format(self.wl_match_id, self.map_id)

class Round_Player_Summary(Base):
    __tablename__ = 'round_player_summary'
    id = Column(Integer, primary_key=True)
    wl_match_id = Column(Integer)
    match_id = Column(Integer, ForeignKey('match_results.id'))

    round_id = Column(Integer, ForeignKey('round_results.id'))
    map_number = Column(Integer)
    map_id = Column(Integer, ForeignKey('map.id'))

    date = Column(DateTime)
    player_id = Column(String, ForeignKey('player.id'))
    team_id = Column(String, ForeignKey('team.id'))

    kills = Column(Integer)
    deaths = Column(Integer)
    kd = Column(Float)
    ults = Column(Integer)
    fk_diff = Column(Integer)
    wl_match_rating = Column(Integer)

    def __repr__(self):
        return "<Round Player Summary (WinstonsLab ID={}, Map={})>".format(self.wl_match_id, self.map_id)

class Round_Player_Detail(Base):
    __tablename__ = 'round_player_detail'
    id = Column(Integer, primary_key=True)
    wl_match_id = Column(Integer)
    match_id = Column(Integer, ForeignKey('match_results.id'))

    round_id = Column(Integer, ForeignKey('round_results.id'))
    map_number = Column(Integer)
    map_id = Column(Integer, ForeignKey('map.id'))

    date = Column(DateTime)
    player_id = Column(String, ForeignKey('player.id'))
    hero_id = Column(String, ForeignKey('hero.id'))
    team_id = Column(String, ForeignKey('team.id'))
    
    play_time = Column(DateTime)
    wl_match_hero_rating = Column(Integer)
    fight_win_percent = Column(Float)
    percent_of_teams_kills = Column(Float)
    
    kills = Column(Integer)
    deaths = Column(Integer)
    ults = Column(Integer)
    kills_per_10 = Column(Float)
    deaths_per_10 = Column(Float)
    ults_per_10 = Column(Float)

    time_to_charge_ult = Column(Integer)
    kills_per_ult = Column(Integer)
    ults_efficiency = Column(Float)
    ults_outside_fight = Column(Float)

    first_kills_percent = Column(Float)
    first_deaths_percent = Column(Float)

    impact = Column(Integer)

    def __repr__(self):
        return "<Round Player Detail (WinstonsLab ID={}, Map={})>".format(self.wl_match_id, self.map_id)


def initialize_db(engine):
    Base.metadata.create_all(engine)

