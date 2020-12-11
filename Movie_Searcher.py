#!/usr/bin/env python
# coding: utf-8

# In[139]:
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import pandas as pd
from bs4 import BeautifulSoup 
import requests

# In[141]:

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=0.55"}]
        )

#####------------------Controls Starts Here-------------------------######
# Colors
banner_color = 'black'
title_font_color = 'black'
font_color = '#FFFFFF'
background_color = 'E3E2DC'
tile_color = '#333333'

# Controls
controls = dbc.Card(
    [
        dbc.Row(
            [
            dbc.Col(
                [
                    dbc.Label("Enter Movie Name: "),
                    html.Div([
                              dcc.Input(id='my_input', value='Star Wars: Episode IX - The Rise of Skywalker', 
                                        placeholder = 'Search Movie', type='text', style = {'width':'100%'})]),
                ],
                xs=12, sm=12, md=12, lg=4, xl=4,
            ),
            dbc.Col(
                [
                    dbc.Button("Search for the Movie", color="primary", id="sbumit_buttom")
                    ],
                xs=12, sm=12, md=12, lg=2, xl=2,
                style = {"margin-top": "10px", 'margin-left':'20px',}
                )
            
            ],
            justify="start"
        )
        
    ],
    body=True, 
    style={'display': 'inline-block',
           'min-height':'100%',
           'border-radius': '5px',
           #'box-shadow': '8px 8px 8px grey',
           'background-color': tile_color,
           'padding': '10px',
           'margin-bottom': '10px',
           'textAlign' : 'left',
           'top': '0px',
           'align-self': 'auto',
           'position': 'sticky',
           'zIndex': 999,
           'color':font_color
          }
)

#####------------------app layout Starts Here-------------------------######

# logo image
image_filename = 'IMDB_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')


app.layout = dbc.Container( 
    [   
        dbc.Row([
            dbc.Col(
                html.Img(
                       src='data:image/png;base64,{}'.format(encoded_image),
                       id="logo-image",
                       style={
                           "height": "70px",
                           "width": "auto",
                           "margin-top": "3px",
                           'textAlign' : 'left',
                           'display': 'inline-block'}),
                xs=12, sm=12, md=12, lg=3, xl=3,
            ),
            dbc.Col([
                html.H1("Movie Searcher",  
                        style = {'textAlign' : 'Center',
                                 "margin-top": "0px", 
                                 'color': title_font_color}),
                html.H6('Search for Movie Information.',
                          style={'textAlign' : 'Center',
                                 'width' :'flex',
                                 'font-size' : '12px', 
                                 'color': title_font_color}),
            ], xs=12, sm=12, md=12, lg=6, xl=6,
            ),
            dbc.Col(
            html.A(
                html.Button("IMDB.COM", id="learn-more-button"),
                href="https://www.imdb.com/",
                style={'display': 'inline-block',
                       "margin-top": "20px", 'width' : '100%', 
                       'textAlign' : 'right'}
               ), xs=12, sm=12, md=12, lg=3, xl=3,
            ),
    ],
            style= {"backgroundColor" : background_color}
        ),
        dbc.Row(controls),
        html.Hr(),
        dbc.Row([dbc.Spinner(html.Div(id="alert_dash"), color="light")], 
                    style={'textAlign' : 'right'},
                ),
        dbc.Row(
            [
                dbc.Col(
                    
                    [
                        dbc.Spinner(html.Div(id="alert_msg"), color="light"),
                        dbc.CardImg(id="picture", top=True)],xs=10, sm=10, md=10, lg=5, xl=5,
                        style={'display': 'inline-block', 
                               #'width': 'flex',
                               'border-radius': '5px',
                               #'box-shadow': '8px 8px 8px grey',
                               'background-color': tile_color,
                               'padding': '10px',
                               'margin-right': '10px',
                               'margin-top': '10px',
                              }
                ),
                dbc.Col(
                    [
                    dbc.Row(
                             dbc.Col([
                                     html.Br(),
                                     dbc.Row(html.H2(id='my-title',style={"color": 'white'})),
                                     html.Br(),
                                     html.Br(),
                                     html.Br(),
                                     dbc.Row(html.H4(id='my-rating',style={"color": 'white'})),
                                     dbc.Row(html.H4(id='my-genre',style={"color": 'white'})),
                                     dbc.Row(html.H4(id='my-cast',style={"color": 'white'})),
                                     dbc.Row(html.H4(id='my-duration',style={"color": 'white'})),
                                     dbc.Row(html.H4(id='my-parental_rating',style={"color": 'white'})),
                                     dbc.Row(html.H4(id='my-release_date',style={"color": 'white'})),
                                     dbc.Row(html.H4(id='my-director',style={"color": 'white'}))
                                     
                                    
                                     ],style ={'margin-left': '50px'}),
                                     
                        
                    ),
                    ], xs=10, sm=10, md=10, lg=5, xl=5,
                        style={'display': 'inline-block', 
                               #'width': 'flex',
                               'border-radius': '5px',
                               #'box-shadow': '8px 8px 8px grey',
                               'background-color': tile_color,
                               'padding': '10px',
                               'margin-right': '10px',
                               'margin-top': '10px',
                              },
             )
                ],
                justify="center"
             ),
        
    ],
    fluid=True, style={'background-color':background_color}#'display': 'block'}
)

