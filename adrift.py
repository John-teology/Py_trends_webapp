from pytrends.request import TrendReq
import streamlit as st
from fbprophet import Prophet
from streamlit import caching
from scipy.interpolate import interp1d
from geopy.geocoders import Nominatim
import plotly.express as px
from PIL import Image
import pandas as pd
import plotly.graph_objects as go



###################DICTIONARIES##############################################################

countries = {
        'Worldwide': '',
        'Finland' : 'FI',
        'Netherlands' : 'NL',
        'Sweden'  : 'SE',
        'Germany' : 'DE',
        'Denmark' : 'DK',
        'Switzerland' : 'CH',
        'Norway'  : 'NO',
        'France'  : 'FR',
        'Spain'   : 'ES',
        'Canada'  : 'CA',
        'Bulgaria' : 'BG',
        'Belgium' : 'BG',
        'Estonia' : 'EE',
        'United Kingdom' : 'GB',
        'Luxembourg' : 'LU',
        'Russia'  : 'RU',
        'New Zealand' : 'NZ',
        'Austria' : 'AT',
        'Italy'   : 'IT',
        'Australia' : 'AU',
        'Latvia'  : 'LV',
        'Cyprus'  : 'CY',
        'Singapore' : 'SG',
        'United States' : 'US',
        'Japan'   : 'JP',
        'North Macedonia' : 'MK',
        'South Korea'  : 'KR',
        'Moldova' : 'MD',
        'Slovakia' : 'SK',
        'Romania' : 'RO',
        'Portugal' : 'PT',
        'Malaysia' : 'MY',
        'China' : 'CN',
        'Poland'   : 'PL',
        'Philippines' : 'PH',
}
timech = {
    'Pass 7 days' : 'now 7-d',
    'Pass 90 days' : 'today 3-m',
    'Pass 12 months' : 'today 12-m',
    'Pass 5 Years' : 'today 5-y',     
}

pre_dict = {
    'now 7-d' : 2,
    'today 3-m' : 20,
    'today 12-m' : 65,  
    'today 5-y' : 365
}

typeSearch = {
    'Google Search' : '',
    'YouTube Search' : 'youtube',
    'Image Search' : 'images',
    'News Search' : 'news',
    'Google shopping Search' : 'froogle'
    
}


################### CONFIGURATION SETUP #############################################################

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout = 'wide')
icon = Image.open('appicon.png')
if st.button('Clear cache'):
            caching.clear_cache()
about = st.beta_expander('About')
about.markdown(""" 
    <p class ="about">The purpose of this web application is to <b>"visualize the number of searches based on userdefined topics, 
    show top searches and to forecast".</b>
    <br>Python Libraries used:<br><b>pytrends https://pypi.org/project/pytrends/</b>
    <br><b> fbprophet https://facebook.github.io/prophet/</p>
    </b>""",unsafe_allow_html = True)


################### STYLES ##############################################################

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200&display=swap');

.subbiggy {
    font-size: 20px   !important;
    font-weight: semi-bolder !important;
    font-family: Roboto,sans serif !important;
}

.about {
     font-size: 15px !important;
    font-family: Poppins, sans-serif  !important;
     mapping: 0px;
}
.maintitle {
    font-size: 32px   !important;
    font-family: Roboto, sans-serif  !important;
    text-align: center  !important;
}
.titles {
    font-size: 32px   !important;
    font-family: Roboto, sans-serif  !important;
}
.titles2 {
    font-size: 20px   !important;
    font-family: Poppins, sans-serif  !important;
}

.subtitles {
    font-size: 21px   !important;
    font-weight: bolder  !important;
    font-family: Poppins, sans-serif  !important;
}

