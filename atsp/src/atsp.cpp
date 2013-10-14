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
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <cstdio>



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

int** read_data(string filename, int &dimension) {
	dimension = -1;
	int** matrix;
	ifstream data;
	string line = "";
	int offset = 0;
	filename = "../data-atsp/" + filename;
	data.open(filename.c_str());

	if (data.is_open()) {
		while (!data.eof() && (dimension == -1)) {
			getline(data, line);
			if ((offset = line.find("DIMENSION:", 0)) != string::npos) {
				istringstream iss;
				iss.str(line.substr(offset + 10));
				iss >> dimension;
				matrix = new int*[dimension];
				for (int i = 0; i < dimension; i++) {
					matrix[i] = new int[dimension];
				}
			}
		}

		bool reading_matrix = false;
		while (!data.eof() && (dimension > 0) && (!reading_matrix)) {
			getline(data, line);
			if ((offset = line.find("EDGE_WEIGHT_SECTION", 0)) != string::npos) {
				reading_matrix = true;
				break;
			}
		}
		int x = 0;
		int y = 0;
		while (!data.eof() && (reading_matrix)) {
			getline(data, line);
			if ((offset = line.find("EOF", 0)) != string::npos) {
				reading_matrix = false;
				break;
			}
			std::stringstream  linestream(line);
			int value;
			// Read an integer at a time from the line
			while(linestream >> value)
			{
				matrix[x][y] = value;
				x = (x+1) % dimension;
				if (x == 0) {
					y++;
				}
			}
		}

	}

	data.close();
	if (matrix != NULL) {
		return matrix;
	}
	return NULL;
}

void permuteTab(int* tab, int len) {
    int swap_index = 0;
    int tmp;

    for(int i=0; i<len-1; i++) {
        swap_index = i + rand() % (len-i);
        tmp = tab[i];
        tab[i] = tab[swap_index];
        tab[swap_index] = tmp;
    }
}


int main() {
	double result = measure_time(1);
	cout << result << " ms"<< endl; // prints !!!Hello World!!!
	int dimension = 0;
	int** mat = read_data("br17.atsp", dimension);
	for (int i = 0; i < dimension; i++) {
		for (int j = 0; j < dimension; j++) {
			cout << mat[j][i] << " ";
		}
		cout << endl;
	}


	srand(time(NULL));
	int* tab = new int[5];
	for(int i=0; i<5; i++)
		tab[i] = i;

	permuteTab(tab, 5);
	for(int i =0; i<5; i++)
		std::cout << tab[i] << " ";
	return 0;
}
