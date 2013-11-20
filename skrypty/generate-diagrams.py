__author__ = 'Pawel Rychly, Dawid Wisniewski'

from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import os

destination_dir = '../sprawozdanie/diagrams/'
figure_counter = 0
line_style_counter = 0
marker_style_counter = 0

def reset_line_style_counter():
    global line_style_counter
    line_style_counter = 0

def get_marker_style():
    global marker_style_counter
    styles = ['v','o','^','s', '*', 'x']
    marker_style_counter = (marker_style_counter + 1) % 6
    return styles[marker_style_counter]


def get_line_style():
    ##return '-'
    global line_style_counter
    #styles = ['-','-.',':','...']
    styles = ['--', '-']
    line_style_counter = (line_style_counter + 1) % 2
    return styles[line_style_counter]

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
    files = listFiles('../atsp/src/first_vs_best/')
    data = {}
    for file in files:
        series_name = file[file.rfind('/')+1:file.rfind('.')]
        file_entry = open(file, 'r')
        for line in file_entry:
            line_splitted = line.split(" ")
            type_data = line_splitted[0].split("-")
            alg = type_data[0]
            type = type_data[1]
            line_splitted[0] = line_splitted[0][line_splitted[0].rfind('/')+1:line_splitted[0].rfind('.')]
            #line_splitted.pop()
            if not data.has_key(series_name + "-" + alg):
                data[series_name + "-" + alg] = {}
            if not data[series_name + "-" + alg].has_key(line_splitted[1]):
                data[series_name + "-" + alg][line_splitted[1]] = {}
            best_name = ""
            start_name = ""
            if line_splitted[1] == "value":
                start_name = "poczatkowy wynik"
                best_name = "znaleziony wynik"
            elif line_splitted[1] == "efficiency":
                start_name = "poczatkowy wynik - optimum"
                best_name = "znaleziony wynik - optimum"
            else:
                start_name = "(poczatkowy wynik - optimum) / optimum"
                best_name = "(znaleziony wynik - optimum) / optimum"

            data[series_name + "-" + alg][line_splitted[1]]['best-name'] = best_name
            data[series_name + "-" + alg][line_splitted[1]]['start-name'] = start_name

            data[series_name + "-" + alg][line_splitted[1]][type] = [float(value) for value in line_splitted[2:len(line_splitted)-2]]
    return data

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
                                      'dimnesions' : int(line_splitted[10]),
                                      'steps_avg' : float(line_splitted[11]),
                                      'std_steps' : float(line_splitted[12]),
                                      'evals_avg' : float(line_splitted[13]),
                                      'std_evals' : float(line_splitted[14]),
                                      })
        data[series_name] = sorted(data[series_name], key=lambda k: k['dimnesions'], reverse=False)
    return data


