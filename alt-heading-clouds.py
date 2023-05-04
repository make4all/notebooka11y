# %% [markdown]
# # wordcloud for headings
# %% [markdown]
# # wordcloud
# %% [markdown]
# ## setup
from wordcloud import WordCloud
alt = ''
h1 = ''

h2 = ''
h3 = ''
h4 = ''
h5 = ''
h6 = ''
with open('texts/alt.txt', 'r') as f:
    alt = f.read()
    # remove new lines
    alt = alt.replace('\n', ' ')
with open('texts/h1.txt', 'r') as f:
    h1 = f.read()
    h1 = h1.replace('\n', ' ')
with open('texts/h2.txt', 'r') as f:
    h2 = f.read()
    h2 = h2.replace('\n', ' ')
with open('texts/h3.txt', 'r') as f:
    h3 = f.read()
    h3 = h3.replace('\n', ' ')
with open('texts/h4.txt', 'r') as f:
    h4 = f.read()
    h4 = h4.replace('\n', ' ')
with open('texts/h5.txt', 'r') as f:
    h5 = f.read()
    h5 = h5.replace('\n', ' ')

with open('texts/h6.txt', 'r') as f:
    h6 = f.read()
    h6 = h6.replace('\n', ' ')
heading = h1+' '+h2+' '+h3+' '+h4+' '+h5+' '+h6
altCloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
altCloud.generate(alt)
altCloud.to_image()
altCloud.to_file('altCloud.png')
headingCloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
headingCloud.generate(heading)
headingCloud.to_image()
headingCloud.to_file('headingCloud.png')

h1Cloud = WordCloud(background_color="white", max_words=5000, contour_width=3, contour_color='steelblue')
h1Cloud.generate(h1)
h1Cloud.to_image()
h1Cloud.to_file('h1Cloud.png')


