import base64
import codecs
import random
anahtarlar = ["rot13","utf-8","utf_32","utf_32_be","utf_32_le","utf_16","utf_16_be","utf_16_le","utf_7","utf_8_sig"]
key = random.choice(anahtarlar)
sifreli_veri = base64.b64encode(b"metin")
sifreli_veri = codecs.encode(str(sifreli_veri),key)
print(sifreli_veri)
#şifreleme kullanılmamıştır