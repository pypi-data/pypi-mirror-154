""" Plotting utility imitating the uq_display functionality of UQLab """
import numpy as np  # type: ignore
from scipy.stats import norm  # type: ignore
import pandas as pd  # type: ignore
import plotly.graph_objects as go  # type: ignore
import plotly.express as px  # type: ignore
import plotly.figure_factory as ff  # type: ignore
from plotly.subplots import make_subplots  # type: ignore
import plotly.io as pio  # type: ignore

# Figure template
pio.templates.default = 'simple_white'

# Template modifications
# Size
pio.templates[pio.templates.default].layout.height = 600
pio.templates[pio.templates.default].layout.width = 600

# Grid
pio.templates[pio.templates.default].layout.xaxis.showgrid = True
pio.templates[pio.templates.default].layout.yaxis.showgrid = True
pio.templates[pio.templates.default].layout.autosize = False

# Font
pio.templates[pio.templates.default].layout.font.size = 16

# Markers
pio.templates[pio.templates.default].data.histogram[0].marker.line.width = 0


def Input(Module,
          theInterface,
          inputs=None,
          plot_density=False,
          show_vine=False):
    '''Input display is a utility function for visualising a
    random vector specified in an Input object of generated
    by the uq_default_input module. By default, it generates
    a scatter plot matrix of the elements of the random vector.
    There is also the option to plot the PDF and CDF of the
    marginal distributions of the vector components.

    Args:
        Module (dict, optional): Input parameters of multivariate
            random vectors. Defaults to None.
        inputs (list, optional): Set of indexes that define
            the variables to be displayed . Defaults to None.
        plot_density (bool, optional): Flag to plot the
            marginal distributions. Defaults to False.
    '''

    # Parameters
    M_max = 10  # Input dimension limit
    N = 1000  # Sample size
    # Number of std's for the x_range in case of input_array
    # scalar (displaying of a single marginal)
    n_std = 5

    # Define inputs
    if isinstance(Module['Marginals'], dict):
        Module['Marginals'] = [Module['Marginals']]
    M = len(Module['Marginals'])
    if inputs is None:
        inputs = range(1, M + 1)
    inputs = [f'X{var}' for var in inputs]
    n_var = len(inputs)

    # Consistency checks
    if M > M_max:
        return print(
            'Requested input range is too large, please select a smaller range.'
        )

    # Get sample for plotting
    X = theInterface.getSample(Module, N, 'LHS')
    df = pd.DataFrame(X)
    df.columns = [f'X{var}' for var in range(1, X.shape[1] + 1)]
    df = df[inputs]

    # Produce the plot
    # Scatter plot for two inputs
    if (n_var == 2) & (not plot_density):
        # Figure
        fig = px.scatter(df,
                         x=df.columns[0],
                         y=df.columns[1],
                         marginal_x='histogram',
                         marginal_y='histogram',
                         opacity=0.4)
        # Aesthetics
        marker_color_ref = pio.templates[
            pio.templates.default].layout.colorway[1]
        fig._data_objs[1].marker.color = marker_color_ref
        fig._data_objs[2].marker.color = marker_color_ref
        fig.data[1]['opacity'] = fig.data[2]['opacity'] = 1

    # Scatter matrix for >2 inputs
    elif (n_var > 2) & (not plot_density):
        width = 250 * n_var if n_var <= 5 else 250 * 6
        # Figure
        fig = ff.create_scatterplotmatrix(df,
                                          diag='histogram',
                                          marker_opacity=0.4,
                                          width=width,
                                          height=width)
        # Aesthetics
        fig.layout.hovermode = False
        # ..Scatter color
        fig.layout.colorway = [
            pio.templates[pio.templates.default].layout.colorway[0]
        ]
        # ..Histogram color
        for data in fig.data:
            if type(data) == type(go.Histogram()):
                data.marker.color = pio.templates[
                    pio.templates.default].layout.colorway[1]

    # Line plots for density functions
    else:
        # Figure
        fig = make_subplots(rows=n_var,
                            cols=2,
                            vertical_spacing=0.12,
                            subplot_titles=('PDF', 'CDF'))
        row = 1
        for var in inputs:
            # Prepare data
            marginal = [x for x in Module['Marginals'] if x['Name'] == var][0]
            x_mean, x_std = marginal['Moments']
            x = np.linspace(x_mean - n_std * x_std, x_mean + n_std * x_std, N)

            # Calculate PDF and CDF
            pdf = theInterface.all_pdf(x, marginal)
            cdf = theInterface.all_cdf(x, marginal)

            # Add data to figure
            fig.add_trace(go.Scatter(
                x=x,
                y=pdf,
                line=dict(color=pio.templates[
                    pio.templates.default].layout.colorway[row - 1]),
                name=f'{var} PDF'),
                          row=row,
                          col=1)

            fig.add_trace(go.Scatter(
                x=x,
                y=cdf,
                line=dict(color=pio.templates[
                    pio.templates.default].layout.colorway[row - 1]),
                name=f'{var} CDF'),
                          row=row,
                          col=2)
            fig.update_xaxes(title_text=var, row=row, col=1)
            fig.update_xaxes(title_text=var, row=row, col=2)
            fig.update_yaxes(title_text=f'f<sub>{var}', row=row, col=1)
            fig.update_yaxes(title_text=f'F<sub>{var}', row=row, col=2)
            row += 1

        # Aesthetics
        fig.update_layout(showlegend=False, height=500 * n_var, width=1000)

    return fig


