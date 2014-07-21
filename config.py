# Welcome to Will's settings.
# 
# All of the settings here can also be specified in the environment, and should be for
# keys and the like.  In case of conflict, you will see a warning message, and the 
# value in this file will win.


# ------------------------------------------------------------------------------------
# Required
# ------------------------------------------------------------------------------------



# The list of plugin modules will should load. 
# Will recursively loads all plugins contained in each module.


# This list can contain:
# 
# Built-in core plugins:
# ----------------------
# All built-in modules:     will.plugins
# Built-in modules:         will.plugins.module_name
# Specific plugins:         will.plugins.module_name.plugin
#
# Plugins in your will:
# ----------------------
# All modules:              plugins
# A specific module:        plugins.module_name
# Specific plugins:         plugins.module_name.plugin
# 
# Plugins anywhere else on your PYTHONPATH:
# -----------------------------------------
# All modules:              someapp
# A specific module:        someapp.module_name
# Specific plugins:         someapp.module_name.plugin


# By default, the list below includes all the core will plugins and
# all your project's plugins.  

PLUGINS = [
    # Built-ins
    "will.plugins.admin",
    "will.plugins.chat_room",
    "will.plugins.devops",
    "will.plugins.friendly",
    "will.plugins.help",
    "will.plugins.productivity",
    "will.plugins.web",

    # All plugins in your project.
    "plugins",
]

# Don't load any of the plugins in this list.  Same options as above.
PLUGIN_BLACKLIST = [

]


# ------------------------------------------------------------------------------------
# Potentially Required
# ------------------------------------------------------------------------------------

# If will isn't accessible at localhost, you must set this for his keepalive to work.
# Note no trailing slash.
PUBLIC_URL = "http://will.greenkahuna.com"

# Port to bind the web server to (defaults to $PORT, then 80.)
# Set > 1024 to run without elevated permission.
# HTTPSERVER_PORT = "9000"


# ------------------------------------------------------------------------------------
# Optional
# ------------------------------------------------------------------------------------

# The list of rooms will should join.  Default is all rooms.
ROOMS = ['GreenKahuna', 'Development', 'Fun!']

# The room will will talk to if the trigger is a webhook and he isn't told a specific room. 
# Default is the first of ROOMS.
DEFAULT_ROOM = 'Development'


# Fully-qualified folders to look for templates in, beyond the two that 
# are always included: core will's templates folder, and your project's templates folder.
# 
# TEMPLATE_DIRS = [
#   os.path.abspath("other_folder/templates")
# ]

# User handles who are allowed to perform `admin_only` plugins.  Defaults to everyone.
ADMINS = [
    "steven",
    "levi",
]

# Mailgun config, if you'd like will to send emails.

# DEFAULT_FROM_EMAIL="will@example.com"
# Set in your environment:
# export WILL_MAILGUN_API_KEY="key-12398912329381"
# export WILL_MAILGUN_API_URL="example.com"


# Logging level
# LOGLEVEL = "DEBUG"

# ------------------------------------------------------------------------------------
# GK settings
# ------------------------------------------------------------------------------------

# Deploy
DEPLOY_PREFIX = "gk-"
GITHUB_ORGANIZATION_NAME = "greenkahuna"

# Urls
GOLD_STAR_URL = "https://gk-will.s3.amazonaws.com/Gold-Star.jpg"
MAINTENANCE_PAGE_URL = "https://gk-maintenance.s3.amazonaws.com/maintenance.html"
HANGOUT_URL = "https://plus.google.com/hangouts/_/event/ceggfjm3q3jn8ktan7k861hal9o?authuser=0&hl=en&hcb=0&lm1=1380301029308&hs=26&ssc=WyIiLDAsbnVsbCxudWxsLG51bGwsW10sbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLDI2LG51bGwsbnVsbCxudWxsLFsxMzgwMzAxMDI5MzA4XSxudWxsLFsiZXZlbnQiLCJjZWdnZmptM3Ezam44a3RhbjdrODYxaGFsOW8iXSxbXSxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxudWxsLG51bGwsbnVsbCxbXSxbXSxudWxsLG51bGwsbnVsbCxbXSxudWxsLG51bGwsbnVsbCxbXV0."
ZOOM_URL = "https://www.zoom.us/j/4502033094"
