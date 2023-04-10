import json
import numpy as np
from flask import Flask, request, url_for, redirect, render_template, jsonify, session
from flask_session import Session
import pandas as pd
import random
import uuid
from ast import literal_eval
import os
from scipy.stats import percentileofscore  # pip install scipy
import time
import collections
import redis
from datetime import datetime, timedelta
from difflib import SequenceMatcher


app = Flask(__name__)
# SESSION_TYPE = 'redis'
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
app.config['SECRET_KEY'] = os.urandom(24)
app.config['JSON_SORT_KEYS'] = False
app.config.from_object(__name__)
# Session(app)
sess = Session()
sess.init_app(app)




CURRENT_SESSION = 1
cur_session_str = 's' + str(CURRENT_SESSION)
RESPONSIVE = 0   # 0: nonresponsive,  1: responsive
# session['current_session'] = CURRENT_SESSION

# r = redis.Redis(host='localhost',port=6379, db=0)
labelDict = {
    "None": "None",
    "Gun": "Gun",
}
model_detected_objects = [1,2,3] # list format, no space
ground_truth_objects = [1,2,3,4]

num_unofficial = 10
num_official = 5
count = 0

treatment_dict = {
    0: "noXAI",
    1: "saliencyMap",
    2: "similarInstances"
}
treatment = 1
session_time_limit = 60 # minutes


