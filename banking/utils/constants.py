from django.conf import settings
BANK_REG_NUM = getattr(settings, 'BANK_REG_NUM', None)
IPBR_URL = getattr(settings, 'IPBR_URL', None)

print(BANK_REG_NUM)