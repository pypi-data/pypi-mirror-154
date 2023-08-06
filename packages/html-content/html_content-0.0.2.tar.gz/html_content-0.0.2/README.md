# HTML Content

Easily construct HTML document with pandas DataFrame, markdown, matplotlib, plotly and HTML.

This tiny package can help build organized content similar to Jupyter notebook, while using pure python code.


## Install

`pip install html-content==0.0.1`

## Example


For full example code, please refer to [test.py](example/test.py).

```python
content = HtmlContent('Title of example')

# markdown
content.add_markdown('# Header')
content.add_markdown('***')
content.add_markdown('## success text', bg_color=Type.SUCCESS)
content.add_markdown('## warning text', bg_color=Type.WARNING)
content.add_markdown('## error text', bg_color=Type.ERROR)
content.add_markdown('normal text')

# add fig
content.add_matplotlib_fig(create_matplotlib_fig())
content.add_plotly_fig(create_plotly_fig())

# add HTML
content.add_html('<b>Bold font</b>')

# add pandas
df = create_df()
content.add_df(df, caption='pandas table with diverging_gradient=False', diverging_gradient=False)
content.add_df(df, caption='pandas table with diverging_gradient=True', diverging_gradient=True)

# save content to HTML
# content.get_html()
content.save_html('example/content.html')
```

### Snapshot of `example/content.html`


![Part1](example/img/part1.png)
![Part2](example/img/part2.png)
![Part3](example/img/part3.png)


## Reference
- [Seaborn light_palette](https://seaborn.pydata.org/generated/seaborn.light_palette.html), [Seaborn diverging_palette](https://seaborn.pydata.org/generated/seaborn.diverging_palette.html#seaborn.diverging_palette)
- [Pandas table visualization](https://pandas.pydata.org/docs/user_guide/style.html)
- [Plotly to_html](https://plotly.com/python-api-reference/generated/plotly.io.to_html.html)
- [Seaborn, matplotlib to html](https://stackoverflow.com/a/48717971)
- [Python markdown](https://python-markdown.github.io/)
