import os
import pandas as pd
import numpy as np
import scipy as scp
from scipy.cluster.hierarchy import distance, linkage, dendrogram, fcluster
from collections import OrderedDict, defaultdict
from natsort import natsorted, index_natsorted, order_by_index
from report_manager.plots import color_list
import urllib.request

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib.colors
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
from report_manager.plots import Dendrogram
from report_manager.plots import basicFigures
from report_manager.analyses import wgcnaAnalysis

def get_module_color_annotation(map_list, col_annotation=False, row_annotation=False, bygene=False, module_colors=[], dendrogram=[]):
    colors_dict = color_list.make_color_dict()

    n = len(map_list)
    val = 1/(n-1)
    number = 0
    colors = []
    vals = []

    if bygene == True:
        gene_colors = dict(zip(map_list, module_colors))

        for i in map_list:
            name = gene_colors[i]
            color = colors_dict[name]
            n = number
            colors.append([round(n,4), color])
            vals.append((i, round(n,4)))
            number = n+val

        labels = list(dendrogram.layout.xaxis.ticktext)
        y = [1]*len(labels)

        df = pd.DataFrame([labels, y], index=['labels', 'y']).T
        df['vals'] = df['labels'].map(dict(vals))
    else:
        for i in map_list:
            name = i.split('ME')
            if len(name) == 2:
                name = name[1]
                color = colors_dict[name]
                n = number
                colors.append([round(n,4), color])
                vals.append((i, round(n,4)))
                number = n+val
            else:
                name = name[0]
                n = number
                colors.append([round(n,4), '#ffffff'])
                vals.append((i, round(n,4)))
                number = n+val

        y = [1]*len(map_list)
        df = pd.DataFrame([map_list, y], index=['labels', 'y']).T
        df['vals'] = df['labels'].map(dict(vals))

    if row_annotation == True and col_annotation == True:
        r_annot = go.Heatmap(z=df.vals, x=df.y, y=df.labels, showscale=False, colorscale=colors, xaxis='x', yaxis='y')
        c_annot = go.Heatmap(z=df.vals, x=df.labels, y=df.y, showscale=False, colorscale=colors, xaxis='x2', yaxis='y2')
        return r_annot, c_annot
    elif row_annotation == True:
        r_annot = go.Heatmap(z=df.vals, x=df.y, y=df.labels, showscale=False, colorscale=colors, xaxis='x2', yaxis='y2')
        return r_annot
    elif col_annotation == True:
        c_annot = go.Heatmap(z=df.vals, x=df.labels, y=df.y, showscale=False, colorscale=colors, xaxis='x2', yaxis='y2')
        return c_annot
    else: pass


def get_heatmap(df, colorscale=None , color_missing=True):
    if colorscale:
        colors = colorscale
    else:
        colors = [[0, 'rgb(255,255,255)'], [1, 'rgb(255,51,0)']]

    figure = go.Figure()
    figure.add_trace(go.Heatmap(z=df.values.tolist(),
                                     y=list(df.index),
                                     x=list(df.columns),
                                     colorscale=colors,
                                     showscale=True,
                                     colorbar=dict(x=1, y=0, xanchor='left', yanchor='bottom', len=0.35, thickness=15)))
    if color_missing == True:
        df_missing = wgcnaAnalysis.get_miss_values_df(df)
        figure.add_trace(go.Heatmap(z=df_missing.values.tolist(),
                                      y=list(df.index),
                                      x=list(df.columns),
                                      colorscale=[[0, 'rgb(201,201,201)'], [1, 'rgb(201,201,201)']],
                                      showscale=False))

    return figure


