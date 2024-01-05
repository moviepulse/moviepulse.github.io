from flask import Flask, render_template, request, url_for
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (5.12,3.84)
import subprocess
import requests
import os,sys,re
from numpy import dot
from numpy.linalg import norm
from ast import literal_eval

api_key = "### PLACE YOUR GPT API KEY HERE"

#prompt
prompt_base ="Eight different emotions exist, including Amusement, Anger, Awe, Contentment, Disgust, Excitement, Fear, and Sadness. I want to examinine what emotions above are included in a synopsis. Can you judge the synopsis by distributing a total of 100 points to each of the emotions? Please just give me scores for each emotion without explanation and use commas to separate each score. The synopsis is "

#temp_setting from 0~1
temp_setting = 0

#list to screen emotion
emotion_list=["Amuse.", "Anger", "Awe", "Content.", "Disgust", "Excite.", "Fear", "Sadness"]
#=================================================================

def Which_is_the_Better_poster (result_poster1, result_poster2, result_text):
    #text
    Score_text = [float(i) for i in result_text.split(",")[-8:]]
    
    #poster1
    arr1 = literal_eval(result_poster1)
    Score_poster1 = [float(i.strip())*100 for i in arr1[2].split(",")]
    cos_sim1 = dot(Score_poster1, Score_text)/(norm(Score_poster1)*norm(Score_text))
    
    #poster2
    arr2 = literal_eval(result_poster2)
    Score_poster2 = [float(i.strip())*100 for i in arr2[2].split(",")]
    cos_sim2 = dot(Score_poster2, Score_text)/(norm(Score_poster2)*norm(Score_text))    
    
    Coef_list = [0.021,-1.086,-1.767,-1.783,-3.445,-1.768,0.918,0.2,6.996,2.381,-12.658,2.872,-0.625,-18.783,8.048,4.195]
    
    ###Add the constant back
    Model_result_poster1 = sum(x * y for x, y in zip(Score_poster1+Score_text, Coef_list))+(2.42*cos_sim1)+38.78
    Model_result_poster2 = sum(x * y for x, y in zip(Score_poster2+Score_text, Coef_list))+(2.42*cos_sim2)+38.78
    
    if (Model_result_poster1>=Model_result_poster2):
        return 1
    else:
        return 2
    

#=================================================================

def Emotion_result_output_Image (lst1, poster_num):

    arr = literal_eval(lst1)


    plt.clf()

    if(poster_num==1):
        COLOR = "#00b4d8"#"skyblue"
    else:
        COLOR = "#fb6f92"#"lightblue"
        
    plt.barh(emotion_list, [float(i.strip())*100 for i in arr[2].split(',')],color=COLOR)
    
    plt.yticks(emotion_list, fontsize=8, rotation=20)

    plt.xlabel('Values', fontsize=10)
    plt.ylabel('Emotions', fontsize=10)
    #plt.set_facecolor('#d0ccd0')
    title_str = "Emotions for Poster "+str(poster_num)
    plt.title(title_str, fontsize=10)
    plt.xlim(0, 100)
    
    file_name = "./static/bar_chart"+str(poster_num)+".png"
    
    plt.savefig(file_name)
    
#=================================================================

def remove_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
#=================================================================


def Ask_GPT(infunc_prompt):
    prompt=prompt_base+"'"+infunc_prompt+"'"

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        },
        json = {
            'model': 'gpt-4',
            'messages' : [{"role": "user", "content": prompt}],
            'temperature' :temp_setting
        })
    
    json = response.json()
    answer = json["choices"][0]['message']['content'].split(",")
    
    output="output"
    
    for emotion in range(8):
            for i in answer:
                if(i.split(":")[0].strip()==emotion_list[emotion]):
                    output+=(","+i.split(":")[1].strip())
    
    
    return output

#=================================================================

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def make_prediction():

    try:
        remove_files_in_folder("static")
        remove_files_in_folder("static/file1")
        remove_files_in_folder("static/file2")

        #render_template('index.html', result="The model is running. Please wait.")
        
        input_text = request.form['input_text']
        
               
       
        #####Image1
        if 'input_image1' not in request.files:
            return 'No file part'

        file = request.files['input_image1']
        if file.filename == '':
            return 'No selected file'
        if file:
            image1_name = file.filename
            file.save('static/file1/' + file.filename)
            
        #####Image2
        if 'input_image2' not in request.files:
            return 'No file part'

        file = request.files['input_image2']
        if file.filename == '':
            return 'No selected file'
        if file:
            image2_name = file.filename
            file.save('static/file2/' + file.filename)
            
        
        #Real output
        
        result_model1 = subprocess.run(["python", "fpn_model_predict_image1.py"], capture_output=True, text=True)
        result_model2 = subprocess.run(["python", "fpn_model_predict_image2.py"], capture_output=True, text=True)
        
        output_lines_poster1 = result_model1.stdout.splitlines()
        output_lines_poster2 = result_model2.stdout.splitlines()
        
        result_image1 = output_lines_poster1[-1] if output_lines_poster1 else None
        result_image2 = output_lines_poster2[-1] if output_lines_poster2 else None    
        
        #result_text = Ask_GPT(input_text)
        
        
        # Fake output
        # result_image1 =['rl0427521', ':', '0.00015528795,0.6592951,5.836318e-09,1.3831776e-06,0.00014431382,0.008701873,0.33167392,2.8153563e-05', ',', 'anger']
        # result_image2 =['rl3791750657', ':', '0.00015001936,0.4999637,2.9879611e-06,2.71626e-05,0.028712025,0.0004035938,0.4600123,0.010728233', ',', 'anger']
        result_text = "output,5,20,10,5,10,30,15,5"
        
        Emotion_result_output_Image(result_image1, 1)
        Emotion_result_output_Image(result_image2, 2)
        
        img1_dat="static/file1/"+image1_name
        img2_dat="static/file2/"+image2_name
           
        Selected_poster=Which_is_the_Better_poster (result_image1, result_image2, result_text) ## use for poster selection output
        
        
        #return render_template('index.html', result_text=result_text, result_image=result_image)
        return render_template('index.html', result=result_text+result_image1+result_image2, img1_dat=img1_dat, img2_dat=img2_dat, Selected_poster=Selected_poster)
        
    except:
        render_template('index.html', result="Prediction Fialed. Please check your input and retry.")

if __name__ == '__main__':
    app.run(debug=True)
