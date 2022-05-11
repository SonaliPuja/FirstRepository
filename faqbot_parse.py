import os


def faqbotparse(file_path):
    error = False
    parse_error = False
    domain_path = os.path.join(file_path, 'domains')
    #print("domain path",domain_path)
    if os.path.exists(domain_path):
        domain_folders = os.listdir(domain_path)
    else:

        return True,"domain folder not there"
    result = {}
    sections = []
    for domain in domain_folders:
        # print(domain)
        intent_folders_path = os.path.join(domain_path, domain)
        #print("intent folders,",intent_folders_path)
        if os.path.exists(intent_folders_path):
            intent_folders = os.listdir(intent_folders_path)
        else:
            return True,"no domain folder present"
        if len(intent_folders) == 0:
            return True, "no intent folders"
        for intent_folder in intent_folders:
            intent_file_path = os.path.join(intent_folders_path, intent_folder)
            # intent folder is name of intent
            train_file_path = os.path.join(intent_file_path, 'train.txt')
            #print("train file path,",train_file_path)
            if os.path.exists(train_file_path):
                error = False
            else:
                error = True
           # print(train_file_path)
            #print("-----")
            intent = {}
            intent['answers'] = []
            intent['enabled'] = True
            intent["logic"] = ""
            intent["metadata"] = {}
            intent["response_type"] = "paths"
            intent["category_name"] = intent_folder

            intent["paths"] = {
                "configurable": [],
                "default": {
                    "__ui_error_count": 0,
                    "actions": {
                        "web": [
                            {
                                "text": [
                                    "This is default messsage",
                                    "Set your custom sentence"
                                ],
                                "type": "response"
                            }
                        ]
                    }
                }
            }
            try:
                with open(train_file_path) as f:
                    #utterance_list = f.readlines()
                    utterance_list = [line.rstrip() for line in f]

            except:
               parse_error = True

            if parse_error == True:
                parse_error,utterance_list = (train_file_path)


            intent["questions"] = utterance_list

            if parse_error == True:
                error = True

            if error == True:
                return error,{}

            sections.append(intent)

    result['sections'] = sections
    # Directly from dictionary

    # with open('json_data55.json', 'w') as outfile:
    #     json.dump(result, outfile)

    return error, result

    #return {"file uploaded":"success"}


#faqbotparse("672913")


def read_file(file_path):
    enc_list = ['big5big5-tw,',
                'cp037IBM037,',
                'cp437437,',
                'cp737Greek',
                'cp850850,',
                'cp855855,',
                'cp857857,',
                'cp861861,',
                'cp863863,',
                'cp865865,',
                'cp869869,',
                'cp875Greek',
                'cp949949,',
                'cp1006Urdu',
                'cp1140ibm1140Western',
                'cp1251windows-1251Bulgarian,',
                'cp1253windows-1253Greek',
                'cp1255windows-1255Hebrew',
                'cp1257windows-1257Baltic',
                'euc_jpeucjp,',
                'euc_jisx0213eucjisx0213Japanese',
                'gb2312chinese,',
                'gb18030gb18030-2000Unified',
                'iso2022_jpcsiso2022jp,',
                'iso2022_jp_2iso2022jp-2,',
                'iso2022_jp_3iso2022jp-3,',
                'iso2022_krcsiso2022kr,',
                'iso8859_2iso-8859-2,',
                'iso8859_4iso-8859-4,',
                'iso8859_6iso-8859-6,',
                'iso8859_8iso-8859-8,',
                'iso8859_10iso-8859-10',
                'iso8859_14iso-8859-14,',
                'johabcp1361,',
                'koi8_uUkrainian',
                'mac_greekmacgreekGreek',
                'mac_latin2maclatin2,',
                'mac_turkishmacturkishTurkish',
                'shift_jiscsshiftjis,',
                'shift_jisx0213shiftjisx0213,',
                'utf_16_beUTF-16BEall',
                'utf_16_le',
                'utf_7',
                'utf_8',
                'base64_codec',
                'bz2_codec',
                'hex_codec',
                'idna',
                'mbcs',
                'palmos',
                'punycode',
                'quopri_codec',
                'raw_unicode_escape',
                'rot_13',
                'string_escape',
                'undefined',
                'unicode_escape',
                'unicode_internal',
                'uu_codec',
                'zlib_codec'
                ]

    for encode in enc_list:
        try:
            with open(file_path, encoding=encode) as f:
                #utterance_list = f.readlines()
                utterance_list = [line.rstrip() for line in f]
        except:
            enc_list.remove(encode)
        if utterance_list:
            return False,utterance_list

        else:
            return True, "not able to read file"