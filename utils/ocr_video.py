from filter_optical_character_recognition.filter import FilterOpticalCharacterRecognition
from openfilter.filter_runtime.filters.video_in import VideoIn
from openfilter.filter_runtime.filters.webvis import Webvis
from openfilter.filter_runtime.filter import Filter

if __name__ == '__main__':
    Filter.run_multi([
        (VideoIn, dict(
            sources='file://utils/hello.mov!no-loop',
            outputs='tcp://*:5550',
            outputs_metrics='tcp://*:6550',    
            log=True,        
        )),
        (FilterOpticalCharacterRecognition, dict(
            sources='tcp://localhost:5550',
            outputs='tcp://*:5552',
            ocr_engine='easyocr',
            forward_ocr_texts=True,
        )),
        (Webvis, dict(
            sources='tcp://localhost:5552',
        )),
    ])