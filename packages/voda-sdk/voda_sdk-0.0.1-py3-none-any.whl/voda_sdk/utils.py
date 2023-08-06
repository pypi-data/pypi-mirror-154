

def sanitize_isoformat(isoformat: str) -> str:
    """
    datetime.fromisoformat 메소드가 파싱 가능한 형태로 가공

    C# 기본 라이브러리의 ISO 8601 날짜시간 문자열 생성 함수인
    DateTime.UtcNow.ToString("o") 의 형식이 Python 기본 라이브러리의 파서가
    지원하는 형식 `YYYY-MM-DD[*HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]]` 과 달라
    이를 보정하기 위한 전처리 함수
    """
    sanitized = isoformat
    if sanitized[-1] == 'Z':
        sanitized = sanitized.replace('Z', '+00:00')
    start = sanitized.rfind('.')
    end = sanitized.rfind('+')
    if start != -1 and end != -1 and end - start - 1 == 7:
        sanitized = sanitized[:end-1] + sanitized[end:]
    return sanitized
