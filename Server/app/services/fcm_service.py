import logging
from typing import Optional
import firebase_admin
from firebase_admin import credentials, messaging
from app.config import settings

logger = logging.getLogger(__name__)

_fcm_initialized = False


def initialize_fcm():
    global _fcm_initialized
    if _fcm_initialized:
        return

    try:
        if settings.firebase_service_account_path:
            cred = credentials.Certificate(settings.firebase_service_account_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase Admin SDK initialized")
        else:
            logger.warning("Firebase service account path not set. FCM features will be disabled.")
        _fcm_initialized = True
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}", exc_info=True)
        _fcm_initialized = False


def send_data_request_notification(
    fcm_token: str,
    request_id: str,
    data_types: list[str],
    start_date: str,
    end_date: str
) -> bool:
    """
    FCM을 통해 안드로이드 앱에 데이터 요청 알림 전송
    
    Args:
        fcm_token: 안드로이드 기기의 FCM 토큰
        request_id: 요청 ID
        data_types: 요청할 데이터 타입 목록
        start_date: 시작 날짜 (YYYY-MM-DD)
        end_date: 종료 날짜 (YYYY-MM-DD)
    
    Returns:
        전송 성공 여부
    """
    if not _fcm_initialized:
        logger.error("FCM not initialized. Cannot send notification.")
        return False

    try:
        data_types_str = ",".join(data_types)
        
        message = messaging.Message(
            data={
                "type": "data_request",
                "request_id": request_id,
                "data_types": data_types_str,
                "start_date": start_date,
                "end_date": end_date,
            },
            token=fcm_token,
            android=messaging.AndroidConfig(
                priority="high",
                notification=messaging.AndroidNotification(
                    title="건강 데이터 요청",
                    body=f"{start_date} ~ {end_date} 기간의 데이터를 요청합니다",
                    sound="default"
                )
            )
        )

        response = messaging.send(message)
        logger.info(f"FCM message sent successfully: {response}")
        return True

    except messaging.UnregisteredError:
        logger.warning(f"FCM token is unregistered: {fcm_token}")
        return False
    except Exception as e:
        logger.error(f"Failed to send FCM message: {e}", exc_info=True)
        return False