data = ""
trainData = ""
taskData = ""
# # predSE = [1.266335746,1.181905613,1.56584739,1.312722299,1.034996148,0.888943077,1.691238093,1.451837921,1.142564792,1.017254256,1.278425507,1.673083901,1.33825397,1.213818071,1.557312752,1.311331642,1.816822498,1.282988995,1.925545327,1.532985065,1.433913784,1.359568851,0.947197108,1.070456409,1.75195972,1.602376737,0.880697066,0.894897126,1.020497794,1.081039655,1.573805816,1.382387326,0.982603768,1.302952847,0.776193889,1.367449428,1.333245464,1.615217236,0.910971844,1.561874789,1.713096684,1.287323424,0.880125034,1.407056384,1.517514345,1.261829808,0.883408846,1.374764993,1.232656213,1.323890507,1.286209419,1.547068537,2.02330579,1.323476074,1.877748883,1.553259347,1.395610632,1.69427601,2.0356824,2.152402372,1.247177167,0.979248206,0.931380468,2.005152423,1.696962806,0.951066438,1.078659241,0.8436838,1.096114867,1.474213022,0.840531004,1.634370905,1.317155928,1.251022187,1.29731145,1.919897246,0.95994049,1.11819778,1.480574945,1.044931509,1.151374146,1.094239111,1.374838731,1.599269861,1.174366087,1.178643489,1.406525879,0.987232536,0.970105479,1.173090855,1.443901274,1.052266178,0.923969211,2.048782727,0.915177241,1.424536557,0.882797496,0.999210227,0.778746004,1.780734502,1.270253853,1.15626463,1.302115444,2.030758922,1.225928066,0.999311823,1.384394169,0.957156825,1.538384642,1.400685998,0.838156158,1.469353806,1.796591893,1.110927621,0.88486612,1.107860271,1.949661139,1.254976595,1.518757139,0.835350634,1.496794949,1.149655998,1.381829214,1.611723171,1.54723732,1.366076783,1.825887498,1.870109893,1.326928739,1.080773938,1.636691552,1.195714391,1.314511529,1.03643585,1.600727253,1.337007535,1.416797344,1.047523998,0.739297669,1.213902048,1.172197,1.026825065,1.356644436,1.736343982,1.189516475,1.469155719,1.309882988,1.637038827,0.812423411,1.111282616,0.985125012,1.588062133,1.134719046,0.775057761,1.452838463,1.115523374,1.393353578,1.493776271,1.453540583,1.821729349,1.840146878,1.191142106,1.290619876,1.391875524,1.307404599,1.175944954,1.425108796,0.91614892,1.963427727,1.806250018,1.053168412,0.832449935,0.901826632,1.370004699,0.807400021,1.661637248,1.128715328,1.291032785,1.594650009,0.980213891,1.028667862,1.348002902,1.179970026,0.807981583,0.937452003,2.122109041,1.10034095,1.130828466,1.868567385,1.368991642,0.727564768,1.392347678,1.146759446,1.810333052,1.859068853,1.271598598,1.346064399,1.392149999,1.03741474,1.22630698,1.547625051,1.510739207,1.397628343,1.578972502,1.346612528,1.526368638,1.161280495,2.011935474,1.408297485,1.249597497,1.443724287,1.199196512,0.890738424,0.822988432,1.469765985,1.595191136,1.035069712,1.461957527,1.549483811,1.029337511,0.871900905,1.362637654,1.167811378,0.772060018,0.870340505,1.347817442,1.298463507,1.499096467,0.823629645,1.096373474,1.046262828,1.43924763,1.244841032,1.138884247,1.992003748,1.280150712,1.179315425,1.583341308,1.63971615,1.173081168,1.014631306,0.986084891,1.093213599,1.326377057,1.245816049,1.091803336,1.084827365,0.857845791,1.168145315,1.163618785,1.010251428,1.200674935,1.057046061,1.581094396,1.270124184,1.058665431,1.754911343,1.785281831,1.037808235,1.346008095,1.497953694,1.059639185,0.727103148,0.929141484,0.89826607,1.120703874,0.818744559,1.570359288,2.086372294,1.15836999,1.37422724,1.888238569,0.86871016,1.365165262,1.432929003,1.44852648,1.107985911,1.202478842,1.220175579,1.682286934,1.159792919,1.018993436,1.725988972,0.907221812,0.753022988,0.859645275,2.017530276,1.20881607,1.355166763,1.158177172,1.122319364,0.85254916,1.088263917,1.025448122,2.025638257,0.988064804,1.242929066,1.1826595,1.275782222,0.990198984,1.072629344,1.588324787,1.041191163,1.246081438,0.926443894,1.126002701,1.677234932,1.408630067,0.99265985,1.162045243,0.989031379,1.313794483,1.330719927,0.927785548,1.344707408,1.366115229,0.871769766,1.180632603,2.044039119,1.350941593,1.150658533,1.280726023,0.926223887,1.313627169,1.059951733,1.536436782,1.322188836,1.405522817,1.323391238,1.206173435,1.161111734,1.605587378,0.953201615,1.65244365,1.123594216,1.968626493,1.562807543,0.976330267,1.632222494,1.474632601,0.953216354,1.616868764,1.585841523,1.416993282,1.355706741,1.433636176,1.294288442,1.057343058,0.971754856,1.326640176,1.073110029,1.455661389,1.20881928,1.52498196,1.773830518,1.200414117,1.277217203,1.114562745,1.696298258,1.226606988,1.748146646,1.3605672,1.374456884,0.992155358,1.063584014,1.194379115,1.399660253,1.344676264,1.362732292,1.074869965,1.393707123,1.03679613,1.625719268,1.120931789,1.136004809,1.000008416,1.525077031,0.847332297,1.097225997,1.327250831,0.855977062,1.39286976,1.48185894,1.681505524,1.543606893,2.129315042,1.011917653,1.439294147,0.940157837,0.993963109,1.698366108,1.094984079,1.438236477,0.908311386,0.91503726,0.8019576,1.568416083,1.398643085,1.060329149,1.73274409,0.966253433,1.071910279,1.364178577,1.341616424,1.376766698,1.283149012,1.146628247,1.415328093,1.433864337,1.818960149,1.786830693,1.460183105,1.6295943,0.988354736,1.287896715,2.168527227,1.181525683,1.380606552,1.616145336,0.830090585,1.227906085,0.954503455,1.928022019,1.764502212,0.857593249,2.065387011,0.980190688,0.879337828,1.684999134,1.158579397,1.162825379,1.915372977,0.939069809,1.941512667,1.266022869,0.780138565,1.330828642,1.071344588,1.359122282,1.358173746,1.366420359,1.136529853,1.655723156,0.841471596,1.638301142,1.121257587,1.04637571,1.386980326,0.977141524,1.147308635,1.082430426,1.321090632,1.683243055,1.728041692,0.934700758,1.106514791,1.039599922,1.401219578,1.217876651,0.901291551,1.363894882,1.093268876,1.558942906,1.181676273,1.249708238,1.919688581,1.332134628,1.822442088,1.547592459,1.100517937,1.487028297,0.925058198,1.251297635,1.552396394,1.634910144,0.96241833,1.349094526,2.134443577,1.44437915,2.031433073,2.495845839,1.716915868,2.84564844,1.343564423,2.859284248,2.281452092,1.53715959,2.480838596,1.644835875,2.849883616,1.568467713,1.695609553,2.387265826,2.583323336,2.383896609,2.36737397,2.230333277,1.801269666]
pred_interval_arr = [11.73298953,11.72417749,11.76908302,11.73808659,11.71027985,11.69827581,11.78642114,11.75445747,11.72027693,11.70872509,11.73430053,11.78382989,11.74096933,11.72743754,11.76795055,11.73793115,11.80509555,11.73479858,11.82231626,11.76475585,11.75225705,11.74341792,11.70284664,11.71346721,11.79528719,11.77399882,11.69765209,11.69872976,11.70900734,11.71443912,11.77014451,11.74608155,11.70576555,11.73699805,11.69024867,11.74433289,11.7403995,11.77575321,11.69997037,11.76855513,11.78957749,11.73527327,11.69760903,11.74901037,11.76274997,11.73250406,11.69785657,11.74518692,11.7294023,11.73934083,11.73515112,11.76659926,11.83863182,11.7392941,11.81462559,11.76741482,11.74764513,11.78685744,11.84075335,11.86137737,11.73093721,11.70548436,11.7015771,11.8355428,11.78724394,11.70316045,11.71421968,11.69492366,11.71583991,11.75724207,11.69469664,11.7783957,11.73858325,11.73134662,11.73637312,11.82139765,11.70388494,11.71792658,11.75804147,11.71116215,11.721139,11.71566457,11.74519555,11.7735764,11.72341984,11.72384909,11.74894685,11.70615501,11.70472305,11.72329217,11.75347982,11.71181887,11.70098954,11.84301261,11.70029856,11.7511166,11.69781041,11.70717123,11.6904184,11.79959543,11.73341305,11.72162041,11.73690512,11.83990789,11.72869714,11.7071799,11.7463179,11.70365696,11.76546065,11.74824916,11.69452619,11.75663377,11.80199896,11.71723505,11.69796671,11.71694463,11.82626803,11.73176898,11.76291037,11.69432545,11.7600949,11.72097035,11.74601588,11.77527446,11.76662145,11.74417314,11.80649407,11.8134139,11.73968385,11.7144146,11.77871794,11.7255776,11.73828683,11.71040718,11.77377445,11.74082732,11.75018092,11.71139375,11.68785687,11.72744624,11.72320276,11.70956049,11.74307971,11.79297789,11.72494719,11.75660902,11.7377694,11.7787662,11.69271007,11.71726871,11.70597746,11.77205922,11.71951468,11.69017329,11.75458109,11.71767167,11.74737721,11.75971108,11.75466789,11.80585172,11.8087077,11.72511222,11.73563534,11.74720199,11.73749308,11.72357811,11.75118599,11.70037461,11.82854537,11.80347306,11.71189996,11.6941186,11.69926187,11.74463069,11.69236212,11.78221012,11.71893491,11.73568075,11.77294975,11.70556519,11.70972223,11.74208452,11.72398253,11.69240229,11.70206193,11.85591767,11.71623605,11.71913862,11.81316982,11.74451256,11.68712058,11.74725794,11.7206866,11.80409856,11.81167109,11.73355871,11.74186214,11.74723451,11.71049386,11.72873675,11.76667244,11.76187783,11.747885,11.77083647,11.74192498,11.76389554,11.72211625,11.83669385,11.74915907,11.73119478,11.75345808,11.7259332,11.69841237,11.69344889,11.75668529,11.77302305,11.71028635,11.75571167,11.76691706,11.70978107,11.69699313,11.7437736,11.72276505,11.68997492,11.69687692,11.74206323,11.73650052,11.76038806,11.69349404,11.71586411,11.71128101,11.75290904,11.73068908,11.7199187,11.83332227,11.73448861,11.72391666,11.77142331,11.7791386,11.7232912,11.7084975,11.70605828,11.71556883,11.73962151,11.73079259,11.71543732,11.71478926,11.69595385,11.72279832,11.72234813,11.70811876,11.72608449,11.71224929,11.7711213,11.73339902,11.71239555,11.79572596,11.80028255,11.71052872,11.74185568,11.76024244,11.71248361,11.68709186,11.7013991,11.69898795,11.71816599,11.69315097,11.76968417,11.84957326,11.72182827,11.74512399,11.8162973,11.69675572,11.74406715,11.75213694,11.75404892,11.71695651,11.72626933,11.72809727,11.78514007,11.72196898,11.70887632,11.79145771,11.69967899,11.68873307,11.69608597,11.83764611,11.72692088,11.74290909,11.72180922,11.71832061,11.69556656,11.715108,11.70943982,11.83903068,11.70622523,11.73048634,11.72425352,11.73401284,11.70640556,11.71366598,11.77209466,11.71082901,11.73082077,11.70118521,11.71867395,11.78441997,11.74919894,11.70661397,11.72219204,11.70630685,11.73820655,11.74011297,11.70129151,11.74170665,11.74417762,11.69698335,11.72404923,11.84219291,11.74242225,11.72106873,11.73455138,11.70116779,11.73818782,11.71251189,11.76520612,11.73914905,11.74882681,11.73928454,11.72664877,11.72209954,11.7744362,11.70333416,11.78091707,11.71844277,11.82940942,11.76867896,11.70524061,11.77809778,11.75729469,11.70333536,11.77597986,11.77175987,11.75020455,11.74297142,11.75222318,11.73603935,11.7122761,11.70485987,11.73965124,11.71371001,11.75493033,11.72692121,11.7637157,11.79855549,11.72605778,11.73416895,11.71758026,11.78714829,11.72876813,11.79472144,11.74353355,11.74515086,11.7065712,11.71284116,11.72544151,11.74812691,11.74170308,11.74378458,11.71387137,11.74741915,11.71043907,11.77719832,11.71818779,11.71963924,11.70723938,11.76372802,11.69518743,11.71594392,11.73972026,11.69581694,11.74731983,11.75820322,11.78502855,11.76614462,11.8572096,11.70826265,11.75291473,11.702279,11.70672455,11.78744605,11.71573417,11.75278525,11.69976353,11.70028761,11.69198756,11.76942505,11.74800577,11.71254605,11.79244839,11.70440442,11.71360016,11.7439525,11.74135306,11.74542139,11.73481608,11.72067376,11.75000386,11.75225102,11.80542473,11.80051698,11.75549113,11.77773385,11.7062497,11.73533617,11.86431403,11.7241392,11.7458721,11.77588055,11.69395089,11.72890406,11.70344026,11.82271991,11.79715665,11.69593533,11.84589636,11.70556324,11.69754983,11.78552753,11.72184897,11.7222694,11.82066372,11.70219164,11.82492742,11.73295576,11.69051125,11.74012529,11.71354841,11.74336623,11.74325649,11.74421311,11.71969015,11.78137752,11.69476428,11.7789417,11.71821896,11.7112911,11.74662298,11.70530831,11.72074034,11.71456754,11.73902541,11.78527659,11.79175836,11.70184184,11.71681749,11.71068764,11.74831279,11.72785831,11.69922064,11.74391955,11.71557399,11.76816638,11.72415438,11.73120658,11.82136377,11.74027341,11.80596172,11.76666816,11.71625268,11.75885582,11.70107558,11.731376,11.76730095,11.77847054,11.70408844,11.74220989,11.85813166,11.75353854,11.84002354,11.92848203,11.79013304,12.00654622,11.74157581,12.00978532,11.88547267,11.76530053,11.92535103,11.77985238,12.00755069,11.76943193,11.7870492,11.90623682,11.94709155,11.90556173,11.90226435,11.87576623,11.80271195]



