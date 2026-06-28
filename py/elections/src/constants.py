# src/constants.py

"""
+--------------------------------------------------------------------------
| CONSTANTS
+--------------------------------------------------------------------------
| Read only variables used throughout project.
+--------------------------------------------------------------------------
"""

ARG_PARAMS = [
    "--noise",
    "--popular",
    "--rank",
    "--redist",
    "--remaining",
    "--weighted",
    ]

# --- Generic Constants --- #
PEP8_LINE_LEN = 79 # PEP8 line length standards
OPEN_CLOSE_LEN = 4
MAX_LINE_LEN = PEP8_LINE_LEN - OPEN_CLOSE_LEN
RUN_MIN_ID = 10000
RUN_MAX_ID = 99999
PERCENTILE = 100
MSEC = 1000
SECS_IN_MIN = 60 # secs in min

# --- Elections --- #
ELECTION_DURATION = 365 

# --- Candidates --- #
# Source: https://www.fec.gov/help-candidates-and-committees/candidate-taking-receipts/contribution-limits
CANDIDATE_DONATION_MIN = 20.00
CANDIDATE_DONATION_MAX = 3500.00
CANDIDATE_DEFAULT_COUNT = 4
 
CANDIDATE_COUNT_MIN = 2
CANDIDATE_COUNT_MAX = 10 #128

CANDIDATE_DURATION_MAX_OFFSET = 45

CANDIDATE_NAME_POOL = {
    'first': [
        'Alexander',
        'Aïsha',
        'Amelia',
        'Anaïs',
        'Aries',
        'Ava',
        'Benjamin',
        'Charlotte',
        'Chloë',
        'Dmitri',
        'Elijah',
        'Elizabeth',
        'Emma',
        'Ella',
        'Fatima',
        'Harper',
        'Henry',
        'Isabella',
        'James',
        'Jürgen',
        'León',
        'Lars',
        'Liam',
        'Lucas',
        'Matthew',
        'Michael',
        'Mia',
        'Ming',
        'Noah',
        'Oliver',
        'Olga',
        'Omar',
        'Samuel',
        'Scarlett',
        'Sophia',
        'Sofia',
        'Thaddeus',
        'William',
        'Yuki',
        'Zhang'
    ],
    'last': [
        'Abdullah',
        'Anderson',
        'Ben-Ali',
        'Brown',
        'Clark',
        'Davis',
        'Dupont',
        'Dubois',
        'Fernández',
        'Garcia',
        'García',
        'Gonzalez',
        'Harris',
        'Hussein',
        'Hernandez',
        'Johnson',
        'Johansson',
        'Jackson',
        'King',
        'Lee',
        'Lewis',
        'Lopez',
        'Martin',
        'Martinez',
        'Miller',
        'Moore',
        'Ramírez',
        'Ramirez',
        'Rodriguez',
        'Schmidt',
        'Sanchez',
        'Sharma',
        'Silva',
        'Smith',
        'Taylor',
        'Thomas',
        'Thompson',
        'Takahashi',
        'Ivanov',
        'Walker',
        'Wilson',
        'Wright',
        'Young',
        'Zhang',
        'Zimmerman'
    ]
}

# Source: https://ballotpedia.org/List_of_political_parties_in_the_United_States
POLITICAL_PARTIES = [
    'Constitution',
    'Democrat',
    'Green',
    'Libertarian',
    'Non-Party Affiliation',
    'Republican'
    'Socialist of America',
    'Working Families',
    'Forward',
]

PARTY_TOP_TIER = 48
PARTY_MID_TIER = 4
PARTY_BTM_TIER = 2

# --- Voters --- #

"""
* U.S. population: 340.1 million
* Eligible to vote: 236.4 million (69.5% of the population)
* Registered to vote: 174.0 million (73.6% of eligible voters)
* Actually voted: 154.0 million (88.5% of registered voters)

Another useful way to view turnout:

* 154.0 million voted.
* 82.4 million eligible citizens did not vote (about 34.7% of eligible voters).  

So the overall “funnel” looks like this:

* 340.1M total people
    * ↓ 69.5%
* 236.4M eligible voters
    * ↓ 73.6% registered
* 174.0M registered voters
    * ↓ 88.5% voted
* 154.0M ballots cast  
"""

# Voter Turnout
# Source: https://www.census.gov/newsroom/press-releases/2025/2024-presidential-election-voting-registration-tables.html
POPULATION = 0       # US Population
VOTER_ELEGIBLE = 0   # 18 years or older and citizen
VOTER_REGISTERED = 0 # Eligible voter that has actually registered
VOTER_VOTED = 0      # Registered voter than participated 63.7%.

FIRST_CHOICE = 0
MAX_CHOICES = 4

DEFAULT_VOTER_COUNT = 16
BALLOT_BLANK = ['', '', '', ''] # used to mark votes
BALLOT_FRESH = [0, 0, 0, 0] # used to tally votes
VOTE_BLANK = None
VOTE_BLANK_PCT_THRESH = 15 # Odds of registered voter not voting
NO_CHOICE_PCT_THRESHOLD = 10 # Odds of a voter not picking a candidate

VOTE_BY_LIKELYNESS_ODDS = 12 # The odds of a voter just randomly picking a candidate.

VOTE_NOISE_ODDS = 0.1 # Add/subtract 10% from value
VOTE_METHODICAL_ODDS = 50
 
# Source: https://www.statista.com/statistics/273743/number-of-registered-voters-in-the-united-states/
VOTER_MIN_COUNT = 8 #25
VOTER_MAX_COUNT = 16 #168000000 

# 49.8% of popular vote Rep
# 48.3% of popular vote Dem

# Dems: 45.1 million registered voters.
# Reps: 35.7 million registered voters.

# --- Doners --- #
# https://www.opensecrets.org/elections-overview/donor-demographics
# https://www.opensecrets.org/elections-overview/donor-demographics?cycle=2024&display=A
# Only about 1.3195% of the population gives more than $200.
# 4,411,871 donors

DONOR_COUNT_MIN = 100
DONOR_COUNT_MAX = 1000  

# --- Icons --- #
I_BOT = '🤖'
I_CHECKMARK = '✅'
I_CLOCK = '⏰'
I_CROSSMARK = '❌'
I_DEAD = '😵'
I_EXCLAMATION = '❗'
I_FLAG = '🚩'
I_FROWN = '😦'
I_HANDSHAKE = '🤝🏾'
I_INFO = 'ℹ️'
I_MINUS = '➖'
I_PEN = '🖊️'
I_PLUS = '➕'
I_QUES = '❓'
I_SKULL = '💀'
I_SLEEPING = '😴'
I_SMILING = '😊'
I_STAR = '⭐'
I_TIMER = '⏱'
I_WARNING = '⚠️'
I_WATCH = '⌚'
I_BALLOT = '🗳️'
I_RIBBON = '🎗️'
I_TROPHY = '🏆'
 
I_REP = '🐘'
I_DEM = '🫏'
I_LIB = ''
I_PROG = ''
I_GREEN = '💚'
