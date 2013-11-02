__author__ = 'Pawel Rychly, Dawid Wisniewski'

import matplotlib.pyplot as plt
import os

destination_dir = '../sprawozdanie/diagrams/'
figure_counter = 0

def get_figure_counter():
    global figure_counter
    figure_counter += 1
    return figure_counter

def listFiles(dir):
    result = []
    for item in os.listdir(dir):
        if item.endswith('.txt'):
            result.append(os.path.join(dir, item))
    return result

def load_best_vs_first_data():
    return

def load_data(files):
    data = {}
    for file in files:
        series_name = file[file.rfind('/')+1:file.rfind('.')]
        data[series_name] = []
        file_entry = open(file, 'r')
        for line in file_entry:
            line_splitted = line.split(" ")
            line_splitted[0] = line_splitted[0][line_splitted[0].rfind('/')+1:line_splitted[0].rfind('.')]
            #line_splitted.pop()
            data[series_name].append({'file_name': line_splitted[0],
                                      'time' : float(line_splitted[1]),
                                      'std_time' : float(line_splitted[2]),
                                      'best_result' : float(line_splitted[3]),
                                      'optimum_distance_best_result': float(line_splitted[4]),
                                      'optimum_distance2_best_result' : float(line_splitted[5]),
                                      'avg_result' : float(line_splitted[6]),
                                      'optimum_distance_avg_result' : float(line_splitted[7]),
                                      'optimum_distance2_avg_result' : float(line_splitted[8]),
                                      'avg_result_std' : float(line_splitted[9]),
                                      'dimnesions' : float(int(line_splitted[10])),
                                      })
        data[series_name] = sorted(data[series_name], key=lambda k: k['dimnesions'], reverse=False)
    return data


def generate_distance_from_optimum_diagram_avg(files):

    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance_avg_result'] for value in series]
        std = [value['avg_result_std'] for value in series]

        plt.errorbar(x, y,
                     yerr=std,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')
    plt.legend()
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('usredniony wynik - optimum')
    plt.savefig(destination_dir+'avarage_results_distance_from_optimum.pdf')

def generate_distance_from_optimum_diagram_avg_normalized(files):
    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance2_avg_result'] for value in series]

        plt.errorbar(x, y,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')
    plt.legend()
    plt.xlabel('rozmiar instancji')
    plt.ylabel('(usredniony wynik - optimum) / optimum')
    plt.savefig(destination_dir+'avarage_results_distance_from_optimum2.pdf')

def generate_distance_from_optimum_diagram_best(files):

    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance_best_result'] for value in series]

        plt.errorbar(x, y,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')
    plt.legend()
    plt.xlabel('rozmiar instancji')
    plt.ylabel('(najlepszy wynik - optimum)')
    plt.savefig(destination_dir+'best_results_distance_from_optimum.pdf')



def generate_distance_from_optimum_diagram_best_normalized(files):
    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance2_best_result'] for value in series]

        plt.errorbar(x, y,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')

    plt.legend()
    plt.xlabel('rozmiar instancji')
    plt.ylabel('(najlepszy wynik - optimum) / optimum')
    plt.savefig(destination_dir+'best_results_distance_from_optimum2.pdf')

def generate_time_diagram(files):
    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['time'] for value in series]
        std = [value['std_time'] for value in series]

        plt.errorbar(x, y,
                     yerr=std,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')
    plt.legend()
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('czas dzialania algorytmu')
    plt.savefig(destination_dir+'time.pdf')

def generate_time_diagram(files):
    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['time'] for value in series]
        std = [value['std_time'] for value in series]

        plt.errorbar(x, y,
                     yerr=std,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')
    plt.legend()
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('czas dzialania algorytmu')
    plt.savefig(destination_dir+'time.pdf')

def generate_efficiency_diagram(files):
    plt.figure(get_figure_counter())
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance_avg_result'] / value['time'] for value in series]
        #std = [value['std_time'] for value in series]

        plt.errorbar(x, y,
                     #yerr=std,
                     marker='o',
                     label=series_name,
                     capsize=5,
                     linestyle='-')
    plt.legend()
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('srednia odleglosc od optimum / czas dzialania algorytmu')
    plt.savefig(destination_dir+'efficiency.pdf')




def generate_diagrams():
    files = listFiles('../atsp/src/res/')
    print files
    generate_distance_from_optimum_diagram_avg(files)
    generate_distance_from_optimum_diagram_avg_normalized(files)
    generate_distance_from_optimum_diagram_best(files)
    generate_distance_from_optimum_diagram_best_normalized(files)
    generate_time_diagram(files)
    generate_efficiency_diagram(files)
generate_diagrams()
    #matplotlib.savefig('foo.pdf')
#def temp():
    #for file in listFiles('../data-atsp/'):
    #    print file
    #    exact_filename=file[file.rfind('/')+1:file.rfind('.')]
    #    #print exact_filename
    #    result = runProgram(file)
    #    #print result
    #    for line in result:
    #        if len(line) < 4:
    #            continue
    #        print line
    #        splitted = line.split(" ")
    #        f = open('res/' + splitted[0] + '.txt', 'a')
    #        f.write(file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(float(splitted[4])-float(best[exact_filename])) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] + " " + splitted[6] +" \n")
    #        #file + " " + splitted[1] + " " + splitted[2] + " " + splitted[3] + " " + str(int(splitted[3])-best[exact_filename]) + " " + str((float(splitted[3])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[4] + " " + str(int(splitted[4])-best[exact_filename]) + " " + str((float(splitted[4])-float(best[exact_filename]))/float(best[exact_filename])) + " " + splitted[5] +"\n"
    #        f.close()