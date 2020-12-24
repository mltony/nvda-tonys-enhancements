logSpeech = False
if True:
    from speech.priorities import Spri
    import traceback
    originalSpeak = speech.speak
    def speak(
        speechSequence,
        symbolLevel = None,
        priority: Spri = Spri.NORMAL
    ):
        if logSpeech:
            mylog(speechSequence)
            for line in traceback.format_stack():
                mylog("    " + line.strip())
        return originalSpeak(speechSequence, symbolLevel, priority)
    speech.speak = speak
    tones.beep(500, 500)


    @script(description='Log speech stacktrace.', gestures=['kb:NVDA+Delete'])
    def script_log(self, gesture):
        global logSpeech
        logSpeech = not logSpeech
        ui.message(f"logSpeech={logSpeech}")