def PCE(Model):

    # Prepare data
    Coefficients = np.array(Model['PCE']['Coefficients'])
    nnz_idx = np.abs(Coefficients) > 0
    Coefficients = Coefficients[nnz_idx]
    Indices = np.array(Model['PCE']['Basis']['Indices'])
    Indices = Indices[nnz_idx]
    Indices_row_num = np.arange(1, Indices.shape[0] + 1)
    Degree = Indices.sum(axis=1)
    legend_txt = ['Mean', '<i>p=1', '<i>p=2', '<i>p=3', '<i>p>3']
    logCoeffs = np.log10(np.abs(Coefficients))
    logCoeffRange = np.max([1, np.max(logCoeffs) - np.min(logCoeffs)])

    # Create figure traces
    traces = []
    for k in range(5):
        if k < 4:
            idx = Degree == k
        else:
            idx = Degree >= k
        traces.append(
            go.Scatter(x=Indices_row_num[idx],
                       y=np.log10(np.abs(Coefficients[idx])),
                       mode='markers',
                       marker=dict(size=15 - 2 * k, opacity=0.5),
                       name=legend_txt[k]))

    # Define figure layout
    layout = go.Layout(title=f'NNZ Coeffs: {Coefficients.shape[0]}',
                       xaxis_title='𝛼',
                       yaxis_title='log<sub>10</sub>(|𝑦<sub>𝛼</sub>|)')
    # Create figure
    fig = go.Figure(data=traces, layout=layout)

    return fig


def Kriging(Model, theInterface):
    """Display Kriging dictionary with 1-dimensional output"""

    N1d = 500  # Number of points to plot in one-dimension
    N2d = 80  # Number of points to plot in two-dimension

    # One-dimensional case

    # Compute points to plot
    X = np.array(Model['ExpDesign']['X'])
    Y = np.array(Model['ExpDesign']['Y'])
    Xmin = np.min(X)
    Xmax = np.max(X)
    Xval = np.linspace(Xmin, Xmax, N1d).transpose()
    # Exp. design points belong to evaluation
    Xval = np.sort(np.concatenate((Xval, X)))
    [Ymu_krg,
     Ysigma_krg] = theInterface.evalModel(Model,
                                          Xval.reshape([Xval.shape[0], 1]),
                                          nargout=2)

    # Compute upper and lower bounds of the confidence interval
    conf_level = 0.95  # 95% confidendence level
    conf_interval = norm.ppf(1 - 0.5 *
                             (1 - conf_level), 0, 1) * np.sqrt(Ysigma_krg)

    # Figure
    # Traces
    traces = [
        go.Scatter(x=Xval.squeeze(),
                   y=Ymu_krg.squeeze(),
                   name='Kriging approximation',
                   fill=None,
                   mode='lines',
                   legendgroup=0),
        go.Scatter(x=Xval.squeeze(),
                   y=(Ymu_krg - conf_interval).squeeze(),
                   name='95% confidence interval',
                   fill=None,
                   legendgroup=1,
                   mode='lines',
                   marker=dict(color='lightgrey'),
                   showlegend=False),
        go.Scatter(x=Xval.squeeze(),
                   y=(Ymu_krg + conf_interval).squeeze(),
                   fill='tonexty',
                   name='95% confidence interval',
                   legendgroup=1,
                   mode='lines',
                   marker=dict(color='lightgrey')),
        go.Scatter(x=X.squeeze(),
                   y=Y.squeeze(),
                   name='Observations',
                   fill=None,
                   legendgroup=2,
                   mode='markers',
                   marker=dict(color='black'))
    ]

    # Layout
    layout = go.Layout(xaxis_title='𝑋<sub>1',
                       yaxis_title='𝑌',
                       hovermode='x',
                       width=800)

    # Create figure
    fig = go.Figure(data=traces, layout=layout)

    return fig
