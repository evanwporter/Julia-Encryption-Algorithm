# Julia Set Encryption Algorithm

Proof of concept for how the filled julia set can be used to encryt and decrypt images. The following image is an example of the encryption and decryption capabilities of the julia set.

![encrypted-decrypted frog](https://github.com/evanwporter/Julia-Encryption-Algorithm/assets/115374841/4dcf51a7-a7b7-479e-b0c5-6398eb84058a)

To use this library, simply download the [JEA folder](https://github.com/evanwporter/Julia-Encryption-Algorithm/jea). Two functions are inside: `encrypt` and `decrypt`.

### Encrypt 

* Parameters
  * `image_path`: Path to the image that needs to be encrypted
  * `c`: The key (ie: password) used to encrypt the image. This is a complex function of the form `x + iy`.
* Return
  * Saves image to `image_path_encrypted.png`
  * Returns encrypted image as `Pillow.Image`
 
### Decrypt 

* Parameters
  * `image_path`: Path to the image that needs to be decrypted
  * `c`: The key (ie: password) used to decrypt the image. This is a complex function of the form `x + iy`.
* Return
  * Saves image to `image_path_decrypted.png`
  * Returns decrypted image as `Pillow.Image`

## Example

```
import jea
img_path = r"images\frog.jpg"
encrypt(r"images\frog.jpg", 0.5 + 0.75j)
decrypt(r"images\frog_encrypted.png", 0.5 + 0.75j)
```
