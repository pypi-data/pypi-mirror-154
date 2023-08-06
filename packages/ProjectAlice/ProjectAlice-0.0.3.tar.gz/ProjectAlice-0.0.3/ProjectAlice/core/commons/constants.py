#  Copyright (c) 2022
#
#  This file, constants.py, is part of Project Alice.
#
#  Project Alice is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>
#
#  Last modified: 2022.06.08 at 12:56:46 CEST

# System
ALL                                    = 'all'
DATABASE_FILE                          = 'system/database/data.db'
DEFAULT                                = 'default'
DEFAULT_SITE_ID                        = 'default'
DUMMY                                  = 'dummy'
EVERYWHERE                             = 'everywhere'
GITHUB_API_URL                         = 'https://api.github.com/repos/project-alice-assistant'
GITHUB_RAW_URL                         = 'https://raw.githubusercontent.com/project-alice-assistant'
GITHUB_URL                             = 'https://github.com/project-alice-assistant'
JSON_EXT                               = '.json'
PNG_EXT                                = '.png'
RANDOM                                 = 'random'
SKILL_INSTALL_TICKET_PATH              = 'system/skillInstallTickets'
SKILL_REDIRECT_URL                     = 'https://skills.projectalice.ch'
SKILLS_SAMPLES_STORE_ASSETS            = 'https://skills.projectalice.io/assets/store/skills.samples'
SKILLS_STORE_ASSETS                    = 'https://skills.projectalice.io/assets/store/skills.json'
UNKNOWN                                = 'unknown'
UNKNOWN_MANAGER                        = 'unknownManager'
UNKNOWN_USER                           = 'unknownUser'
UNKNOWN_WORD                           = 'unknownword'

### MQTT Topics
## Common Topics
# hermes Topics
TOPIC_ASR_START_LISTENING              = 'hermes/asr/startListening'
TOPIC_ASR_STOP_LISTENING               = 'hermes/asr/stopListening'
TOPIC_ASR_TOGGLE_OFF                   = 'hermes/asr/toggleOff'
TOPIC_ASR_TOGGLE_ON                    = 'hermes/asr/toggleOn'
TOPIC_AUDIO_FRAME                      = 'hermes/audioServer/{}/audioFrame'
TOPIC_CONTINUE_SESSION                 = 'hermes/dialogueManager/continueSession'
TOPIC_DIALOGUE_MANAGER_CONFIGURE       = 'hermes/dialogueManager/configure'
TOPIC_END_SESSION                      = 'hermes/dialogueManager/endSession'
TOPIC_CLEAR_LEDS                       = 'hermes/leds/clear'  # TODO: rename in sat to HLC_CLEAR_LEDS (MqttManager only)
TOPIC_HLC_CLEAR_LEDS                   = 'hermes/leds/clear'
TOPIC_DND_LEDS                         = 'hermes/leds/doNotDisturb'  # TODO: rename in sat to HLC_DND_LEDS (MqttManager only)
TOPIC_HLC_DND_LEDS                     = 'hermes/leds/doNotDisturb'
TOPIC_HOTWORD_DETECTED                 = 'hermes/hotword/default/detected'
TOPIC_HOTWORD_TOGGLE_OFF               = 'hermes/hotword/toggleOff'
TOPIC_HOTWORD_TOGGLE_ON                = 'hermes/hotword/toggleOn'
TOPIC_INTENT_NOT_RECOGNIZED            = 'hermes/dialogueManager/intentNotRecognized'
TOPIC_INTENT_PARSED                    = 'hermes/nlu/intentParsed'
TOPIC_NLU_ERROR                        = 'hermes/error/nlu'
TOPIC_NLU_INTENT_NOT_RECOGNIZED        = 'hermes/nlu/intentNotRecognized'
TOPIC_NLU_QUERY                        = 'hermes/nlu/query'
TOPIC_PARTIAL_TEXT_CAPTURED            = 'hermes/asr/partialTextCaptured'
TOPIC_PLAY_BYTES                       = 'hermes/audioServer/{}/playBytes/#'  # hermes/audioServer/<SITE_ID>/playBytes/<REQUEST_ID>
TOPIC_PLAY_BYTES_FINISHED              = 'hermes/audioServer/{}/playFinished'
TOPIC_SESSION_ENDED                    = 'hermes/dialogueManager/sessionEnded'
TOPIC_SESSION_QUEUED                   = 'hermes/dialogueManager/sessionQueued'
TOPIC_SESSION_STARTED                  = 'hermes/dialogueManager/sessionStarted'
TOPIC_START_SESSION                    = 'hermes/dialogueManager/startSession'
TOPIC_SYSTEM_UPDATE                    = 'hermes/leds/systemUpdate'  # TODO: rename in both to HLC_SYD_UPDATE?
TOPIC_TEXT_CAPTURED                    = 'hermes/asr/textCaptured'
TOPIC_TOGGLE_FEEDBACK                  = 'hermes/feedback/sound/toggle{}'
TOPIC_TOGGLE_FEEDBACK_OFF              = 'hermes/feedback/sound/toggleOff'
TOPIC_TOGGLE_FEEDBACK_ON               = 'hermes/feedback/sound/toggleOn'
TOPIC_TTS_FINISHED                     = 'hermes/tts/sayFinished'
TOPIC_TTS_SAY                          = 'hermes/tts/say'
TOPIC_VAD_DOWN                         = 'hermes/voiceActivity/{}/vadDown'
TOPIC_VAD_UP                           = 'hermes/voiceActivity/{}/vadUp'
TOPIC_WAKEWORD_DETECTED                = 'hermes/hotword/{}/detected'