def generate_distance_from_optimum_diagram_avg(files, log = ""):

    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():

        x = [i for i in range(len(series))]#[[value['file_name']] for value in series]#[value['dimnesions'] for value in series ]
        labels = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance_avg_result'] for value in series]
        std = [value['avg_result_std'] for value in series]

        plt.errorbar(x, y,
                     yerr=std,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('usredniony wynik - optimum')
    plt.savefig(destination_dir+'avarage_results_distance_from_optimum' + log +'.pdf')

def generate_distance_from_optimum_diagram_avg_normalized(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [i for i in range(len(series))]
        labels = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance2_avg_result'] for value in series]

        plt.errorbar(x, y,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)

    plt.xlabel('rozmiar instancji')
    plt.ylabel('(usredniony wynik - optimum) / optimum')
    plt.savefig(destination_dir+'avarage_results_distance_from_optimum2' + log +'.pdf')

def generate_distance_from_optimum_diagram_best(files, log=""):

    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [i for i in range(len(series))]
        labels = [value['dimnesions'] for value in series ]
        y = [value['optimum_distance_best_result'] for value in series]

        plt.errorbar(x, y,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)


    plt.xlabel('rozmiar instancji')
    plt.ylabel('(najlepszy wynik - optimum)')
    plt.savefig(destination_dir+'best_results_distance_from_optimum' + log + '.pdf')



def generate_distance_from_optimum_diagram_best_normalized(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        labels = [value['dimnesions'] for value in series ]
        x = [i for i in range(len(series))]
        y = [value['optimum_distance2_best_result'] for value in series]

        plt.errorbar(x, y,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)

    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)
    plt.xlabel('rozmiar instancji')
    plt.ylabel('(najlepszy wynik - optimum) / optimum')
    plt.savefig(destination_dir+'best_results_distance_from_optimum2' + log +'.pdf')

def generate_time_diagram(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [i for i in range(len(series))]
        labels = [value['dimnesions'] for value in series ]
        y = [value['time'] for value in series]
        std = [value['std_time'] for value in series]

        plt.errorbar(x, y,
                     yerr=std,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('sredni czas dzialania algorytmu')
    plt.savefig(destination_dir+'time' + log +  '.pdf')


def generate_efficiency_diagram(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        labels = [value['dimnesions'] for value in series ]
        x = [i for i in range(len(series))]
        y = [value['optimum_distance_avg_result'] / value['time'] for value in series]
        #std = [value['std_time'] for value in series]

        plt.errorbar(x, y,
                     #yerr=std,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(prop = fontP)
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('srednia odleglosc od optimum / czas dzialania algorytmu')
    plt.savefig(destination_dir+'efficiency' + log +'.pdf')

def generate_efficiency2_diagram(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        x = [i for i in range(len(series))]
        labels = [value['dimnesions'] for value in series ]
        y = [1.0 /(value['optimum_distance2_avg_result'] * value['time']) for value in series]
        #std = [value['std_time'] for value in series]

        plt.errorbar(x, y,
                     #yerr=std,
                     marker=get_marker_style(),
                     label=series_name,
                     capsize=5,
                     linestyle= get_line_style())
        plt.xticks(x, labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(prop = fontP)
    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('1 / (znormalizowana odleglosc od optimum * czas dzialania algorytmu)')
    plt.savefig(destination_dir+'efficiency2' + log +'.pdf')


def generate_best_vs_first_diagram():

    data = load_best_vs_first_data()
    print data
    for file_name, series in data.iteritems():
        for series_name in series.keys():

            plt.figure(get_figure_counter())
            values = series[series_name]
            x = values['start']
            y = values['best']
            print values['best-name']
            print values['start-name']
            plt.errorbar(x, y,
                         #yerr=std,
                         marker='.',
                         capsize=5,
                         linestyle= ''
                         )
            #plt.legend()
            plt.title(file_name)
            plt.xlabel(values['start-name'])
            plt.ylabel(values['best-name'])
            plt.savefig(destination_dir + "best-vs-first/" + file_name +"-" + series_name + ".pdf")

def generate_avg_steps_diagram(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        if series_name == 'steepest' or series_name == 'greedy':
            labels = [value['dimnesions'] for value in series ]
            x = [i for i in range(len(series))]
            y = [value['steps_avg'] for value in series]
            std = [value['std_steps'] for value in series]

            plt.errorbar(x, y,
                         yerr=std,
                         marker=get_marker_style(),
                         label=series_name,
                         capsize=5,
                         linestyle= get_line_style())
            plt.xticks(x,labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)

    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('srednia liczba krokow algorytmu')
    plt.savefig(destination_dir+'avg_steps' + log + '.pdf')


def generate_avg_evals_diagram(files, log=""):
    plt.figure(get_figure_counter())
    if log == "log":
        plt.yscale(log)
    data = load_data(files)
    for series_name, series in data.iteritems():
        if series_name == 'steepest' or series_name == 'greedy':
            labels = [value['dimnesions'] for value in series ]
            x = [i for i in range(len(series))]
            y = [value['evals_avg'] for value in series]
            std = [value['std_evals'] for value in series]

            plt.errorbar(x, y,
                         yerr=std,
                         marker=get_marker_style(),
                         label=series_name,
                         capsize=5,
                         linestyle= get_line_style())
            plt.xticks(x,labels)
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc = 2, prop = fontP)

    plt.xlabel('rozmiar instancji problemu')
    plt.ylabel('srednia liczba ocenionych rozwiazan')
    plt.savefig(destination_dir+'avg_evals' + log + '.pdf')

def generate_diagrams():
    files = listFiles('../atsp/src/res/')
    print files

    #normal
    generate_distance_from_optimum_diagram_avg(files)
    generate_distance_from_optimum_diagram_avg_normalized(files)
    generate_distance_from_optimum_diagram_best(files)
    generate_distance_from_optimum_diagram_best_normalized(files)
    generate_time_diagram(files)
    generate_efficiency_diagram(files)
    generate_efficiency2_diagram(files)
    generate_avg_steps_diagram(files)
    generate_avg_evals_diagram(files)
    #log
    generate_distance_from_optimum_diagram_avg(files, log="log")
    generate_distance_from_optimum_diagram_avg_normalized(files, log = "log")
    generate_distance_from_optimum_diagram_best(files, log = "log")
    generate_distance_from_optimum_diagram_best_normalized(files, log = "log")
    generate_time_diagram(files, log = "log")
    generate_efficiency_diagram(files, log = "log")
    generate_efficiency2_diagram(files, log = "log")
    generate_avg_steps_diagram(files, log = "log")
    generate_avg_evals_diagram(files, log = "log")

    generate_best_vs_first_diagram()

generate_diagrams()