# In[]
####Helper Function
# finding selectors 
movie_title_selector = 'h1'
movie_genre_selector = '.subtext a'
movie_cast_selector = '#titleCast .loadlate'
movie_poster_selector = '.poster img'
movie_rating_selector = '.ratingValue span'
url = 'https://www.imdb.com/title/tt1185834/'
headers = {"Accept-Language": "en-US,en;q=0.5"} # making sure the language scraped will be set in English
response = requests.get(url, headers = headers)
html_str = response.text
soup = BeautifulSoup(html_str)

movie_title = soup.select(movie_title_selector)[0].text.replace('\xa0', " ")
print(movie_title)
# getting movie_genre
movie_genre = [i.text for i in soup.select(movie_genre_selector)][:-1]
print(movie_genre)
# getting movie_cast
movie_cast = [i.get('alt') for i in soup.select(movie_cast_selector)]
print(movie_cast)
# getting movie_poster
movie_poster = soup.select(movie_poster_selector)[0].get('src')
print(movie_poster)
# getting movie_rating
movie_rating = float(soup.select(movie_rating_selector)[0].text)
print(movie_rating)


movie_time = soup.find_all('div', attrs = {'class':'subtext'})[0].find_all('time')[0].text.strip()
movie_parental_rating = soup.find_all('div', attrs = {'class':'subtext'})[0].text.strip().split('\n')[0]
movie_release_date = soup.find_all('div', attrs = {'class':'subtext'})[0].find_all('a')[-1].text.strip().replace(' (USA)', '')
movie_director = soup.find_all('div', attrs = {'class' : 'credit_summary_item'})[0].find_all('a')[0].text


fields_we_are_scaping = ["Movie Title", "Movie Poster Link", "Rating", "Genre", "Cast", "Duration", 
                         "Parental Rating", "Release Date", "Director"] # creating fields that we are going to scraped
scraped_data = {keys:[] for keys in fields_we_are_scaping} # convert field to dict format

