### Different Libraries Considered

1. SpeechRecognition
2. DeepSpeech 2
3. PySpeechToText
4. Hugging Face Transformers
5. Vosk
6. Kaldi

### Comparision

| Library | Accuracy | Speed | Memory footprint | Ease of use | Offline support |
|---|---|---|---|---|---|
| SpeechRecognition | High | Medium | High | Medium | Yes, with Google Cloud Speech-to-Text Offline API |
| Kaldi | Very high | Medium | High | Difficult | Yes |
| DeepSpeech 2 | Very high | Medium | High | Difficult | Yes |
| Hugging Face Transformers | High | Medium | High | Medium | Yes |
| Vosk | High | Fast | Low | Easy | Yes |


### Best Options

1. **Speech Recognition**
    - Highly accurate
    - Provides support for ***Google Cloud speech, Wit.ai, Microsoft Azure speech, IBM speech to text, Tensorflow, Vosk, etc.***
    - Works in both **online** and **offline** mode

2. **Vosk**
    - ***Light weight***
    - Faster with smaller memory footprint
    - provides offline support

### References
- https://pypi.org/project/SpeechRecognition/
- https://pypi.org/project/vosk/
- https://realpython.com/python-speech-recognition/
- https://www.simplilearn.com/tutorials/python-tutorial/speech-recognition-in-python