.textinstructionsstyle {
     font-family: Poppins, sans-serif  !important;
     mapping: 0px;

}
.reportview-container {
    background: #0C1916;  /* fallback for old browsers */
    background: -webkit-linear-gradient(0.5turn,#2E3734CC,#07221C);  /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(0.5turn,#2E3734CC,#07221C); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    color: rgb(255, 255, 255);
}

.secondary-background-color {
    background: #1FDE83;
}
.line_chart{
    background: #0C1916;
}
</style>
""",unsafe_allow_html=True
)


################### MAIN PROGRAM ##############################################################

Title = st.beta_container()
InterestOT = st.beta_container()
Related_Q = st.beta_container()
Map_Q = st.beta_container()
Top_trends = st.beta_container()
predict = st.beta_container()
run_bot = st.form('form')
Frontface = st.beta_container()
sider = st.sidebar


@st.cache
def splitter(userinput):
    product = userinput.split('-')
    return product

def Interest_OT(kw_list, tl,country,types):
    ct = countries[country]
    pytrends = TrendReq(hl='en-US', tz=360 ,timeout= (10,25) )
    pytrends.build_payload( kw_list,
                         timeframe = tl, 
                         geo = ct,
                         gprop = typeSearch[types]
                         )
    data = pytrends.interest_over_time() 
    if 'isPartial' in data:
            del data['isPartial']
            return data


def map_plot(kwlist, timef, ct,types):
    country_map = countries[ct]
    for i in kwlist:
        cities = region_names(i, timef, country_map,types)
        lang = []
        longt = []
        for rg in cities:
            geolocator = Nominatim(user_agent="Streamlit_app",timeout = 1000)
            location = geolocator.geocode(rg)
            try:
                lang.append(location.latitude)
                longt.append(location.longitude)
            except AttributeError:
                lang.append(0)
                longt.append(0)
        dataf = world_map(i, timef, country_map,types)
        dataf['long'] = longt
        dataf['lang'] = lang
        fdata_f = dataf.reset_index()
        list1 = fdata_f[i].values.tolist()
        m = interp1d([ min(list1), max(list1)],[10, 20])
        cr = m(list1)
        zoo = 0 if ct == 'Worldwide' else 3.9
        fig = px.density_mapbox(fdata_f, lat='lang', lon='long',
                                radius=cr, zoom=zoo, color_continuous_scale="turbid",mapbox_style = 'open-street-map',z = i,hover_name = 'geoName')
        fig.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',         # para maging transparent ang background
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
        maptext = '{} Map visualization'.format(i)
        st.markdown(
            '<p class ="subtitles">{}</p>'.format(maptext), unsafe_allow_html=True)
        st.plotly_chart(fig)


def region_names(kw_list, tl, cot,types):
    list_of_kw = []
    list_of_kw.append(kw_list)
    pytrends = TrendReq(hl='en-US', tz=360,timeout= (10,25)  )
    pytrends.build_payload(list_of_kw,
                           timeframe=tl,
                           geo=cot,
                           gprop= typeSearch[types]
                           )
    tr = pytrends.interest_by_region(
        resolution='COUNTRY', inc_low_vol=False, inc_geo_code=False)
    clean = tr[tr[list_of_kw] > 0]
    clean_region = clean.dropna()
    return clean_region.index


def world_map(kw_list, tl, cut,types):
    list2_of_kw = []
    list2_of_kw.append(kw_list)
    pytrends = TrendReq(hl='en-US', tz=360,timeout= (10,25)  )
    pytrends.build_payload(list2_of_kw,
                           timeframe=tl,
                           geo=cut,
                           gprop =  typeSearch[types]
                           )
    tr = pytrends.interest_by_region(
        resolution='COUNTRY', inc_low_vol=False, inc_geo_code=False)
    clean = tr[tr[list2_of_kw] > 0]
    return clean.dropna()



@st.cache
def world_list(kw_list, tl, cut,types):
    country2 = countries[cut]
    pytrends = TrendReq(hl='en-US', tz=360,timeout= (10,25)  )
    pytrends.build_payload(kw_list,
                           timeframe=tl,
                           geo=country2,
                           gprop =  typeSearch[types]
                           )
    tr = pytrends.interest_by_region(
        resolution='COUNTRY', inc_low_vol=False, inc_geo_code=False) 
    return tr
    

@st.cache
def related_Q(relatedkw,tl,rcountry,types):
    realct = countries[rcountry]
    pytrends = TrendReq(hl = 'en-US', tz = 360 ,timeout= (10,25) )
    pytrends.build_payload( relatedkw,
                         timeframe = tl, 
                         geo= realct,
                         gprop = typeSearch[types]
                         )
    que = pytrends.related_queries()
    return que



@st.cache
def cleaning(dfname,onekw):
    df = dfname.reset_index()
    df['ds'] = df['date']
    df['y'] = df[onekw]
    df.drop([onekw,'date'],axis = 1,inplace = True)
    df.columns = ['ds','y']
    return df


@st.cache
def topcharts(loc,year):
    ct = 'GLOBAL' if loc == '' else loc
    pytrends = TrendReq(hl = 'en-US', tz = 360 ,timeout= (10,25) )
    charts = pytrends.top_charts(year, hl='en-US', tz=360, geo=ct)
    return charts.values


@st.cache        
def trendingsearch(tcountry):
    tc = tcountry.replace(' ','_')
    tct = 'philippines' if tc == 'worldwide' else tc
    pytrends = TrendReq(hl='en-US', tz=360 ,timeout= (10,25) )
    trends = pytrends.trending_searches(pn=tct)
    return trends.loc[:9]

def forecast(df,time,valName): 
    model = Prophet(interval_width = 0.65,yearly_seasonality = True if time >= 65 else False, 
                                          daily_seasonality = True if time <= 20 else False) 
    model.fit(df)
    future = model.make_future_dataframe(periods=time)
    forecast = model.predict(future)
    model.plot(forecast,xlabel='Dates', ylabel='{} Search Values'.format(valName))
    

def Prediction(prelist, tml,country,types):
    correct = countries[country]
    pytrends = TrendReq(hl='en-US', tz=360,timeout= (10,25) )
    pytrends.build_payload( prelist,
                         timeframe = tml, 
                         geo = correct,
                         gprop = typeSearch[types]
                         )
    pdata = pytrends.interest_over_time() 
    if 'isPartial' in pdata:
            del pdata['isPartial']
            return pdata


################### SIDE BAR ##############################################################
with run_bot: 
    with sider:
        st.sidebar.image(icon,use_column_width=True)
        st.markdown('<p class ="subbiggy">Navigator</p>',unsafe_allow_html = True)
        st.write('<p class ="textinstructionsstyle">Enter to Search term or a topic and seperate it with "-"</p>',unsafe_allow_html=True)
        User_input = st.text_input('Search Topic here....')
        type_of = st.selectbox('Select Type of Search',options=list(typeSearch.keys()), index=0)
        kw = splitter(User_input)
        time = st.selectbox('Select Time Frame', options = list(timech.keys()), index = 2)
        timeline = timech[time]
        country = st.selectbox('Select Country', options = list(countries.keys()), index = 35)
        st.markdown('<p class ="subbiggy">Top Search</p>',unsafe_allow_html = True)
        topchartcountry = country
        yeard = st.selectbox('Select Year', list(reversed(range(2008,2021))))
        submit = st.form_submit_button('Start the search')
        
        
with Frontface:
    st.write('<p class =maintitle> DATA VISUALIZATION OF PYTREND MADE IN STREAMLIT!</p>',unsafe_allow_html=True)

    ################### GRAPHS ##############################################################
if submit:
    
    with Title:
        st.markdown('<p class ="maintitle">Data Visualization for {}</p>'.format(User_input),
                    unsafe_allow_html=True)
        st.markdown('<p class ="titles2"> Type of Search: {}</p>'.format(type_of),
                    unsafe_allow_html=True)
    
    
    with InterestOT:
        col1,col2 = st.beta_columns((1,1))
        try:
            iot = Interest_OT(kw,timeline,country,type_of)
            dataf = iot.reset_index()
            df2 = []
            fig_line = go.Figure()
            for data in kw:
                fig_line.add_trace(go.Scatter(x=dataf.date, y=dataf[data],
                    mode='lines',
                    name=data))
                a = data,iot[data].values.mean()
                df2.append(a)
            fig_bar = px.bar(df2, color = 0,x = 0, y = 1,height=300,
                                        labels={
                                            "1": "Count", 
                                            "0": "Labels"
                                        },)
            fig_bar.update_layout({
            'plot_bgcolor': 'rgba(0, 0, 0, 0)',       
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
            fig_line.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',        
            'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
            fig_line.update_layout(
                    autosize=False,
                    height=330,)
            for i in range(2): col2.write("   ")
            col2.plotly_chart(fig_bar)
            col2.markdown('<p class ="subtitles">Average No. of Search about {}</p>'.format(User_input),unsafe_allow_html = True)
            col1.plotly_chart(fig_line)
            col1.markdown('<p class ="subtitles">Interest Over Time</p>',unsafe_allow_html = True)
            
            
            
        except AttributeError or KeyError:
                col1.error('The API return no Value')
        st.write('---')

                
    with Related_Q:
        st.markdown('<p class ="titles">RELATED QUERIES</p>',unsafe_allow_html = True)
        col1, col2 = st.beta_columns((1, 1))
        que = related_Q(kw, timeline, country,type_of)
        for man in que:
            try:
                kwof_W = [man]
                qq = world_list(kwof_W, timeline, country,type_of)
                col2.markdown('<p class ="subtitles">Number of {} queries per Region</p>'.format(man), unsafe_allow_html=True)
                col2.dataframe(qq.sort_values(man, ascending=False))
                sd = que[man]
                df = sd['rising']
                col1.markdown('<p class ="subtitles">Related queries about {} </p>'.format(man), unsafe_allow_html=True)
                col1.dataframe(df.head())
                kwof_W.append(man)
            except AttributeError or KeyError:
                col1.error('The API return no Value')
        st.write('---')


    with Map_Q:
        try:
            st.markdown('<p class ="titles">RELATED QUERIES MAP</p>',unsafe_allow_html = True)
            map_plot(kw,timeline,country,type_of)
        except ValueError:
            st.error('The API return no Value')
            st.warning('Try to input meaningful terms')
        st.write('---')
    

    with Top_trends:
        col1,col2 = st.beta_columns((2,2))
        col1.markdown('<p class ="subtitles">TOP 10 SEARCH IN THE {} IN THE YEAR {}</p>'.format(topchartcountry.upper(),yeard),unsafe_allow_html = True)
        tc = 'Philippines' if topchartcountry == 'Worldwide' else topchartcountry
        col2.markdown('<p class ="subtitles,">TOP 10 SEARCH IN {} AT THIS MOMENT</p>'.format(tc.upper()),unsafe_allow_html = True)
        try:
            col1.write(topcharts(countries[topchartcountry],yeard))
            
        except IndexError or KeyError:
            col1.error('The API return no Value')
        try:
            col2.dataframe(trendingsearch(topchartcountry.lower()))
        except AttributeError:
            col2.error('The API return no Value')
        st.write('---')

        
        st.set_option('deprecation.showPyplotGlobalUse', False)
    with predict:
        st.markdown('<p class ="titles">FORECAST </p>',unsafe_allow_html = True)
        try :
            for prelist in kw:
                dataf = Prediction([prelist],timeline,country,type_of)
                cleandf = cleaning(dataf,prelist)
                finalplot = forecast(cleandf,pre_dict[timeline],prelist)
                st.markdown('<p class ="subtitles">Prediction about {} for the next {} days</p>'.format(prelist,pre_dict[timeline]),unsafe_allow_html = True)
                st.pyplot(finalplot) 
        except AttributeError:
            st.error('The API return no Value')
            st.warning('Try to input meaningful terms')
            











