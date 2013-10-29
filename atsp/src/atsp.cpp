//============================================================================
// Name        : atsp.cpp
// Author      : Pawe³ Rych³y Dawid Wiœniewski
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <time.h>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <cstdio>

int* best;
int* current;
int* candidate;
int** mat;
int length = 0;
int best_result = 0;

using namespace std;


// UTILS
void showArray(int* tab, int length) {
	for(int i=0; i< length; i++) {
		cout << tab[i] << ", ";
	}
	cout << endl;
}

void copy_arrays(int* src, int* dest, int size) {
	for(int i=0; i<size; i++) {
		dest[i] = src[i];
	}
}

void showMat() {
	for (int i =0; i < length; i++) {
		for ( int j = 0; j < length; j++) {
			cout << mat[i][j]<< " ";
		}
		cout << endl;
	}
}

int random_experiment(int* array, int size) {
	permuteTab(array, size);
	return getTotalPathLength(array, size);
}

int** read_data(string filename, int &dimmension) {
	dimmension = -1;
	int** matrix;
	ifstream data;
	string line = "";
	int offset = 0;
	filename = "../data-atsp/" + filename;
	data.open(filename.c_str());

	if (data.is_open()) {
		while (!data.eof() && (dimmension == -1)) {
			getline(data, line);
			if ((offset = line.find("dimmension:", 0)) != string::npos) {
				istringstream iss;
				iss.str(line.substr(offset + 10));
				iss >> dimmension;
				matrix = new int*[dimmension];
				for (int i = 0; i < dimmension; i++) {
					matrix[i] = new int[dimmension];
				}
			}
		}

		bool reading_matrix = false;
		while (!data.eof() && (dimmension > 0) && (!reading_matrix)) {
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
				x = (x+1) % dimmension;
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


void init() {
	srand(time(NULL));
	int l = 0;
	mat = read_data("br17.atsp", l);
	length = l;
	best = new int[length];
	current = new int[length];
	candidate = new int[length];

	for(int i = 0; i < length; i++) {
		current[i] = i;
	}
}

void swap(int i, int j) {
//zapewnic zeby candidate == old
	for (int k=0; k < length; k++) {
		candidate[k] = current[k];
	}
	candidate[i] = current[j];
	candidate[j] = current[i];
}


int evaluateOnPositions(int* tab, int i, int j){
	int prev_j = (j - 1) < 0 ? length-1 : (j-1);
	int prev_i = (i - 1) < 0 ? length-1 : (i-1);
	int evaluation = mat[tab[prev_i]][tab[i]] + mat[tab[i]][tab[(i + 1)%length] ] +
			mat[tab[prev_j]][tab[j]] + mat[tab[j]][tab[(j + 1)%length] ];
	return evaluation;
}


void simple_heuristics() {

}


void steepest_2opt(){
	cout << "iteracja" << endl;
	showArray(current, length);
	int delta = 0;
	int value = 0;
	for (int i = 0; i < length-1; i++ ) {
		for(int j = i+1; j < length; j++) {
			swap(i, j);
			int eval_old = evaluateOnPositions(current, i, j);
			int eval = evaluateOnPositions(candidate, i, j);
			value = eval - eval_old;
			
			if (value < delta) {
				delta = value;
				for(int k=0; k < length; k++) {
					best[k] = candidate[k];
				}
			}
			cout << "eval: " << eval << " eval_old: " << eval_old << " value: " << value << " delta: " << delta << "best_r: " << best_result<< endl;
			showArray(candidate, length);
			//cin.get();
		}
	}
	if (delta < 0) {
		int temp;//current;
		for (int i = 0; i < length; i++) {
			temp = current[i];
			current[i] = best[i];
			best[i] = temp;
		}
		/*current = best;
		best = temp;
		best_result -= delta;*/
		best_result += delta;
		steepest_2opt();
	}

}


// returns total length of path
int getTotalPathLength(int* tab){
	int sum = 0;
	for (int i = 0; i < length; i++) {
		sum += mat[tab[i]][tab[(i+1) % length]];
	}
	return sum;
}

// main function of experiments
double doExperiment(double accuracy) {
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


// makes "in place" random array permutation
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

void localSearch() {
	permuteTab(current, length);
}



int main() {
	double result = doExperiment(1);
	cout << result << " ms"<< endl; // prints !!!Hello World!!!
	
	init();
	mat = new int*[5];
	for (int i= 0; i < 5; i++) {
		mat[i] = new int[5];
		for (int j =0; j < 5; j++) {
			mat[i][j] = i*j;
		}
	}
	length = 5;
	permuteTab(current, length);
	showArray(current, length);
	int distance = getTotalPathLength(current);
	cout << distance;
	for (int i = 0; i < length; i++) {
		for (int j = 0; j < length; j++) {
			cout << mat[j][i] << " ";
		}
		cout << endl;
	}
	best_result = getTotalPathLength(current);
	cout << "distance: " << best_result << endl;
	steepest_2opt();
	showArray(current, length);
	cout << "distance: " << best_result << endl;
	return 0;
}
