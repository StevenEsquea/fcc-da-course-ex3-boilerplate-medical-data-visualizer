import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('medical_examination.csv')

aux_df = df['weight'] / ((df['height']/100)**2)
df['overweight'] = aux_df > 25
df['overweight'] = df['overweight']*1

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 1, 'gluc'] = 1
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 1, 'cholesterol'] = 1

def draw_cat_plot():
    df_cat = pd.melt(df, id_vars='cardio', value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    g = sns.FacetGrid(data=df_cat, col='cardio', height=5, aspect=1)
    g.map(sns.countplot, 'variable', hue='value', data=df_cat, order=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'], palette="bright")
    g.set_ylabels("total")
    g.add_legend(title='value')
    fig = g.fig
    fig.savefig('catplot.png')
    return fig

def draw_heat_map():
    df_heat = df.drop(df[df['ap_lo'] > df['ap_hi']].index)

    aux_series = (df_heat['height'] < df_heat['height'].quantile(q=0.025)) | (df_heat['height'] > df_heat['height'].quantile(q=0.975))
    aux_series2 = (df_heat['weight'] < df_heat['weight'].quantile(q=0.025)) | (df_heat['weight'] > df_heat['weight'].quantile(q=0.975))
    aux_series3 = aux_series | aux_series2
    df_heat = df_heat.drop(df_heat[aux_series2].index)
    corr = df_heat.corr()
    mask = np.tril(np.ones_like(corr, dtype=np.bool_), k=-1)
    corr.where(mask)
    
    fig, ax = plt.subplots()
    sns.heatmap(corr.where(mask), annot=True, fmt=".1f", ax=ax)
    fig.savefig('heatmap.png')
    return fig
