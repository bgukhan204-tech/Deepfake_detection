import os
import sys
import json
import cv2
import numpy as np

print("[TEST] Running DeepShield AI System Integration Test...")

try:
    # 1. Model Service
    from services.model_service import model_service
    print(f"[OK] ModelService status: {model_service.model_status}")

    # 2. Orchestrator Pipeline
    from services.orchestrator import orchestrator
    dummy_img = np.zeros((300, 300, 3), dtype=np.uint8)
    cv2.rectangle(dummy_img, (50, 50), (250, 250), (255, 200, 150), -1)
    _, img_encoded = cv2.imencode('.jpg', dummy_img)
    img_bytes = img_encoded.tobytes()

    img_res = orchestrator.process_image(img_bytes, "test_image.jpg")
    print(f"[OK] Image Pipeline: Verdict={img_res['verdict']}, Confidence={img_res['confidence']}%")

    cam_res = orchestrator.process_camera_frame(img_bytes, "camera.jpg")
    print(f"[OK] Camera Pipeline: Verdict={cam_res['verdict']}, Pipeline={cam_res['pipeline']}")

    # 3. Report Service (PDF Generation)
    from services.report_service import report_service
    pdf_res = report_service.generate_pdf_report(img_res)
    print(f"[OK] Report Service PDF generated: {pdf_res['pdf_filename']} (SHA-256: {pdf_res['sha256_hash'][:16]}...)")

    cybercrime_res = report_service.generate_cybercrime_report({
        'victim_name': 'Test Complainant',
        'target_platform': 'Web Platform',
        'agency': 'NCRP',
        'description': 'Test complaint report',
        'analysis_id': img_res.get('analysis_id', 'DS-TEST'),
        'filename': 'test_image.jpg'
    })
    print(f"[OK] Cybercrime Report PDF generated: {cybercrime_res['pdf_filename']}")

    # 4. Translation Service
    from services.translation_service import translation_service
    trans_res = translation_service.generate_audio(img_res.get('reason', 'Genuine media'), target_lang='es')
    print(f"[OK] Translation Service: {trans_res['language_name']} -> {trans_res['audio_filename']}")

    # 5. Flask App API endpoints test client
    from app_web import app
    client = app.test_client()

    r_health = client.get('/health')
    assert r_health.status_code == 200, "Health endpoint failed"
    print("[OK] API /health endpoint passed!")

    r_history = client.get('/history')
    assert r_history.status_code == 200, "History endpoint failed"
    print("[OK] API /history endpoint passed!")

    r_report = client.post('/report', json={'filename': 'test.jpg', 'verdict': 'MANIPULATED'})
    assert r_report.status_code == 200, "Report endpoint failed"
    print("[OK] API /report endpoint passed!")

    r_translate = client.post('/translate', json={'text': 'Genuine image', 'target_lang': 'fr'})
    assert r_translate.status_code == 200, "Translate endpoint failed"
    print("[OK] API /translate endpoint passed!")

    print("\n========================================================")
    print("ALL DEEPSHIELD AI SYSTEM TESTS PASSED SUCCESSFULLY!")
    print("========================================================")

except Exception as e:
    print(f"[FAIL] Test error: {e}")
    import traceback
    traceback.print_exc()