def get_movie_data_using_title(movie):
    scraped_data = {keys:[] for keys in fields_we_are_scaping} # clean up scraped data from previous search
    movie_title_selector = 'h1'
    movie_genre_selector = '.subtext a'
    movie_cast_selector = '#titleCast .loadlate'
    movie_poster_selector = '.poster img'
    movie_rating_selector = '.ratingValue span'
    #request finding data
    scraped_url_list = []
    headers = {"Accept-Language": "en-US,en;q=0.5"}
    params = {'q': movie, 's' : 'tt', 'ttype' : 'ft', 'ref' : 'fn_ft'} # q is our search input parameters
    response = requests.get('https://www.imdb.com/find', params = params, headers = headers)
    html_str = response.text
    soup = BeautifulSoup(html_str)
    search_result = soup.select('.result_text > a')
    for result in search_result:
        movie_url = 'https://www.imdb.com' + result.get('href') # combining the movies url with domain url
        scraped_url_list.append(movie_url)
        
    #request movie data from movie url
    for i, movie_url in enumerate (scraped_url_list[:1], start = 1): # only run ten search result, often times search result after the tenth is not relevant to our search
        headers = {"Accept-Language": "en-US,en;q=0.5"}
        response_movie = requests.get(movie_url, headers = headers)
        html_movie_str = response_movie.text
        soup_movie = BeautifulSoup(html_movie_str)
        # parsing data
        movie_title = soup_movie.select(movie_title_selector)[0].text.replace('\xa0', " ")
        #print('Working on {}'.format(movie_url),'Movie: {}'.format(movie_title), i,'/', 10)

        try:
            movie_poster = soup_movie.select(movie_poster_selector)[0].get('src')
        except:
            movie_poster = 'NA'
        try:
            movie_rating = float(soup_movie.select(movie_rating_selector)[0].text)
        except:
            movie_rating = 'NA'
        movie_genre = [i.text for i in soup_movie.select(movie_genre_selector)][:-1]
        movie_cast = [i.get('alt') for i in soup_movie.select(movie_cast_selector)]
        
        movie_time = soup_movie.find_all('div', attrs = {'class':'subtext'})[0].find_all('time')[0].text.strip()
        movie_parental_rating = soup_movie.find_all('div', attrs = {'class':'subtext'})[0].text.strip().split('\n')[0]
        movie_release_date = soup_movie.find_all('div', attrs = {'class':'subtext'})[0].find_all('a')[-1].text.strip().replace(' (USA)', '')
        movie_director = soup_movie.find_all('div', attrs = {'class' : 'credit_summary_item'})[0].find_all('a')[0].text


        #appending all data to scraped data
        scraped_data['Movie Title'].append(movie_title)
        scraped_data['Movie Poster Link'].append(movie_poster)
        scraped_data['Rating'].append(movie_rating)
        scraped_data['Genre'].append(movie_genre)
        scraped_data['Cast'].append(movie_cast)
        scraped_data['Duration'].append(movie_time)
        scraped_data['Parental Rating'].append(movie_parental_rating)
        scraped_data['Release Date'].append(movie_release_date)
        scraped_data['Director'].append(movie_director)

    return pd.DataFrame(scraped_data)

df = get_movie_data_using_title('Stars war')

# In[]


#####------------------Function Starts Here-------------------------######
@app.callback(
    [Output(component_id = 'alert_msg', component_property = 'children'),
     Output(component_id = 'picture', component_property = 'src'),],
    Input(component_id = 'sbumit_buttom', component_property = 'n_clicks'),
    State(component_id = 'my_input', component_property = 'value'),

)

def search_movie_image(n_clicks,my_input):
    
    df = get_movie_data_using_title(my_input)
    src = df['Movie Poster Link'][0]
    
    alert_msg = "Movie Poster Generated!"
    alert = dbc.Alert(alert_msg, color="success", duration = 4000, dismissable=True)
    return alert, src


@app.callback(
    [
     Output(component_id = 'my-title', component_property = 'children'),
     Output(component_id = 'my-rating', component_property = 'children'),
     Output(component_id = 'my-genre', component_property = 'children'),
     Output(component_id = 'my-cast', component_property = 'children'),
     Output(component_id = 'my-duration', component_property = 'children'),
     Output(component_id = 'my-parental_rating', component_property = 'children'),
     Output(component_id = 'my-release_date', component_property = 'children'),
     Output(component_id = 'my-director', component_property = 'children'),],
    Input(component_id = 'sbumit_buttom', component_property = 'n_clicks'),
    State(component_id = 'my_input', component_property = 'value'),
)

def display_name(button, value):
    
    df = get_movie_data_using_title(value)
    title  = df['Movie Title'][0]
    rating = df['Rating'][0]
    genre  = df['Genre'][0]
    cast  = df['Cast'][0]
    duration  = df['Duration'][0]
    parental_rating = df['Parental Rating'][0]
    release_date = df['Release Date'][0]
    director = df['Director'][0]
    
    return title, 'Rating : {} / 10'.format(rating), 'Genre : {}'.format(genre), 'Cast : {}'.format(cast), 'Duration : {}'.format(duration), 'Parental Rating : {}'.format(parental_rating), 'Release Date : {}'.format(release_date), 'Director : {}'.format(director)


if __name__ == "__main__":
        app.run_server(debug=True, port=8060)
        