def plot_labeled_heatmap(df, textmatrix, title, colorscale=[[0,'rgb(0,255,0)'],[0.5,'rgb(255,255,255)'],[1,'rgb(255,0,0)']], width=1200, height=800, row_annotation=False, col_annotation=False):
    figure = get_heatmap(df, colorscale=colorscale, color_missing=False)
    figure.add_trace(get_module_color_annotation(list(df.index), row_annotation=row_annotation, col_annotation=col_annotation, bygene=False))

    annotations = []
    for n, row in enumerate(textmatrix.values):
        for m, val in enumerate(row):
            annotations.append(go.layout.Annotation(text=str(textmatrix.values[n][m]), font=dict(size=8),
                                                    x=df.columns[m], y=df.index[n], xref='x', yref='y', showarrow=False))

    layout = go.Layout(width=width, height=height, title=title,
                       xaxis=dict(domain=[0.015, 1], autorange=True, showgrid=False, zeroline=False, showline=False, ticks='', showticklabels=True, automargin=True, anchor='y'),
                       yaxis=dict(autorange='reversed', ticklen=5, ticks='outside', tickcolor='white', showticklabels=False, automargin=True, showgrid=False, anchor='x'),
                       xaxis2=dict(domain=[0, 0.01], autorange=True, showgrid=False, zeroline=False, showline=False, ticks='', showticklabels=False, automargin=True, anchor='y2'),
                       yaxis2=dict(autorange='reversed', showgrid=False, zeroline=False, showline=False, ticks='', showticklabels=True, automargin=True, anchor='x2'))

    figure['layout'] = layout
    figure['layout'].update(annotations=annotations)

    return figure


def plot_dendrogram_guidelines(Z_tree, dendrogram):
    tickvals = list(dendrogram.layout.xaxis.tickvals)

    keys = ['type', 'x0', 'y0', 'x1', 'y1', 'line']
    line_keys = ['color', 'width', 'dash']
    line_vals = ['rgb(192,192,192)', 0.1, 'dot']
    line = dict(zip(line_keys,line_vals))

    values = []
    for i in tickvals[70::70]:
        values.append(('line', i, 0.3, i, np.max(Z_tree['dcoord'])))

    values = [list(i)+[line] for i in values]
    shapes = []
    for i in values:
        d = dict(zip(keys, i))
        shapes.append(d)

    return shapes

def plot_intramodular_correlation(MM, FS, feature_module_df, title, width=1000, height=800):

    MM['modColor'] = MM.index.map(feature_module_df.set_index('name')['modColor'].get)

    figure = tls.make_subplots(rows=len(FS.columns), cols=len(MM.columns), shared_xaxes=True, shared_yaxes=True, vertical_spacing = 0.01, horizontal_spacing = 0.01, print_grid=False)

    layout = go.Layout(width=width, height=height, showlegend=False, title=title)
    figure.layout.update(layout)

    axis_dict = {}
    for i, j in enumerate(MM.columns[MM.columns.str.startswith('MM')]):
        axis_dict['xaxis{}'.format(i+1)] = dict(title = j, titlefont = dict(size=13))
    for a, b in enumerate(FS.columns):
        name = b.split(' ')
        if len(name) > 1:
            #label = [' '.join(name[i:i+2]) for i in range(0, len(name), 2)]
            label = ['<br>'.join(name[i:i+3]) for i in range(0, len(name), 3)][0]
        else: label = name[0]
        axis_dict['yaxis{}'.format(a+1)] = dict(title = label, titlefont = dict(size=13))

    annotation = []
    for a, b in enumerate(FS.columns):
        for i, j in enumerate(MM.columns[MM.columns.str.startswith('MM')]):
            name = MM[MM['modColor'] == j[2:]].index
            x = abs(MM[MM['modColor'] == j[2:]][j].values)
            y = abs(FS[FS.index.isin(name)][b].values)

            slope, intercept, r_value, p_value, std_err = scp.stats.linregress(x, y)
            line = slope*x+intercept

            figure.append_trace(go.Scatter(x = x,
                                           y = y,
                                           text = name,
                                           mode = 'markers',
                                           opacity=0.7,
                                           marker={'size': 7,
                                                   'color': 'white',
                                                   'line': {'width': 1.5, 'color': j[2:]}}), a+1, i+1)

            figure.append_trace(go.Scatter(x = x, y = line, mode = 'lines', marker={'color': 'black'}), a+1, i+1)

            annot = dict(x = 0.7, y = 0.7,
                         xref = 'x{}'.format(i+1), yref = 'y{}'.format(a+1),
                         text = 'R={:0.2}, p={:.0e}'.format(r_value, p_value),
                         showarrow = False)
            annotation.append(annot)

    figure.layout.update(axis_dict)
    figure.layout.update(annotations = annotation)

    return figure

