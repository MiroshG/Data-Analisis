import requests



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

url = 'https://results.european-games.org/EG2023/ENG/reports/BOX/all-event/UNIT'

"""https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXMO92KG-------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM71KG--------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------SFNL000200--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------SFNL000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXMO92KG-------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM92KG--------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXW54KG--------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------FNL-000100--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------R32-000800--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------R32-000200--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------8FNL000800--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------8FNL000600--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM63KG--------------QFNL000400--.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C32C1_BOXMO92KG-------------------------.pdf
https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C32C1_BOXM92KG--------------------------.pdf"""


men_weight_array=["51", "57", "63", "71", "80", "92", "092"]
women_weight_array=["50", "54", "57", "60", "66", "75"]


base_path='C:\\Users\\Mirosh\\Desktop\\Data\\'

############################################################### MEN ################################################################################

for weight in men_weight_array:
    counter_32=1
    counter_16=1
    counter_quarters=1
    counter_semi=1
    # PRELIMINARIES 32 ########################
    for _ in range(16):
        if counter_32!=17:
            if counter_32<10:
                counter_url="0"+str(counter_32)
            else:
                counter_url= str(counter_32)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM'+weight+'KG--------------R32-00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'H\\'+weight+'\\P32\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_32+=1
    # PRELIMINARIES 16 #######################
    for _ in range(8):
        if counter_16!=9:
            counter_url= "0"+str(counter_16)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM'+weight+'KG--------------8FNL00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'H\\'+weight+'\\P16\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_16+=1
    # QUARTER FINALS #########################
    for _ in range(4):
        if counter_quarters!=5:
            counter_url= "0"+str(counter_quarters)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM'+weight+'KG--------------QFNL00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'H\\'+weight+'\\Q\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_quarters+=1
    # SEMIFINALS #############################
    for _ in range(8):
        if counter_semi!=3:
            counter_url= "0"+str(counter_semi)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM'+weight+'KG--------------SFNL00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'H\\'+weight+'\\SF\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_semi+=1
    #FINALS #################################
    url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXM'+weight+'KG--------------FNL-000100--.pdf'
    response=requests.get(url, headers=headers)
    with open(base_path+'H\\'+weight+'\\F\\01.pdf', 'wb') as f:
        f.write(response.content)
    # ENTRY LIST ############################
    url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C32C1_BOXM'+weight+'KG--------------------------.pdf'
    response=requests.get(url, headers=headers)
    with open(base_path+'H\\'+weight+'\\Entry_list\\Entry_list.pdf', 'wb') as f:
        f.write(response.content)

############################################################### WOMEN ################################################################################

for weight in women_weight_array:
    counter_32=1
    counter_16=1
    counter_quarters=1
    counter_semi=1
    # PRELIMINARIES 32 ########################
    for _ in range(16):
        if counter_32!=17:
            if counter_32<10:
                counter_url="0"+str(counter_32)
            else:
                counter_url= str(counter_32)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXW'+weight+'KG--------------R32-00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'M\\'+weight+'\\P32\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_32+=1
    # PRELIMINARIES 16 #######################
    for _ in range(8):
        if counter_16!=9:
            counter_url= "0"+str(counter_16)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXW'+weight+'KG--------------8FNL-00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'M\\'+weight+'\\P16\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_16+=1
    # QUARTER FINALS #########################
    for _ in range(4):
        if counter_quarters!=5:
            counter_url= "0"+str(counter_quarters)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXW'+weight+'KG--------------QFNL00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'M\\'+weight+'\\Q\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_quarters+=1
    # SEMIFINALS #############################
    for _ in range(8):
        if counter_semi!=3:
            counter_url= "0"+str(counter_semi)
            url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXW'+weight+'KG--------------SFNL00'+ counter_url+"00--.pdf"
            response=requests.get(url, headers=headers)
            if response.status_code==200:
                with open(base_path+'M\\'+weight+'\\SF\\'+counter_url+'.pdf', 'wb') as f:
                    f.write(response.content)
            counter_semi+=1
    #FINALS #################################
    url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C73_BOXW'+weight+'KG--------------FNL-000100--.pdf'
    response=requests.get(url, headers=headers)
    with open(base_path+'M\\'+weight+'\\F\\01.pdf', 'wb') as f:
        f.write(response.content)
    # ENTRY LIST ############################
    url='https://results.european-games.org/pdf/EG2023/BOX/EG2023_BOX_C32C1_BOXW'+weight+'KG--------------------------.pdf'
    response=requests.get(url, headers=headers)
    with open(base_path+'M\\'+weight+'\\Entry_list\\Entry_list.pdf', 'wb') as f:
        f.write(response.content)