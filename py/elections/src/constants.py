# src/constants.py

"""
+--------------------------------------------------------------------------
| CONSTANTS
+--------------------------------------------------------------------------
| Read only variables used throughout project.
| Notes:
| U.S. population: 340.1 million
| Eligible to vote: 236.4 million (69.5% of the population)
| Registered to vote: 174.0 million (73.6% of eligible voters)
|  Actually voted: 154.0 million (88.5% of registered voters)
| 
| Another useful way to view turnout:
| 
| 154.0 million voted.
| 82.4 million eligible citizens did not vote (about 34.7% of eligible voters).  
| 
| So the overall “funnel” looks like this:
| 
| 340.1M total people
|    * ↓ 69.5%
| 236.4M eligible voters
|     * ↓ 73.6% registered
| 174.0M registered voters
|     * ↓ 88.5% voted
| 154.0M ballots cast  
+--------------------------------------------------------------------------
"""

VOTING_SYS = [
    "popular",  # Calculates Popular Voting System
    "ranked",   # Calculates Ranked Choice Voting System
    "redist",   # Calculates Redistribution Voting Systemn
    "remaining" # Calculates Last Remaining Voting System
    ]
ARG_PARAMS = [
    "--debug",  # Turns on the debug log
    "--noise",  # Add noise
    "--no_log", # Turns off all logs
    "--weighted", # Calculates weighted voting system
    ]

for sys in VOTING_SYS:
    ARG_PARAMS.append(f"--{sys}")

# --- Generic Constants --- #
PEP8_LINE_LEN = 79 # PEP8 line length standards
OPEN_CLOSE_LEN = 4
MAX_LINE_LEN = PEP8_LINE_LEN - OPEN_CLOSE_LEN
RUN_MIN_ID = 10000
RUN_MAX_ID = 99999
PERCENTILE = 100
MSEC = 1000
SECS_IN_MIN = 60

# --- Elections --- #
ELECTION_DURATION = 365 

# --- Candidates --- #
# Source: https://www.fec.gov/help-candidates-and-committees/candidate-taking-receipts/contribution-limits
CANDIDATE_DONATION_MIN = 20.00
CANDIDATE_DONATION_MAX = 3500.00
CANDIDATE_DEFAULT_COUNT = 4
CANDIDATE_COUNT_MIN = 2
CANDIDATE_COUNT_MAX = 16 # 128
CANDIDATE_DURATION_MAX_OFFSET = 45
CANDIDATE_WEIGHT_PARTY = 40
CANDIDATE_WEIGHT_DURATION = 20
CANDIDATE_WEIGHT_DONATION = 25
CANDIDATE_WEIGHT_BALLOT_PLACEMENT = 10
CANDIDATE_WEIGHT_NAME = 5

# --- Weights --- #
WEIGHT_NOISE = 0.10
WEIGHTED_SYS_DEFAULT = 0.25
WEIGHT_POPULAR = 0.25
WEIGHT_RANKED = 0.4
WEIGHT_REDIST = .15
WEIGHT_REMAINING = .20

# Source: https://ballotpedia.org/List_of_political_parties_in_the_United_States
POLITICAL_PARTIES = [
    "Constitution",
    "Democrat",
    "Green",
    "Libertarian",
    "Non-Party Affiliation",
    "Republican",
    "Socialist of America",
    "Working Families",
    "Forward",
]

# Party Points by political party
PARTY_TOP_TIER = 48
PARTY_MID_TIER = 4
PARTY_BTM_TIER = 2

# --- Voters --- #
# Source: https://www.census.gov/newsroom/press-releases/2025/2024-presidential-election-voting-registration-tables.html
FIRST_CHOICE = 0
MAX_CHOICES = 4

BALLOT_BLANK = ["", "", "", ""] # used to mark votes
BALLOT_FRESH = [0, 0, 0, 0]     # used to tally votes

VOTE_BLANK = None
VOTE_BLANK_PCT_THRESH = 15      # Odds of registered voter not voting
VOTE_BY_LIKELYNESS_ODDS = 12    # The odds of a voter just randomly picking a candidate
VOTE_METHODICAL_ODDS = 50       # Odds that voter will use a methodical choice
VOTE_NOISE_ODDS = 0.1           # Add/subtract 10% from value
VOTER_DEFAULT_COUNT = 16

# Source: https://www.statista.com/statistics/273743/number-of-registered-voters-in-the-united-states/
VOTER_MIN_COUNT = 32  
VOTER_MAX_COUNT = 256 #174000000 

# --- Doners --- #
# https://www.opensecrets.org/elections-overview/donor-demographics
# https://www.opensecrets.org/elections-overview/donor-demographics?cycle=2024&display=A
# Only about 1.3195% of the population gives more than $200.
# 4,411,871 donors
DONOR_COUNT_MIN = 100 * VOTER_MIN_COUNT
DONOR_COUNT_MAX = 1000 * VOTER_MAX_COUNT 

# --- Icons --- #
I_BOT = "🤖"
I_CHECKMARK = "✅"
I_CROSSMARK = "❌"
I_EXCLAMATION = "❗"
I_FLAG = "🚩"
I_HANDSHAKE = "🤝🏾"
I_INFO = "ℹ️"
I_PEN = "🖊️"
I_QUES = "❓"
I_SMILING = "😊"
I_TIMER = "⏱"
I_WARNING = "⚠️"
I_WATCH = "⌚"
I_BALLOT = "🗳️"
I_RIBBON = "🎗️"
I_TROPHY = "🏆"
