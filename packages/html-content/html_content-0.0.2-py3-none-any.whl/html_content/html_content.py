from typing import List
from markdown import markdown
from matplotlib.figure import Figure
import base64
from io import BytesIO
import seaborn as sns
import pandas as pd
import numpy as np
from pandas.io.formats.style import Styler
import logging
from html_content.default import HTML_TEMPLATE
from html_content.type import Type


class HtmlContent(object):
    def __init__(self, title) -> None:
        self.title = title
        self.contents: List[str] = []

    def add_matplotlib_fig(self, fig: Figure):
        """Add figure created by matplotlib, seaborn, pandas, etc.
        """
        tmpfile = BytesIO()
        fig.savefig(tmpfile, format='png')
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        html = '<div><img src=\'data:image/png;base64,{}\'>'.format(encoded)
        self.contents.append(html)

    def add_plotly_fig(self, fig):
        """Add figure created by plotly
        """
        content = fig.to_html(full_html=False, include_plotlyjs='cdn')
        self.contents.append(content)

    def add_markdown(self, content, bg_color=Type.DEFAULT):
        """Add markdown block
        """
        logging.info(f'adding markdown: {content}')
        html = markdown(content)
        if bg_color != Type.DEFAULT:
            colors = {
                Type.SUCCESS: 'text-success bg-dark',
                Type.INFO: 'text-info',
                Type.WARNING: 'text-warning',
                Type.ERROR: 'text-danger',
            }[bg_color]
            html = f'<div class="{colors}">{html}</div>'
        self.contents.append(html)

    def add_html(self, content):
        self.contents.append(content)

    def _wrap(self, html):
        return f'<div>{html}</div>'

    def add_df(self, df: pd.DataFrame,
               caption='',
               color_axis=0,
               diverging_gradient=False,
               reverse_gradient=False):
        """Add pandas DataFrame

        Args:
            df (pd.DataFrame): pandas DataFrame
            caption (str, optional): caption for table. Defaults to ''.
            color_axis (int, optional): add background gradient to axis if color_axis >= 0. Defaults to 0.
            diverging_gradient (bool, optional): if True, use diverging color gradient. Otherwise, using sequantial color gradient. Defaults to False.
        """
        styler = Styler(df)
        styler.set_table_attributes('class="table table-bordered table-fit table-hover"')
        if caption:
            styler.set_caption(caption=caption)

        if color_axis >= 0:
            columns = df.select_dtypes(include=[np.float32, np.float64, np.int32, np.int64]).columns.tolist()   # type: ignore
            color_right = 240
            color_left = 50
            if diverging_gradient:
                left, right = (color_left, color_right)
                if reverse_gradient:
                    left, right = right, left
                cm = sns.diverging_palette(h_neg=left,
                                           h_pos=right,
                                           s=70,
                                           l=60,
                                           sep=1,
                                           as_cmap=True,
                                           center='light')
            else:
                color = color_right if not reverse_gradient else color_left
                cm = sns.light_palette((color, 70, 60), input="husl", as_cmap=True)
            styler.background_gradient(axis=color_axis, cmap=cm, subset=columns)
            styler.highlight_max(axis=color_axis,
                                 props='font-weight:bold;',  # type: ignore
                                 subset=columns)   # type: ignore
        html = styler.to_html()     # type: ignore
        self.add_html(html)

    def get_html(self):
        content = HTML_TEMPLATE.replace('TITLE', self.title)
        content = content.replace('CONTENT', '\n'.join([self._wrap(x) for x in self.contents]))
        return content

    def save_html(self, path):
        html = self.get_html()
        with open(path, 'w') as outfile:
            outfile.write(html)