def plot_complex_dendrogram(dendro_df, subplot_df, title, dendro_labels=[], distfun='euclidean', linkagefun='average', hang=0.04, subplot='module colors', subplot_colorscale=[], color_missingvals=True, row_annotation=False, col_annotation=False, width=1000, height=800):

    dendro_tree = wgcnaAnalysis.get_dendrogram(dendro_df, dendro_labels, distfun=distfun, linkagefun=linkagefun, div_clusters=False)
    dendrogram = Dendrogram.plot_dendrogram(dendro_tree, hang=hang, cutoff_line=False)

    layout = go.Layout(width=width, height=height, showlegend=False, title=title,
                       xaxis=dict(domain=[0, 1], range=[np.min(dendrogram.layout.xaxis.tickvals)-6,np.max(dendrogram.layout.xaxis.tickvals)+4], showgrid=False,
                                  zeroline=True, ticks='', automargin=True, anchor='y'),
                       yaxis=dict(domain=[0.7, 1], autorange=True, showgrid=False, zeroline=False, ticks='outside', title='Height', automargin=True, anchor='x'),
                       xaxis2=dict(domain=[0, 1], autorange=True, showgrid=True, zeroline=False, ticks='', showticklabels=False, automargin=True, anchor='y2'),
                       yaxis2=dict(domain=[0, 0.64], autorange=True, showgrid=False, zeroline=False, automargin=True, anchor='x2'))


    if subplot == 'module colors':
        figure = tls.make_subplots(rows=2, cols=1, print_grid=False)

        for i in list(dendrogram.data):
            figure.append_trace(i, 1, 1)

        shapes = plot_dendrogram_guidelines(dendro_tree, dendrogram)
        moduleColors = get_module_color_annotation(dendro_labels, col_annotation=col_annotation, bygene=True, module_colors=subplot_df, dendrogram=dendrogram)
        figure.append_trace(moduleColors, 2, 1)
        figure['layout'] = layout
        figure['layout'].update({'shapes':shapes,
                              'xaxis':dict(showticklabels=False),
                              'yaxis':dict(domain=[0.2, 1]),
                              'yaxis2':dict(domain=[0, 0.19], title='Module colors', ticks='', showticklabels=False)})


    elif subplot == 'heatmap':
        if all(list(subplot_df.columns.map(lambda x: subplot_df[x].between(-1,1, inclusive=True).all()))) != True:
            df = wgcnaAnalysis.get_percentiles_heatmap(subplot_df, dendro_tree, bydendro=True, bycols=True)
        else:
            df = wgcnaAnalysis.df_sort_by_dendrogram(wgcnaAnalysis.df_sort_by_dendrogram(subplot_df.T, dendro_tree), dendro_tree)

        heatmap = get_heatmap(df, colorscale=subplot_colorscale, color_missing=color_missingvals)


        if row_annotation == True and col_annotation == True:
            figure = tls.make_subplots(rows=3, cols=2, specs=[[{'colspan':2}, None],
                                                              [{}, {}],
                                                              [{'colspan':2}, None]], print_grid=False)
            for i in list(dendrogram.data):
                figure.append_trace(i, 1, 1)
            for j in list(heatmap.data):
                figure.append_trace(j, 2, 2)

            r_annot, c_annot = get_module_color_annotation(list(df.index), row_annotation=row_annotation, col_annotation=col_annotation, bygene=False)
            figure.append_trace(r_annot, 2, 1)
            figure.append_trace(c_annot, 3, 1)

            figure['layout'] = layout
            figure['layout'].update({'xaxis':dict(ticks='', showticklabels=False, anchor='y'),
                                     'xaxis2':dict(domain=[0, 0.01], ticks='', showticklabels=False, automargin=True, anchor='y2'),
                                     'xaxis3':dict(domain=[0.015, 1], ticks='', showticklabels=False, automargin=True, anchor='y3'),
                                     'xaxis4':dict(domain=[0.015, 1], ticks='', showticklabels=True, automargin=True, anchor='y4'),
                                     'yaxis':dict(domain=[0.635, 1], automargin=True, anchor='x'),
                                     'yaxis2':dict(domain=[0.015, 0.635], autorange='reversed', ticks='', showticklabels=True, automargin=True, anchor='x2'),
                                     'yaxis3':dict(domain=[0.01, 0.635], autorange='reversed', ticks='', showticklabels=False, automargin=True, anchor='x3'),
                                     'yaxis4':dict(domain=[0,0.01], ticks='', showticklabels=False, automargin=True, anchor='x4')})



        elif row_annotation == False and col_annotation == False:
            figure = tls.make_subplots(rows=2, cols=1, print_grid=False)

            for i in list(dendrogram.data):
                figure.append_trace(i, 1, 1)
            for j in list(heatmap.data):
                figure.append_trace(j, 2, 1)

            figure['layout'] = layout
            figure.layout.update({'xaxis':dict(ticktext=np.array(dendrogram.layout.xaxis.ticktext), tickvals=list(dendrogram.layout.xaxis.tickvals)),
                              'yaxis2':dict(autorange='reversed')})

        elif row_annotation == True:# and (col_annotation == False):
            figure = tls.make_subplots(rows=2, cols=2, specs=[[{'colspan':2}, None],
                                                              [{}, {}]], print_grid=False)
            for i in list(dendrogram.data):
                figure.append_trace(i, 1, 1)
            for j in list(heatmap.data):
                figure.append_trace(j, 2, 2)

            r_annot = get_module_color_annotation(list(df.index), row_annotation=row_annotation, col_annotation=col_annotation, bygene=False)
            figure.append_trace(r_annot, 2, 1)

            figure['layout'] = layout
            figure['layout'].update({'xaxis':dict(domain=[0.015, 1], ticktext=np.array(dendrogram.layout.xaxis.ticktext), tickvals=list(dendrogram.layout.xaxis.tickvals), automargin=True, anchor='y'),
                                     'xaxis2':dict(domain=[0, 0.010], ticks='', showticklabels=False, automargin=True, anchor='y2'),
                                     'xaxis3':dict(domain=[0.015, 1], ticks='', showticklabels=False, automargin=True, anchor='y3'),
                                     'yaxis':dict(automargin=True, anchor='x'),
                                     'yaxis2':dict(autorange='reversed', ticks='', showticklabels=True, automargin=True, anchor='x2'),
                                     'yaxis3':dict(domain=[0, 0.64], ticks='', showticklabels=False, automargin=True, anchor='x3')})

        elif col_annotation == True:
            figure = tls.make_subplots(rows=3, cols=1, specs=[[{}], [{}], [{}]], print_grid=False)

            for i in list(dendrogram.data):
                figure.append_trace(i, 1, 1)
            for j in list(heatmap.data):
                figure.append_trace(j, 3, 1)

            c_annot = get_module_color_annotation(list(df.index), row_annotation=row_annotation, col_annotation=col_annotation, bygene=False)
            figure.append_trace(c_annot, 2, 1)

            figure['layout'] = layout
            figure['layout'].update({'xaxis':dict(ticktext=np.array(dendrogram.layout.xaxis.ticktext), tickvals=list(dendrogram.layout.xaxis.tickvals), automargin=True, anchor='y'),
                                     'xaxis2':dict(ticks='', showticklabels=False, automargin=True, anchor='y2'),
                                     'xaxis3':dict(domain=[0, 1], ticks='', showticklabels=False, automargin=True, anchor='y3'),
                                     'yaxis':dict(domain=[0.70, 1], automargin=True, anchor='x'),
                                     'yaxis2':dict(domain=[0.615, 0.625], ticks='', showticklabels=False, automargin=True, anchor='x2'),
                                     'yaxis3':dict(domain=[0, 0.61], autorange='reversed', ticks='', showticklabels=False, automargin=True, anchor='x3')})
        else: pass

    else: pass

    return figure