def interface_data_render(search_word):
    if search_word == "FIRSTPAGE":
        return list(), list()
    



    df = pd.read_csv('merged_result.csv')
    df = df.dropna()

    unique_preferred_names = df['preferred_name'].unique()
    matching_preferred_names = list()
    for name in unique_preferred_names:
        if search_word.lower() in name.lower():
            matching_preferred_names.append(name)


    

    content_idxes = df['content_index'].unique()
    interface_df = pd.DataFrame()
    for idx in content_idxes:
        tmp_df = df[df['content_index'] == idx]
        preferred_name_list = tmp_df['preferred_name'].values
        preferred_name_score_list = tmp_df['score'].values
        new_tmp_df = pd.DataFrame([[tmp_df['Titles'].values[0], tmp_df['Links'].values[0], 
                                    tmp_df['Post_Time'].values[0], tmp_df['Author'].values[0],
                                    tmp_df['Content'].values[0], idx, preferred_name_list, 
                                    preferred_name_score_list]], 
                                columns=['title', 'link', 'post_Time', 'author', 'content', 'content_index','preferred_name_list','preferred_name_score_list'])
        interface_df = pd.concat([interface_df, new_tmp_df],ignore_index=True)

    # interface_df = interface_df.set_index('content_index')
    interface_df['post_Time'] = interface_df['post_Time'].apply(lambda x: x[:-6])