# Alice Topics
TOPIC_ALICE_GREETING                   = 'projectalice/devices/greeting'
TOPIC_ALICE_CONNECTION_ACCEPTED        = 'projectalice/devices/connectionAccepted'
TOPIC_ALICE_CONNECTION_REFUSED         = 'projectalice/devices/connectionRefused'
TOPIC_CORE_DISCONNECTION               = 'projectalice/devices/coreDisconnection'
TOPIC_CORE_HEARTBEAT                   = 'projectalice/devices/coreHeartbeat'
TOPIC_CORE_RECONNECTION                = 'projectalice/devices/coreReconnection'
TOPIC_DEVICE_ACCEPTED                  = 'projectalice/devices/connectionAccepted'
TOPIC_DEVICE_DELETED                   = 'projectalice/devices/deleted'
TOPIC_DEVICE_HEARTBEAT                 = 'projectalice/devices/heartbeat'
TOPIC_DEVICE_REFUSED                   = 'projectalice/devices/connectionRefused'
TOPIC_DEVICE_STATUS                    = 'projectalice/devices/status'
TOPIC_DEVICE_UPDATED                   = 'projectalice/devices/updated'
TOPIC_DISCONNECTING                    = 'projectalice/devices/disconnection'  # TODO: rename in sat to DEVICE_DISCO.. (NetworkManager)
TOPIC_DND                              = 'projectalice/devices/stopListen'
TOPIC_NEW_HOTWORD                      = 'projectalice/devices/alice/newHotword'
TOPIC_NLU_TRAINING_STATUS              = 'projectalice/nlu/trainingStatus'
TOPIC_RESOURCE_USAGE                   = 'projectalice/devices/resourceUsage'
TOPIC_SKILL_STARTED                    = 'projectalice/skills/started'
TOPIC_SKILL_STOPPED                    = 'projectalice/skills/stopped'
TOPIC_SKILL_DELETED                    = 'projectalice/skills/deleted'
TOPIC_SKILL_INSTALLED                  = 'projectalice/skills/installed'
TOPIC_SKILL_INSTALL_FAILED             = 'projectalice/skills/installFailed'
TOPIC_SKILL_INSTRUCTIONS               = 'projectalice/skills/instructions'
TOPIC_SKILL_UPDATE_CORE_CONFIG_WARNING = 'projectalice/skills/coreConfigUpdateWarning'
TOPIC_SKILL_UPDATED                    = 'projectalice/skills/updated'
TOPIC_SKILL_UPDATING                   = 'projectalice/skills/updating'
TOPIC_SKILL_ACTIVATED                  = 'projectalice/skills/activated'
TOPIC_SKILL_DEACTIVATED                = 'projectalice/skills/deactivated'
TOPIC_STOP_DND                         = 'projectalice/devices/startListen' # TODO: rename DND_STOP?
TOPIC_SYSLOG                           = 'projectalice/logging/syslog'
TOPIC_TOGGLE_DND                       = 'projectalice/devices/toggleListen' # TODO: rename DND_TOGGLE?
TOPIC_UI_NOTIFICATION                  = 'projectalice/notifications/ui/notification'
TOPIC_NLU_TRAINER_READY                = 'projectalice/nlu/trainerReady'
TOPIC_NLU_TRAINER_STOPPED              = 'projectalice/nlu/trainerStopped'
TOPIC_NLU_TRAINER_TRAIN                = 'projectalice/nlu/doTrain'
TOPIC_NLU_TRAINER_REFUSE_FAILED        = 'projectalice/nlu/trainingFailed'
TOPIC_NLU_TRAINER_TRAINING_RESULT      = 'projectalice/nlu/trainingResult/#'
TOPIC_NLU_TRAINER_TRAINING             = 'projectalice/nlu/training'
TOPIC_NLU_TRAINER_TRAINING_STATUS      = 'projectalice/nlu/trainingStatus'

