# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
from threading import Lock

from mycroft.configuration import Configuration
from mycroft.metrics import report_timing, Stopwatch
from mycroft.audio.tts import TTSFactory, TTS, RemoteTTSException
from mycroft.util import check_for_signal
from mycroft.util.log import LOG
from mycroft.messagebus.message import Message

bus = None  # Mycroft messagebus connection
tts = None
tts_hash = None
lock = Lock()
fallback_tts = None
fallback_tts_hash = None

_last_stop_signal = 0


def handle_speak(event):
    """Handle "speak" message

    Parse sentences and invoke text to speech service.
    """
    global _last_stop_signal, tts

    # if the message is targeted and audio is not the target don't
    # don't synthesise speech
    event.context = event.context or {}
    if event.context.get('destination') and not \
            ('debug_cli' in event.context['destination'] or
             'audio' in event.context['destination']):
        return

    # Get conversation ID
    if event.context and 'ident' in event.context:
        ident = event.context['ident']
    else:
        ident = 'unknown'

    with lock:
        stopwatch = Stopwatch()
        stopwatch.start()

        utterance = event.data['utterance']
        listen = event.data.get('expect_response', False)
        mute_and_speak(utterance, ident, listen)

        stopwatch.stop()

    report_timing(ident, 'speech', stopwatch,
                  {'utterance': utterance, 'tts': tts.__class__.__name__})


def _maybe_reload_tts():
    global tts, tts_hash, fallback_tts, fallback_tts_hash
    config = Configuration().get("tts", {})

    # update TTS object if configuration has changed
    if not tts_hash or tts_hash != config.get("module", ""):
        if tts:
            tts.shutdown()
        # Create new tts instance
        LOG.info("(re)loading TTS engine")
        tts = TTSFactory.create(config)
        tts.init(bus)
        tts_hash = config.get("module", "")

    # if fallback TTS is the same as main TTS dont load it
    if config.get("module", "") == config.get("fallback_module", ""):
        return

    if not fallback_tts_hash or \
            fallback_tts_hash != config.get("fallback_module", ""):
        if fallback_tts:
            fallback_tts.shutdown()
        # Create new tts instance
        LOG.info("(re)loading fallback TTS engine")
        _get_tts_fallback()
        fallback_tts_hash = config.get("fallback_module", "")


def mute_and_speak(utterance, ident, listen=False):
    """Mute mic and start speaking the utterance using selected tts backend.

    Args:
        utterance:  The sentence to be spoken
        ident:      Ident tying the utterance to the source query
    """
    LOG.info("Speak: " + utterance)
    try:
        tts.execute(utterance, ident, listen)
    except Exception as e:
        LOG.exception("TTS synth failed!")
        if tts_hash != fallback_tts_hash:
            execute_fallback_tts(utterance, ident, listen)


def _get_tts_fallback():
    """Lazily initializes the fallback TTS if needed."""
    global fallback_tts, bus
    if not fallback_tts:
        config = Configuration()
        engine = config.get('tts', {}).get("fallback_module", "mimic")
        cfg = {"tts": {"module": engine,
                       engine: config.get('tts', {}).get(engine, {})}}
        fallback_tts = TTSFactory.create(cfg)
        fallback_tts.validator.validate()
        fallback_tts.init(bus)

    return fallback_tts


def execute_fallback_tts(utterance, ident, listen):
    """Speak utterance using fallback TTS if connection is lost.

    Args:
        utterance (str): sentence to speak
        ident (str): interaction id for metrics
        listen (bool): True if interaction should end with mycroft listening
    """
    try:
        tts = _get_tts_fallback()
        LOG.debug("TTS fallback, utterance : " + str(utterance))
        tts.execute(utterance, ident, listen)
        return
    except Exception as e:
        LOG.exception("TTS FAILURE! utterance : " + str(utterance))


def mimic_fallback_tts(utterance, ident, listen):
    """
    DEPRECATED: use execute_fallback_tts instead
    This method is only kept around for backwards api compat
    """
    LOG.warning("mimic_fallback_tts is deprecated! use execute_fallback_tts instead")
    execute_fallback_tts(utterance, ident=ident, listen=listen)


def handle_stop(event):
    """Handle stop message.

    Shutdown any speech.
    """
    global _last_stop_signal
    if check_for_signal("isSpeaking", -1):
        _last_stop_signal = time.time()
        tts.playback.clear()  # Clear here to get instant stop
        bus.emit(Message("mycroft.stop.handled", {"by": "TTS"}))


def init(messagebus):
    """Start speech related handlers.

    Args:
        messagebus: Connection to the Mycroft messagebus
    """
    global bus

    bus = messagebus
    Configuration.set_config_update_handlers(bus)

    bus.on('mycroft.stop', handle_stop)
    bus.on('mycroft.audio.speech.stop', handle_stop)
    bus.on('speak', handle_speak)

    _maybe_reload_tts()
    Configuration.set_config_watcher(_maybe_reload_tts)


def shutdown():
    """Shutdown the audio service cleanly.

    Stop any playing audio and make sure threads are joined correctly.
    """
    if TTS.playback:
        TTS.playback.shutdown()
        TTS.playback.join()