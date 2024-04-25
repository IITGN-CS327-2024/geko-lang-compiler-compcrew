#include <iostream>

#include <vector>
using namespace std;

extern "C" {
void caesarEncrypt(int plaintext[7], int len, int key) {
for (int i = 0;
i < len; i++) {
	int pre = plaintext[i] + key;
	plaintext[i] = pre % 26;
}
	return 	;
}

void caesarDecrypt(int ciphertext[7], int len, int key) {
for (int i = 0;
i < len; i++) {
	ciphertext[i] = ciphertext[i] - key + 26 % 26;
}
	return 	;
}

}
