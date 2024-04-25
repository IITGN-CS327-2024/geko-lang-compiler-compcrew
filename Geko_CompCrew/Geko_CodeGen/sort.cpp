#include <iostream>

#include <vector>
using namespace std;

extern "C" {
void sort(int arr[100], int len) {
for (int i = 0;
i < len; i++) {
for (int j = 0;
j < len - i - 1; j++) {
	int k = j + 1;
if (arr[j] > arr[k]) {
		int temp = arr[j];
		arr[j] = arr[k];
		arr[k] = temp;
}
}
}
	return 	;
}

}
