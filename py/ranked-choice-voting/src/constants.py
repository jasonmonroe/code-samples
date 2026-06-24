# src/constants.py

"""
+--------------------------------------------------------------------------
| CONSTANTS
+--------------------------------------------------------------------------
| Read only variables used throughout project.
"""

ARG_PARAMS = [
    #'--build',     # Build AI Agent
    #'--data',      # Create and confiirm vectorized data
    #'--deploy',    # Deploy code to Huggingface
    #'--log',       # Logs information in the output (terminal)
    #'--log.debug', # Logs additional information
    #'--refresh',   # Forces chroma to create fresh vectorized data
    '--run',       # Starts version of app
    '--start'      # Starts voting
    ]

MAX_CHOICES = 4
DEFAULT_CANDIDATE_COUNT = 4
DEFAULT_VOTER_COUNT = 16

FIRST_CHOICE_INDEX = 0
MAX_CHOICES = 4

MIN_VOTERS = 9 #25
MAX_VOTERS = 15 #168000000

MIN_CANDIDATES = 2
MEDIAN_CANDIDATES = 8
MAX_CANDIDATES = 10 #128

NO_VOTE_VAL = ''
NO_VOTE_PCT_THRESHOLD = 3
CANDIDATE_CONTRIBUTION_MIN = 20.00
CANDIDATE_CONTRIBUTION_MAX = 3500.00
ELECTION_DURATION = 306
PERCENTILE = 100
MSEC = 1000
SECS_IN_MIN = 60 # secs in min

RUN_MIN_ID = 10000
RUN_MAX_ID = 99999
PEP8_LINE_LEN = 79 # PEP8 line length standards
OPEN_CLOSE_LEN = 4
MAX_LINE_LEN = PEP8_LINE_LEN - OPEN_CLOSE_LEN

LOG_FILE = "outputs/log.txt"
RESULTS_FILE = "outputs/results.txt"

BLANK_BALLOT = ['', '', '', '']

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

POLITICAL_PARTIES = [
            'Constitution',
            'Democrat',
            'Green',
            'Libertarian',
            'No-Party Affiliation',
            'Progressive',
            'Reform',
            'Republican'
        ]


# Icons
I_ANGRY = '😠'
I_BOT = '🤖'
I_BOOK = '📚'
I_BROOM = '🧹'
I_CHECKMARK = '✅'
I_CLOCK = '⏰'
I_CONFUSED = '😕'
I_CROSSMARK = '❌'
I_DB = '📊'
I_DIR = '📂'
I_DEAD = '😵'
I_DISK = '💾'
I_DOCUMENT = '📄'
I_EXCLAMATION = '❗'
I_FIRE = '🔥'
I_FLAG = '🚩'
I_FROWN = '😦'
I_GEAR = '⚙️'
I_GHOST = '👻'
I_HANDSHAKE = '🤝🏾'
I_INFO = 'ℹ️'
I_MINUS = '➖'
I_PEN = '🖊️'
I_PLUS = '➕'
I_QUES = '❓'
I_RUNNING = '🏃'
I_SAD = '😢'
I_SKULL = '💀'
I_SLEEPING = '😴'
I_SMILING = '😊'
I_STAR = '⭐'
I_SURPRISED = '😲'
I_TIMER = '⏱'
I_THINKING = '🤔'
I_THUMBS_DOWN = '👎'
I_THUMBS_UP = '👍'
I_WARNING = '⚠️'
I_WATCH = '⌚'
