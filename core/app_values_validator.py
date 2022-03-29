from core.app_config import AppConfig


def validate_values():
    assert AppConfig.MIN_PLATFORM_WIDTH >= AppConfig.PLATFORM_PART_WIDTH * 3, "PLATFORM NEEDS TO BE AT LEAST THREE TIME AS BIG AS PLATFORM PART"
    assert AppConfig.MAX_PLATFORM_WIDTH >= AppConfig.MIN_PLATFORM_WIDTH, "MAX PLATFORM WIDTH NEEDS TO BE AT LEAST AS BIG AS MIN PLATFORM WIDTH"
    assert AppConfig.MAX_PLATFORM_WIDTH <= AppConfig.SCREEN_WIDTH, "PLATFORM NEEDS TO BE SHORTER OR EQUAL THAN SCREEN WIDTH"