# pybin
Pybin is an open-source, online pastebin that keeps the server entirely blind to the content you share.

The data is encrypted in your browser with 128-bit AES encryption in CBC mode.

## How it works
Common url: ```V5i0G9acTt1DDFAW3N4P-2aW29gBMhQ6nEct3vz2oSwqjZdOAYwo=```
consists of two parts:
  1) first 9 chars - id of the paste
  2) decryption key

Pybin stores only encrypted paste and corresponding id.
