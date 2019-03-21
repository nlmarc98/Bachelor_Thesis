import numpy as np
import matplotlib.pyplot as plt

def plotProbTable(rods, prob_table):
    plt.plot(rods * 180 / np.pi, prob_table)
    plt.title('Generative Rod Distribution for each Frame Orientation')
    plt.xlabel('rod [deg]')
    plt.ylabel('P(right)')
    plt.pause(0.001)


class StimuliPlotter:

    def __init__(self, iterations_num, stim_min, stim_max, params_gen):
        self.iterations_num = iterations_num

        # set minimal and maximal stimulus values in degrees
        self.stim_min = stim_min * 180 / np.pi
        self.stim_max = stim_max * 180 / np.pi

        # set the generative parameter values
        self.params_gen = params_gen

        # initialize stimuli and params as Nones
        self.stimuli = None
        self.params = None


    def initStimuliFigure(self):
        # initialize selected stimuli plot
        figure_stimuli = plt.figure()
        self.plot_stimuli = figure_stimuli.add_subplot(1, 1, 1)

        # initialize stimuli
        self.stimuli = ([], [])


    def plotStimuli(self, rod, frame):
        if self.stimuli is None:
            self.initStimuliFigure()

        # add rod and frame to self.stimuli
        self.stimuli[0].append(rod * 180.0 / np.pi)
        self.stimuli[1].append(frame * 180.0 / np.pi)

        # compute current trial number
        trial_num = len(self.stimuli[0])

        # plot selected stimuli
        self.plot_stimuli.clear()
        self.plot_stimuli.scatter(np.arange(trial_num), self.stimuli[0], label='rod [deg]')
        self.plot_stimuli.scatter(np.arange(trial_num), self.stimuli[1], label='frame [deg]')
        self.plot_stimuli.set_xlabel('trial number')
        self.plot_stimuli.set_ylabel('selected stimulus [deg]')
        self.plot_stimuli.set_xlim(0, self.iterations_num)
        self.plot_stimuli.set_ylim(self.stim_min, self.stim_max)
        self.plot_stimuli.set_title('Selected Stimuli for each Trial')
        self.plot_stimuli.legend()

        # pause to let pyplot draw plot
        plt.pause(0.0001)


    def initParameterFigure(self):
        # initialize calculated parameter values plots
        figure_params = plt.figure(figsize=(15, 8))
        self.plot_kappa_ver = figure_params.add_subplot(2, 3, 1)
        self.plot_kappa_hor = figure_params.add_subplot(2, 3, 2)
        self.plot_tau = figure_params.add_subplot(2, 3, 4)
        self.plot_kappa_oto = figure_params.add_subplot(2, 3, 5)
        self.plot_lapse = figure_params.add_subplot(2, 3, 6)

        # size of points in parameter values graph
        self.point_size = 5

        # initialize parameter and parameter plot dictionaries
        self.params = {'kappa_ver': [], 'kappa_hor': [], 'tau': [], 'kappa_oto': [], 'lapse': []}
        self.param_plots = {'kappa_ver': self.plot_kappa_ver, 'kappa_hor': self.plot_kappa_hor, 'tau': self.plot_tau,
                            'kappa_oto': self.plot_kappa_oto, 'lapse': self.plot_lapse}


    def plotParameterValues(self, params):
        if self.params is None:
            self.initParameterFigure()

        # draw each parameter's values plot
        for param in self.params.keys():
            # add parameter value to self.params
            self.params[param].append(params[param])

            # plot specific parameter's values graph
            self.__plotParemeterValues(param)

        # add a single legend to the figure
        handles, labels = self.plot_kappa_ver.get_legend_handles_labels()
        self.plot_kappa_ver.get_figure().legend(handles, labels, loc='upper right')

        # fit all the plots to the screen with no overlapping text
        plt.tight_layout()

        # pause to let pyplot draw graphs
        plt.pause(0.0001)


    def __plotParemeterValues(self, param):
        # compute current trial number
        trial_num = len(self.params[param])

        # retreive specific parameter plot from self.param_plots
        plot = self.param_plots[param]

        # plot specific parameter values
        plot.clear()
        plot.hlines(self.params_gen[param], 1, self.iterations_num, label='generative parameter value')
        plot.scatter(np.arange(trial_num), self.params[param], s=self.point_size, label='calculated parameter value')
        plot.set_xlabel('trial number')
        plot.set_ylabel(param)
        plot.set_xlim(0, self.iterations_num)
        plot.set_title('Calculated %s Values for each Trial' % param)