### Events
# Common Event
EVENT_AUDIO_FRAME                      = 'audioFrame'
EVENT_BOOTED                           = 'booted'
EVENT_DND_ON                           = 'dndOn'
EVENT_DND_OFF                          = 'dndOff'
EVENT_FIVE_MINUTE                      = 'fiveMinute'
EVENT_FULL_MINUTE                      = 'fullMinute'
EVENT_FULL_HOUR                        = 'fullHour'
EVENT_HOTWORD                          = 'hotword'
EVENT_HOTWORD_TOGGLE_ON                = 'hotwordToggleOn'
EVENT_HOTWORD_TOGGLE_OFF               = 'hotwordToggleOff'
EVENT_PLAY_BYTES                       = 'playBytes'
EVENT_PLAY_BYTES_FINISHED              = 'playBytesFinished'
EVENT_QUARTER_HOUR                     = 'quarterHour'
EVENT_START_LISTENING                  = 'startListening'
EVENT_STOP_LISTENING                   = 'stopListening'

# Core Event
EVENT_ASR_TOGGLE_OFF                   = 'asrToggleOff'
EVENT_ASR_TOGGLE_ON                    = 'asrToggleOn'
EVENT_BROADCASTING_FOR_NEW_DEVICE      = 'broadcastingForNewDeviceStart'
EVENT_CAPTURED                         = 'captured'
EVENT_CONFIGURE_INTENT                 = 'configureIntent'
EVENT_CONTEXT_SENSITIVE_DELETE         = 'contextSensitiveDelete'
EVENT_CONTEXT_SENSITIVE_EDIT           = 'contextSensitiveEdit'
EVENT_CONTINUE_SESSION                 = 'continueSession'
EVENT_DEVICE_ADDED                     = 'deviceAdded'
EVENT_DEVICE_CONNECTING                = 'deviceConnecting'
EVENT_DEVICE_DISCONNECTED              = 'deviceDisconnected'
EVENT_DEVICE_DISCONNECTING             = 'deviceDisconnecting'
EVENT_DEVICE_DISCOVERED                = 'deviceDiscovered'
EVENT_DEVICE_HEARTBEAT                 = 'deviceHeartbeat'
EVENT_DEVICE_REMOVED                   = 'deviceRemoved'
EVENT_END_SESSION                      = 'endSession'
EVENT_INTENT                           = 'intent'
EVENT_INTENT_NOT_RECOGNIZED            = 'intentNotRecognized'
EVENT_INTENT_PARSED                    = 'intentParsed'
EVENT_INTERNET_CONNECTED               = 'internetConnected'
EVENT_INTERNET_LOST                    = 'internetLost'
EVENT_MESSAGE                          = 'message'
EVENT_NLU_ERROR                        = 'nluError'
EVENT_NLU_INTENT_NOT_RECOGNIZED        = 'nluIntentNotRecognized'
EVENT_NLU_QUERY                        = 'nluQuery'
EVENT_NLU_TRAINED                      = 'nluTrained'
EVENT_PARTIAL_TEXT_CAPTURED            = 'partialTextCaptured'
EVENT_SAY                              = 'say'
EVENT_SAY_FINISHED                     = 'sayFinished'
EVENT_SESSION_ENDED                    = 'sessionEnded'
EVENT_SESSION_ERROR                    = 'sessionError'
EVENT_SESSION_QUEUED                   = 'sessionQueued'
EVENT_SESSION_STARTED                  = 'sessionStarted'
EVENT_SESSION_TIMEOUT                  = 'sessionTimeout'
EVENT_SKILL_DELETED                    = 'skillDeleted'
EVENT_SKILL_INSTALL_FAILED             = 'skillInstallFailed'
EVENT_SKILL_INSTALLED                  = 'skillInstalled'
EVENT_SKILL_STARTED                    = 'skillStarted'
EVENT_SKILL_STOPPED                    = 'skillStopped'
EVENT_SKILL_UPDATED                    = 'skillUpdated'
EVENT_SKILL_DEACTIVATED                = 'skillDeactivated'
EVENT_SKILL_ACTIVATED                  = 'skillActivated'
EVENT_SLEEP                            = 'sleep'
EVENT_STOP_BROADCASTING_FOR_NEW_DEVICE = 'broadcastingForNewDeviceStop'
EVENT_SYSLOG                           = 'sysLog'
EVENT_TOGGLE_FEEDBACK_OFF              = 'toggleFeedbackOff'
EVENT_TOGGLE_FEEDBACK_ON               = 'toggleFeedbackOn'
EVENT_USER_CANCEL                      = 'userCancel'
EVENT_VAD_DOWN                         = 'vadDown'
EVENT_VAD_UP                           = 'vadUp'
EVENT_WAKEUP                           = 'wakeup'
EVENT_WAKEWORD                         = 'wakeword'

# Satellite Event
EVENT_ALICE_CONNECTION_ACCEPTED        = 'aliceConnectionAccepted'
EVENT_ALICE_CONNECTION_REFUSED         = 'aliceConnectionRefused'

