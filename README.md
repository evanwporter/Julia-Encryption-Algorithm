# Julia Set Encryption Algorithm

Proof of concept for how the filled julia set can be used to encryt and decrypt images. The following image is an example of the encryption and decryption capabilities of the julia set.

![encrypted-decrypted frog](https://github.com/evanwporter/Julia-Encryption-Algorithm/assets/115374841/4dcf51a7-a7b7-479e-b0c5-6398eb84058a)

To use this library, simply download the [JEA folder](https://github.com/evanwporter/Julia-Encryption-Algorithm/tree/main/jea). Two functions are inside: `encrypt` and `decrypt`.

### Encrypt 

* Parameters
  * `image_path`: Path to the image that needs to be encrypted.
  * `c`: The key (ie: password) used to encrypt the image. This is a complex function of the form `x + iy`.
  * `min_coordinate`: minimum x-y coordinate to generate the Julia set with.
  * `max_coordinate`: maximum x-y coordinate to generate the Julia set with.
  * `iterations_count`: max number of iterations to generate the Julia set with.
  * `threshold`: when the orbit of Q exceeds the threshold then its assumed that the orbit has escaped.
* Return
  * Saves image to `image_path_encrypted.png`
 
### Decrypt 

* Parameters
  * `image_path`: Path to the image that needs to be decrypted.
  * `c`: The key (ie: password) used to decrypt the image. This is a complex function of the form `x + iy`.
* Return
  * Saves image to `image_path_decrypted.png`

### Notes on `c`

The beauty of the program is that any real number can be used for values of `x` and `y` since the program automatically scales the magnitude of c to be constrained between 0 and the threshold..
    
## Example

```
import jea
img_path = r"images\frog.jpg"
jea.encrypt(r"images\frog.jpg", 0.5 + 0.75j)
jea.decrypt(r"images\frog_encrypted.png", 0.5 + 0.75j)
```
