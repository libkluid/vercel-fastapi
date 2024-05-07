import shortuuid

def generate_uid() -> str:
    return shortuuid.ShortUUID().random(length=16)