# change to the corresponding dataframe matching the search keyword later
    matched_df = df[df['preferred_name'].isin(matching_preferred_names)]
    cur_df = interface_df.iloc[matched_df['content_index'].unique()]
    cur_df['cur_search_name'] = search_word
    cur_df['cur_search_name_score'] = matched_df.groupby(['content_index']).sum()['score'].values

    cur_df['post_Time_ymd'] = cur_df['post_Time'].apply(lambda x: x[:10])
    cur_month_list = pd.date_range(cur_df['post_Time_ymd'].min(),cur_df['post_Time_ymd'].max(), 
                freq='MS').strftime("%Y-%m").tolist()
 

    cur_data_list = list()
    for jdict in cur_df.to_dict(orient='records'):
        jdict['preferred_name_list'] = list(jdict['preferred_name_list'])
        jdict['preferred_name_score_list'] = list(jdict['preferred_name_score_list'])
        cur_data_list.append(jdict)
    return cur_data_list, cur_month_list






    
@app.route("/")
def index(data=data, num_official=num_official):

    r = redis.Redis(db=0)
    cur_data_list, cur_month_list = interface_data_render("FIRSTPAGE")
    return render_template("interface.html", data_arr=cur_data_list,  search_word=['Start Searching'], cur_month_list=cur_month_list)
    # return render_template("trustrepair_chat2.html", num=num, taskNum=num_official, modelDetectedLabels=model_detected_objects, groundTruthDetectedLabels=ground_truth_objects)


@app.route("/searchResultPage")
def searchResultPage():
    search_word = request.args.get("searchTerm")
    
    print("RECEIVED Searching Word !!!!!~~~~~~~~~~~~")
    print(search_word)

    cur_data_list, cur_month_list = interface_data_render(search_word)
    search_word_list = list()
    search_word_list.append(search_word)
    # cur_data_list = []
    return render_template("interface.html", data_arr=cur_data_list, search_word=search_word_list, cur_month_list=cur_month_list)




if __name__ == "__main__":
    app.config['JSON_SORT_KEYS'] = False
    app.run(debug=True, threaded=True, host='0.0.0.0')
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['JSON_SORT_KEYS'] = False
    app.config['SESSION_TYPE'] = 'redis'
