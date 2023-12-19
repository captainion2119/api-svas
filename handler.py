from svasModels.predict import VOICE_PREDICT, FACE_PREDICT, DEP_FA_VO_TE


def test_type(type,opt):
    if type == "1":
        if opt == 1:
            return (float(VOICE_PREDICT.voice_predict(1))+float(FACE_PREDICT.face_predict(1)))/2
        elif opt == 2:
            return (VOICE_PREDICT.voice_predict(1))
        elif opt == 3:
            return (FACE_PREDICT.face_predict(1))
    elif type == "2":
        if opt == 1:
            print(float(VOICE_PREDICT.voice_predict(2))+float(FACE_PREDICT.face_predict(2))/2)
            return (float(VOICE_PREDICT.voice_predict(2))+float(FACE_PREDICT.face_predict(2)))/2
        elif opt == 2:
            return (VOICE_PREDICT.voice_predict(2))
        elif opt == 3:
            return (FACE_PREDICT.face_predict(2))
        elif opt == 4:
            return (DEP_FA_VO_TE.get_depression_level())
        elif opt == 5:
            return "TEXT ONLY MODEL TO BE IMPLEMENTED"
        elif opt == 6:
            return "AUDIO + TEXT TO BE IMPLEMENTED"
        elif opt == 7:
            return "IMAGE + TEXT TO BE IMPLEMENTED"

#test_type(1,1)