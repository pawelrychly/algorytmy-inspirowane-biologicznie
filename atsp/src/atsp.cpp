//============================================================================
// Name        : atsp.cpp
// Author      : Pawe³ Rych³y Dawid Wiœniewski
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
using namespace std;
#include <time.h>


double measure_time(double accuracy) {
	double prec = 1;
	clock_t start, measure;
	start = clock(); // bie¿¹cy czas systemowy w ms
	int i = 0;
	do {
		//example function


		measure = clock() - start;
		i++;
	} while((measure < prec/accuracy) || (i <= 10));
	long m =(long)(measure);
	double result = (double) m / i;
	return result;
}

int main() {
	double result = measure_time(1);
	cout << endl;
	cout << "Wynik: ";
	cout << result << " ms"<< endl; // prints !!!Hello World!!!
	return 0;
}
