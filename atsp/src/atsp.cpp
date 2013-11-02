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
#include <vector>
#include <cmath>
#include <cstring>

int* best;
int* current;
int* candidate;
int** mat;
int length = 0;
int best_result = 0;
float time_of_walker = 1;
int number_of_steps = 0;

using namespace std;
typedef void( * algorytmT )();


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

int** read_data(string filename, int &dimension) {
	dimension = -1;
	int** matrix;
	ifstream data;
	string line = "";
	int offset = 0;
	//filename = "../data-atsp/" + filename;
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


void init(char* path) {
	srand(time(NULL));
	number_of_steps = 0;
	int l = 0;
	mat = read_data(path, l);
	length = l;
	best = new int[length];
	current = new int[length];
	candidate = new int[length];

	for(int i = 0; i < length; i++) {
		current[i] = i;
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

void reset() {

	for(int i = 0; i < length; i++) {
		best[i] = i;
		current[i] = i;
		candidate[i] = 0;
	}
	permuteTab(current, length);
	number_of_steps = 0;
	best_result = getTotalPathLength(current);
}

void swap(int i, int j) {
//zapewnic zeby candidate == old
	number_of_steps++;
	for (int k=0; k < length; k++) {
		candidate[k] = current[k];
	}
	candidate[i] = current[j];
	candidate[j] = current[i];
}


int evaluateOnPositions(int* tab, int i, int j){
	int prev_j = (j - 1) < 0 ? length-1 : (j-1);
	int prev_i = (i - 1) < 0 ? length-1 : (i-1);
	int next_j = (j + 1) % length;
	int next_i = (i + 1) % length;

	int evaluation = mat[tab[prev_i]][tab[i]] + mat[tab[i]][tab[next_i] ] +
			mat[tab[prev_j]][tab[j]] + mat[tab[j]][tab[next_j] ];

	if (i == next_j) {
		evaluation = evaluation - mat[tab[j]][tab[i]];
	} else if(j == next_i){
		evaluation = evaluation - mat[tab[i]][tab[j]];
	}

	return evaluation;
}





void greedy_2opt() {
	//showArray(current, length);
	int delta = 0;
	int value = 0;
	bool better_result = false;
	int start_index = rand() % (length-1);
	int i = start_index;
	do {
		//cout << "i: " << i << ", " << endl;
		int j = i+1;
		while ((j < length) && (!better_result)) {
			swap(i, j);
			int eval_old = evaluateOnPositions(current, i, j);
			int eval = evaluateOnPositions(candidate, i, j);
			value = eval - eval_old;
			if (value < delta) {
				//cout << "!!!" << value << " " << delta << endl;
				delta = value;
				for(int k=0; k < length; k++) {
					best[k] = candidate[k];
				}
				better_result = true;
			}
			j++;
		}
		i = (i + 1) % (length-1);
	} while((i != start_index) && (!better_result));

	if (delta < 0) {
		int temp;//current;
		for (int i = 0; i < length; i++) {
			temp = current[i];
			current[i] = best[i];
			best[i] = temp;
		}
		best_result += delta;
		//showArray(current, length);
		greedy_2opt();
	}

}


void random_walker_2opt() {
	for(int k=0; k < length; k++) {
		best[k] = current[k];
	}
	int result = best_result;
	//cout << "best result" << result << endl;
	int value = 0;
	clock_t start;
	double measure = 0.0;
	start = clock();

	do {
		int i = rand() % (length);
		int j = i;
		do {
			j = rand() % (length);
		} while(j == i);

		swap(i, j);
		int eval_old = evaluateOnPositions(current, i, j);
		int eval = evaluateOnPositions(candidate, i, j);
		value = eval - eval_old;
		result += value;
		if (result < best_result) {
			for(int k=0; k < length; k++) {
				best[k] = candidate[k];
			}
			best_result = result;
		}
		for (int l = 0; l < length; l++) {
			current[l] = candidate[l];
		}
		measure = ((double) (clock() - start))/CLOCKS_PER_SEC;
	} while (measure < time_of_walker);
	for(int k=0; k < length; k++) {
		current[k] = best[k];
	}
}


void random_experiment() {
	clock_t start;
	double measure = 0.0;
	start = clock();
	int result = 0;
	int best_result = 99999;

	do {
		permuteTab(candidate, length);
		result = getTotalPathLength(candidate);
		if(result < best_result) {
			copy_arrays(candidate, best, length);
			best_result = result;
		}
		measure = ((double) (clock() - start))/CLOCKS_PER_SEC;
	} while(measure < time_of_walker);

	for(int k=0; k<length; k++) {
		current[k] = best[k];
	}
}



bool isInArray(int value, int* tab, int size) {
	bool isInArray = false;
	for(int i=0; i<size; i++) {
		if(tab[i] == value)
			isInArray = true;
	}
	return isInArray;
}

void nearest_neighbour() {
	for(int i=0; i<length; i++)
		best[i] = -1;

	int current_city = rand() % length;
	best[0] = current_city;

	for(int k = 1; k<length; k++) {
		int current_best_value = 99999999;
		int current_best_candidate = 0;
		for(int i=0; i<length; i++) {
			if(mat[current_city][i] < current_best_value && !isInArray(i, best, length)) {
				current_best_value = mat[current_city][i];
				current_best_candidate = i;
			} 
		}
		best[k] = current_best_candidate;
	}
	best_result = getTotalPathLength(best);
}



void steepest_2opt(){
	//cout << "iteracja" << endl;

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


double average(vector<double> v)
{      double sum=0;
       for(unsigned int i=0;i<v.size();i++)
               sum+=v[i];
       return (double)sum/v.size();
}
double std_dev(vector<double> v, double ave)
{
       double E=0;
       for(unsigned int i=0;i<v.size();i++)
               E+=(v[i] - ave)*(v[i] - ave);
       return sqrt(1.0/v.size()*E);
}
        



// main function of experiments
double doExperiment(double accuracy, algorytmT algorytm, double &std, int &best, double &result_avg, double &result_std, double &steps_avg, double &std_steps) {
	double prec = 1.0;
	clock_t start;
	double prev_measure = 0.0;
	double measure = 0.0;
	vector<double> times;
	vector<double> results;
	vector<double> number_of_steps_list;

	//int result = 0;
	best = 99999999;

	start = clock(); // bie¿¹cy czas systemowy w ms
	int i = 0;
	do {
		//example function
		reset();
		algorytm();
		if(best_result < best){
			best = best_result;
		}
		results.push_back((double)best_result);

		measure = ((double) (clock() - start))/CLOCKS_PER_SEC;
		times.push_back(measure - prev_measure);
		number_of_steps_list.push_back((double) number_of_steps);
		prev_measure = measure;
		i++;
	} while((measure < prec/accuracy) || (i <= 10));
	//long m =(long)(measure);
	//double result = (double) measure / i;
	std = std_dev(times, average(times));
	result_avg = average(results);
	result_std = std_dev(results, result_avg);
	steps_avg = average(number_of_steps_list);
	std_steps = std_dev(number_of_steps_list, steps_avg);
	return average(times);
}



void do_first_vs_last(algorytmT algorytm, string name) {
	cout << "Start first vs best experiment" << endl;
	vector<double> start_results;
	vector<double> best_results;
	for (int i = 0; i < 200; i++) {
		reset();
		start_results.push_back(best_result);
		algorytm();
		best_results.push_back(best_result);
	}
	cout << "out " << name << "-start ";
	for (unsigned int i= 0; i < start_results.size(); i++) {
		cout << start_results[i] << " ";
	}
	cout << endl;
	cout << "out " << name << "-best ";
	for (unsigned int i= 0; i < best_results.size(); i++) {
		cout << best_results[i] << " ";
	}
	cout << endl;
}

int main(int argc, char** argv) {
	init(argv[1]);
	if (argc >= 2) {
		if (strcmp(argv[2], "steepest") == 0) {
			do_first_vs_last(steepest_2opt, "steepest");
			exit(0);
		}
		if (strcmp(argv[2], "greedy") == 0) {
			do_first_vs_last(greedy_2opt, "greedy");
			exit(0);
		}
	}
	init(argv[1]);
	double std;
	int result; 
	double result_avg = 0.0;
	double result_std = 0.0;
	double steps_avg = 0.0;
	double std_steps = 0.0;
	double prev_time = 0.0;
	
	double time = doExperiment(1, greedy_2opt, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "greedy " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " "  << steps_avg << " "  << std_steps << " " << endl;
	//prev_time = time;
	time_of_walker = time;
	time = doExperiment(1, random_walker_2opt, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "random-walker-greedy " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " " << steps_avg << " "  << std_steps << " " << endl;
	time = doExperiment(1, random_experiment, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "random-greedy " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " " << steps_avg << " "  << std_steps << " " << endl;
	

	time = doExperiment(1, steepest_2opt, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "steepest " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " " << steps_avg << " "  << std_steps << " " << endl;
	time_of_walker = time;
	time = doExperiment(1, random_walker_2opt, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "random-walker-steepest " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " " << steps_avg << " "  << std_steps << " " << endl;
	time = doExperiment(1, random_experiment, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "random-steepest " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " " << steps_avg << " "  << std_steps << " " << endl;
	

	time = doExperiment(1, nearest_neighbour, std, result, result_avg, result_std, steps_avg, std_steps );
	cout << "nearest-neighbour " << time << " " << std << " " << result << " " << result_avg << " " << result_std << " " << length << " " << steps_avg << " "  << std_steps << " " << endl;

	return 0;
}
