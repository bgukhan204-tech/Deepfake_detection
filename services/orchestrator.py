import os
import io
import time
import cv2
import numpy as np
from PIL import Image

from services.image_analyzer import analyze_image_bytes
from services.video_analyzer import analyze_video_file

class AnalysisOrchestrator:
    """
    APPLICATION LAYER: Analysis Orchestrator
    Determines which pipeline (IMAGE PIPELINE, CAMERA PIPELINE, VIDEO PIPELINE)
    should process the input payload and coordinates preprocessing, detection, fusion, and response formatting.
    """
    def __init__(self):
        pass

    def process_image(self, file_bytes, filename="image.jpg"):
        """IMAGE PIPELINE: Handles single image analysis."""
        return analyze_image_bytes(file_bytes, filename=filename)

    def process_camera_frame(self, frame_bytes, filename="camera_snapshot.jpg"):
        """CAMERA PIPELINE: Handles live webcam snapshot/frame stream analysis."""
        res = analyze_image_bytes(frame_bytes, filename=filename)
        res['pipeline'] = 'CAMERA_PIPELINE'
        return res

    def process_video(self, video_path, filename="video.mp4"):
        """VIDEO PIPELINE: Handles video file extraction, sampling, and temporal analysis."""
        res = analyze_video_file(video_path)
        res['filename'] = filename
        res['pipeline'] = 'VIDEO_PIPELINE'
        return res

    def process_batch(self, files_list):
        """BATCH PIPELINE: Handles batch processing of multiple files."""
        results = []
        for item in files_list:
            fname = item.get('filename', 'media')
            raw = item.get('bytes')
            if not raw:
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in ['.mp4', '.avi', '.mov', '.webm', '.mkv']:
                # Save temporarily for video pipeline
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
                    tmp.write(raw)
                    tmp_path = tmp.name
                try:
                    res = self.process_video(tmp_path, filename=fname)
                    results.append(res)
                finally:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
            else:
                try:
                    res = self.process_image(raw, filename=fname)
                    results.append(res)
                except Exception:
                    pass
        return {
            'success': True,
            'count': len(results),
            'results': results
        }

orchestrator = AnalysisOrchestrator()
